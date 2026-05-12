"""
Bot Detection Lambda v2.1 - X-Forwarded-For Edition
====================================================
Changes from v2.0:
  - Reads client IP from X-Forwarded-For header (proxy/CDN scenarios)
  - Falls back to sourceIp from API Gateway if header absent
  - Production-ready for deployment behind CloudFront/Load Balancer
"""

import json
import time
import uuid
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

# ========== CONFIGURATION ==========
VALID_EVENTS_TABLE = 'ValidEvents'
RATE_LIMIT_TABLE = 'RateLimitTracker'

RATE_LIMIT_MAX_REQUESTS = 10
RATE_LIMIT_WINDOW_SEC = 60
BLACKLIST_DURATION_SEC = 86400  # 24 hours

HONEYPOT_PATHS = [
    '/admin',
    '/wp-login.php',
    '/wp-admin',
    '/.env',
    '/phpmyadmin',
    '/.git/config',
    '/backup.sql',
    '/config.php',
]

BOT_USER_AGENTS = [
    'bot', 'crawler', 'spider', 'scraper',
    'curl', 'wget', 'python-requests', 'python-urllib',
    'googlebot', 'bingbot', 'slurp',
    'headless', 'phantomjs', 'selenium',
    'nikto', 'sqlmap', 'masscan', 'nmap',
]

# ========== AWS CLIENTS ==========
dynamodb = boto3.resource('dynamodb')
valid_events_table = dynamodb.Table(VALID_EVENTS_TABLE)
rate_limit_table = dynamodb.Table(RATE_LIMIT_TABLE)


# ========== IP RESOLUTION ==========

def resolve_client_ip(headers_lower, http_info):
    """
    Resolve the actual client IP address.
    Priority:
        1. X-Forwarded-For header (first IP = client)
        2. X-Real-IP header
        3. sourceIp from API Gateway
    """
    # Try X-Forwarded-For first (standard for proxies/CDN)
    forwarded_for = headers_lower.get('x-forwarded-for', '')
    if forwarded_for:
        # Format: "client, proxy1, proxy2" - take first (client IP)
        client_ip = forwarded_for.split(',')[0].strip()
        if client_ip:
            return client_ip
    
    # Try X-Real-IP (alternative header)
    real_ip = headers_lower.get('x-real-ip', '')
    if real_ip:
        return real_ip.strip()
    
    # Fallback to API Gateway sourceIp
    return http_info.get('sourceIp', 'unknown')


# ========== DETECTION FUNCTIONS ==========

def is_honeypot_path(path):
    if not path:
        return False
    path_lower = path.lower().rstrip('/')
    for trap in HONEYPOT_PATHS:
        trap_normalized = trap.lower().rstrip('/')
        if path_lower == trap_normalized:
            return True
        if path_lower.startswith(trap_normalized + '/'):
            return True
    return False


def add_to_blacklist(ip_address, reason):
    now = int(time.time())
    expires_at = now + BLACKLIST_DURATION_SEC
    try:
        rate_limit_table.put_item(Item={
            'ip_address': 'BL#' + ip_address,
            'blacklisted': True,
            'reason': reason,
            'banned_at': now,
            'expires_at': expires_at
        })
        print('[BLACKLIST] Added ' + ip_address + ' - reason: ' + reason)
        return True
    except ClientError as e:
        print('[ERROR] Failed to blacklist: ' + str(e))
        return False


def is_blacklisted(ip_address):
    try:
        response = rate_limit_table.get_item(Key={'ip_address': 'BL#' + ip_address})
        item = response.get('Item')
        if item is None:
            return False, None
        now = int(time.time())
        if item.get('expires_at', 0) < now:
            return False, None
        return True, item.get('reason', 'unknown')
    except ClientError as e:
        print('[ERROR] Blacklist check failed: ' + str(e))
        return False, None


def check_user_agent(user_agent):
    if not user_agent or user_agent.strip() == '':
        return True, 'empty_user_agent'
    ua_lower = user_agent.lower()
    for bot_keyword in BOT_USER_AGENTS:
        if bot_keyword in ua_lower:
            return True, 'bot_signature: ' + bot_keyword
    return False, None


def check_rate_limit(ip_address):
    now = int(time.time())
    expires_at = now + RATE_LIMIT_WINDOW_SEC
    try:
        response = rate_limit_table.get_item(Key={'ip_address': ip_address})
        item = response.get('Item')
        if item is None:
            rate_limit_table.put_item(Item={
                'ip_address': ip_address,
                'count': 1,
                'first_request': now,
                'expires_at': expires_at
            })
            return False, 1
        if item.get('expires_at', 0) < now:
            rate_limit_table.put_item(Item={
                'ip_address': ip_address,
                'count': 1,
                'first_request': now,
                'expires_at': expires_at
            })
            return False, 1
        new_count = int(item.get('count', 0)) + 1
        if new_count > RATE_LIMIT_MAX_REQUESTS:
            return True, new_count
        rate_limit_table.update_item(
            Key={'ip_address': ip_address},
            UpdateExpression='SET #c = :c',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':c': new_count}
        )
        return False, new_count
    except ClientError as e:
        print('[ERROR] Rate limit check failed: ' + str(e))
        return False, 0


def save_valid_event(request_id, timestamp, ip_address, user_agent, path, method, body):
    try:
        valid_events_table.put_item(Item={
            'request_id': request_id,
            'timestamp': timestamp,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'path': path,
            'method': method,
            'body_size': len(body) if body else 0,
            'status': 'valid'
        })
        return True
    except ClientError as e:
        print('[ERROR] Failed to save event: ' + str(e))
        return False


def build_response(status_code, message, **kwargs):
    body = {'message': message}
    body.update(kwargs)
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }


# ========== MAIN HANDLER ==========

def lambda_handler(event, context):
    request_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    request_context = event.get('requestContext', {})
    http_info = request_context.get('http', {})

    # Parse headers (case-insensitive)
    headers = event.get('headers') or {}
    headers_lower = {}
    for k, v in headers.items():
        headers_lower[k.lower()] = v

    # Resolve client IP (X-Forwarded-For -> X-Real-IP -> sourceIp)
    ip_address = resolve_client_ip(headers_lower, http_info)
    user_agent = headers_lower.get('user-agent', '')

    method = http_info.get('method', 'UNKNOWN')
    path = http_info.get('path', '/')
    body = event.get('body', '')

    print('[INFO] ' + request_id + ' | ' + method + ' ' + path + ' | IP: ' + ip_address)

    # Layer 1: Honeypot
    if is_honeypot_path(path):
        print('[HONEYPOT] ' + request_id + ' - Trap: ' + path + ' from ' + ip_address)
        add_to_blacklist(ip_address, 'honeypot_trigger: ' + path)
        return build_response(404, 'Not Found', request_id=request_id)

    # Layer 2: Blacklist
    is_banned, ban_reason = is_blacklisted(ip_address)
    if is_banned:
        print('[BLOCKED] ' + request_id + ' - Blacklisted - ' + str(ban_reason))
        return build_response(403, 'Access denied: IP blacklisted',
                            reason=ban_reason, request_id=request_id)

    # Layer 3: User-Agent
    is_bot, bot_reason = check_user_agent(user_agent)
    if is_bot:
        print('[BLOCKED] ' + request_id + ' - Bot UA: ' + bot_reason)
        return build_response(403, 'Access denied: Bot detected',
                            reason=bot_reason, request_id=request_id)

    # Layer 4: Rate Limit
    is_rate_limited, current_count = check_rate_limit(ip_address)
    if is_rate_limited:
        print('[BLOCKED] ' + request_id + ' - Rate limit: ' + str(current_count))
        return build_response(429, 'Too many requests',
                            reason='rate_limit_exceeded',
                            current_count=current_count,
                            limit=RATE_LIMIT_MAX_REQUESTS,
                            request_id=request_id)

    # Layer 5: Save valid
    save_valid_event(request_id, timestamp, ip_address, user_agent, path, method, body)
    print('[ACCEPTED] ' + request_id + ' - Valid from ' + ip_address)

    return build_response(200, 'Request accepted',
                        request_id=request_id,
                        timestamp=timestamp,
                        count=current_count)
