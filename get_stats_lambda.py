"""
Get Stats Lambda Function
Project: Real-time Event-driven Bot Detection System
Description: Reads data from DynamoDB and returns stats for Dashboard
"""

import json
import time
import boto3
from collections import Counter
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

# ========== CONFIGURATION ==========
VALID_EVENTS_TABLE = 'ValidEvents'
RATE_LIMIT_TABLE = 'RateLimitTracker'

# ========== AWS CLIENTS ==========
dynamodb = boto3.resource('dynamodb')
valid_events_table = dynamodb.Table(VALID_EVENTS_TABLE)
rate_limit_table = dynamodb.Table(RATE_LIMIT_TABLE)


def get_valid_events():
    """
    ดึง valid events ทั้งหมดจาก DynamoDB (รองรับ pagination)
    """
    try:
        response = valid_events_table.scan()
        items = response.get('Items', [])

        # Pagination — DynamoDB scan return สูงสุด 1MB ต่อรอบ
        while 'LastEvaluatedKey' in response:
            response = valid_events_table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))

        return items
    except Exception as e:
        print('Error scanning ValidEvents: ' + str(e))
        return []


def get_blacklist():
    """
    ดึง blacklisted IPs ทั้งหมดจาก RateLimitTracker (filter เฉพาะ BL# prefix)
    """
    try:
        response = rate_limit_table.scan(
            FilterExpression=Attr('ip_address').begins_with('BL#')
        )
        return response.get('Items', [])
    except Exception as e:
        print('Error scanning blacklist: ' + str(e))
        return []


def build_response(status_code, body):
    """
    สร้าง HTTP response พร้อม CORS headers
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        },
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    """
    Main handler: รวบรวม stats จาก DynamoDB และส่งกลับให้ Dashboard
    """
    # ========== 1. ดึงข้อมูล ==========
    valid_events = get_valid_events()
    blacklist = get_blacklist()

    # ========== 2. คำนวณ Stats ==========
    total_valid = len(valid_events)
    unique_ips = set()
    user_agents = Counter()
    paths = Counter()
    recent_events = []

    for event_item in valid_events:
        ip = event_item.get('ip_address', 'unknown')
        ua = event_item.get('user_agent', 'unknown')
        path = event_item.get('path', '/')
        ts = event_item.get('timestamp', '')

        unique_ips.add(ip)

        # ตัด UA ให้สั้น 50 ตัวอักษร
        ua_short = ua[:50] if ua else 'empty'
        user_agents[ua_short] += 1
        paths[path] += 1

        recent_events.append({
            'timestamp': ts,
            'ip': ip,
            'user_agent': ua_short,
            'path': path,
            'status': 'allowed'
        })

    # Sort recent events จากใหม่ → เก่า และเอาแค่ 20 ตัวล่าสุด
    recent_events.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    recent_events = recent_events[:20]

    # ========== 3. จัดการ Blacklist ==========
    blacklist_details = []
    for entry in blacklist:
        ip_full = entry.get('ip_address', '')
        ip_clean = ip_full.replace('BL#', '')
        blacklist_details.append({
            'ip': ip_clean,
            'reason': entry.get('reason', 'unknown'),
            'banned_at': entry.get('banned_at', 0),
            'expires_at': entry.get('expires_at', 0)
        })

    # Sort blacklist จากที่ ban ล่าสุด
    blacklist_details.sort(key=lambda x: x.get('banned_at', 0), reverse=True)

    # ========== 4. Build Response ==========
    response_body = {
        'summary': {
            'total_valid_requests': total_valid,
            'unique_users': len(unique_ips),
            'total_blacklisted': len(blacklist),
            'updated_at': int(time.time())
        },
        'top_user_agents': [
            {'user_agent': ua, 'count': count}
            for ua, count in user_agents.most_common(5)
        ],
        'top_paths': [
            {'path': p, 'count': count}
            for p, count in paths.most_common(5)
        ],
        'recent_events': recent_events,
        'blacklist': blacklist_details[:10]
    }

    return build_response(200, response_body)
