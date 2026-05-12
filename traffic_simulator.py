"""
Bot Detection Traffic Simulator v2.0 - IP Spoofing Edition
==========================================================
Simulates realistic traffic with mixed real users and bots,
each with their own unique IP address (via X-Forwarded-For header).

Usage:
    python3 traffic_simulator.py [duration_in_seconds]

Example:
    python3 traffic_simulator.py 60

Requirements:
    Lambda must read X-Forwarded-For header (lambda_function.py v2.1+)
"""

import sys
import time
import json
import random
import threading
import urllib.request
import urllib.error
from collections import defaultdict, Counter

# ========== CONFIGURATION ==========
API_BASE_URL = "https://nf8fmqpd95.execute-api.us-east-1.amazonaws.com"
DEFAULT_DURATION = 60  # seconds


# ANSI color codes
class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'


# ========== PERSONAS ==========
# Each persona has a unique IP address (X-Forwarded-For)
# Using TEST-NET ranges (RFC 5737) to avoid conflict with real IPs
#   203.0.113.0/24 - reserved for documentation/testing (real users)
#   198.51.100.0/24 - reserved for documentation/testing (bots)

REAL_USERS = [
    {
        'name': 'Alice',
        'icon': '👤',
        'ip': '203.0.113.10',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'os': 'Win/Chrome',
        'interval': (3, 8),
        'paths': ['/api/v1/data'],
    },
    {
        'name': 'Bob',
        'icon': '👤',
        'ip': '203.0.113.20',
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'os': 'Mac/Safari',
        'interval': (2, 5),
        'paths': ['/api/v1/data'],
    },
    {
        'name': 'Charlie',
        'icon': '👤',
        'ip': '203.0.113.30',
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'os': 'Linux/Firefox',
        'interval': (5, 10),
        'paths': ['/api/v1/data'],
    },
    {
        'name': 'Diana',
        'icon': '👤',
        'ip': '203.0.113.40',
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'os': 'iOS/Safari',
        'interval': (4, 9),
        'paths': ['/api/v1/data'],
    },
    {
        'name': 'Eve',
        'icon': '👤',
        'ip': '203.0.113.50',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/120.0.0.0',
        'os': 'Win/Edge',
        'interval': (3, 7),
        'paths': ['/api/v1/data'],
    },
]

BOTS = [
    {
        'name': 'NaiveBot',
        'icon': '🤖',
        'ip': '198.51.100.10',
        'user_agent': 'curl/7.88.1',
        'os': 'curl-cli',
        'behavior': 'naive',
        'interval': (1, 3),
        'paths': ['/api/v1/data'],
    },
    {
        'name': 'SpamBot',
        'icon': '🤖',
        'ip': '198.51.100.20',
        'user_agent': 'Mozilla/5.0 (compatible; spambot/1.0)',
        'os': 'spam-attack',
        'behavior': 'burst',
        'interval': (0.1, 0.3),
        'paths': ['/api/v1/data'],
    },
    {
        'name': 'ScannerBot',
        'icon': '🤖',
        'ip': '198.51.100.30',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
        'os': 'fake-chrome',
        'behavior': 'honeypot_scan',
        'interval': (2, 5),
        'paths': ['/admin', '/wp-login.php', '/.env', '/api/v1/data'],
    },
    {
        'name': 'StealthBot',
        'icon': '🤖',
        'ip': '198.51.100.40',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
        'os': 'slow-burn',
        'behavior': 'slow',
        'interval': (8, 15),
        'paths': ['/api/v1/data'],
    },
]


# ========== STATISTICS ==========
class Stats:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_requests = 0
        self.status_counts = Counter()
        self.latencies = []
        self.by_persona = defaultdict(lambda: {'sent': 0, 'blocked': 0, 'allowed': 0})
        self.start_time = time.time()

    def record(self, persona_name, status_code, latency_ms):
        with self.lock:
            self.total_requests += 1
            self.status_counts[status_code] += 1
            self.latencies.append(latency_ms)
            self.by_persona[persona_name]['sent'] += 1
            if status_code == 200:
                self.by_persona[persona_name]['allowed'] += 1
            else:
                self.by_persona[persona_name]['blocked'] += 1

    def get_percentile(self, p):
        if not self.latencies:
            return 0
        sorted_lat = sorted(self.latencies)
        idx = int(len(sorted_lat) * p / 100)
        return sorted_lat[min(idx, len(sorted_lat) - 1)]

    def get_avg_latency(self):
        return sum(self.latencies) / len(self.latencies) if self.latencies else 0


stats = Stats()


# ========== HTTP REQUEST ==========

def make_request(persona, path):
    """Send HTTP request with spoofed IP (X-Forwarded-For)."""
    url = API_BASE_URL + path
    method = 'POST' if path == '/api/v1/data' else 'GET'

    body = json.dumps({
        "msg": "simulated request",
        "persona": persona['name']
    }).encode('utf-8')

    request = urllib.request.Request(
        url,
        data=body if method == 'POST' else None,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': persona['user_agent'],
            'X-Forwarded-For': persona['ip'],  # Spoof IP per persona
        },
        method=method
    )

    start = time.time()
    status_code = 0

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status_code = response.status
            response.read()
    except urllib.error.HTTPError as e:
        status_code = e.code
        try:
            e.read()
        except Exception:
            pass
    except Exception:
        status_code = 0

    latency_ms = (time.time() - start) * 1000
    stats.record(persona['name'], status_code, latency_ms)

    elapsed = time.time() - stats.start_time

    if status_code == 200:
        status_color = Color.GREEN
        emoji = '✅'
    elif status_code == 403:
        status_color = Color.RED
        emoji = '🚫'
    elif status_code == 404:
        status_color = Color.YELLOW
        emoji = '🍯'
    elif status_code == 429:
        status_color = Color.MAGENTA
        emoji = '🛑'
    else:
        status_color = Color.GRAY
        emoji = '❓'

    print(
        Color.GRAY + '[T+' + ('%5.1f' % elapsed) + 's]' + Color.RESET + ' ' +
        persona['icon'] + ' ' + Color.BOLD + ('%-11s' % persona['name']) + Color.RESET + ' ' +
        Color.GRAY + '(' + ('%-15s' % persona['ip']) + ')' + Color.RESET + ' ' +
        ('%-5s' % method) + ' ' + ('%-20s' % path) + ' ' +
        '-> ' + status_color + str(status_code) + ' ' + emoji + Color.RESET + ' ' +
        Color.GRAY + ('%5.0fms' % latency_ms) + Color.RESET
    )


def simulate_persona(persona, duration):
    """Simulate one persona sending requests."""
    behavior = persona.get('behavior', 'normal')
    end_time = time.time() + duration

    if behavior == 'burst':
        # Burst attack - rapid fire
        burst_count = 15
        for _ in range(burst_count):
            if time.time() >= end_time:
                break
            path = random.choice(persona['paths'])
            make_request(persona, path)
            time.sleep(random.uniform(*persona['interval']))
        return

    while time.time() < end_time:
        path = random.choice(persona['paths'])
        make_request(persona, path)
        time.sleep(random.uniform(*persona['interval']))


# ========== OUTPUT ==========

def print_banner():
    print()
    print(Color.BOLD + Color.CYAN + '=' * 80 + Color.RESET)
    print(Color.BOLD + Color.CYAN + '  🛡️  Bot Detection System - Traffic Simulator v2.0' + Color.RESET)
    print(Color.BOLD + Color.CYAN + '=' * 80 + Color.RESET)
    print(Color.GRAY + '🎯 Target:    ' + API_BASE_URL + Color.RESET)
    print(Color.GRAY + '👥 Users:     ' + str(len(REAL_USERS)) + ' real personas' + Color.RESET)
    print(Color.GRAY + '🤖 Bots:      ' + str(len(BOTS)) + ' bot personas' + Color.RESET)
    print(Color.GRAY + '🌐 IP source: X-Forwarded-For header (per-persona IP)' + Color.RESET)
    print()


def print_summary():
    duration = time.time() - stats.start_time
    total = stats.total_requests

    print()
    print()
    print(Color.BOLD + Color.CYAN + '=' * 80 + Color.RESET)
    print(Color.BOLD + Color.CYAN + '  📊 Final Statistics (' + ('%.1f' % duration) + ' seconds)' + Color.RESET)
    print(Color.BOLD + Color.CYAN + '=' * 80 + Color.RESET)
    print()

    print(Color.BOLD + 'Total Requests:     ' + Color.RESET + str(total))

    if total == 0:
        print(Color.YELLOW + '⚠️  No requests sent.' + Color.RESET)
        return

    # Status code breakdown
    print()
    print(Color.BOLD + 'Status Code Distribution:' + Color.RESET)
    for code, count in sorted(stats.status_counts.items()):
        pct = (count / total) * 100
        if code == 200:
            color, label, emoji = Color.GREEN, 'Valid (allowed)', '✅'
        elif code == 403:
            color, label, emoji = Color.RED, 'Blocked (bot/blacklist)', '🚫'
        elif code == 404:
            color, label, emoji = Color.YELLOW, 'Honeypot triggered', '🍯'
        elif code == 429:
            color, label, emoji = Color.MAGENTA, 'Rate limited', '🛑'
        else:
            color, label, emoji = Color.GRAY, 'Other', '❓'
        bar = '█' * int(pct / 2)
        print('  ' + color + emoji + ' ' + str(code) + ' ' + ('%-28s' % label) + Color.RESET + ' ' +
              ('%4d' % count) + ' (' + ('%5.1f' % pct) + '%) ' + color + bar + Color.RESET)

    # Performance
    print()
    print(Color.BOLD + '⚡ Performance Metrics:' + Color.RESET)
    print('  Avg latency:    ' + ('%6.1f' % stats.get_avg_latency()) + ' ms')
    print('  p50 latency:    ' + ('%6.1f' % stats.get_percentile(50)) + ' ms')
    print('  p95 latency:    ' + ('%6.1f' % stats.get_percentile(95)) + ' ms')
    print('  p99 latency:    ' + ('%6.1f' % stats.get_percentile(99)) + ' ms')
    print('  Throughput:     ' + ('%6.1f' % (total / duration)) + ' req/sec')

    # By persona
    print()
    print(Color.BOLD + '👥 By Persona:' + Color.RESET)
    print('  ' + ('%-14s' % 'Persona') + ' ' + ('%-15s' % 'IP Address') + ' ' +
          ('%6s' % 'Sent') + ' ' + ('%8s' % 'Allowed') + ' ' + ('%8s' % 'Blocked') + ' ' +
          ('%15s' % 'Detection'))
    print('  ' + ('-' * 14) + ' ' + ('-' * 15) + ' ' + ('-' * 6) + ' ' +
          ('-' * 8) + ' ' + ('-' * 8) + ' ' + ('-' * 15))

    real_user_names = {u['name'] for u in REAL_USERS}
    persona_lookup = {p['name']: p for p in REAL_USERS + BOTS}

    for persona_name, data in sorted(stats.by_persona.items()):
        is_real = persona_name in real_user_names
        sent = data['sent']
        allowed = data['allowed']
        blocked = data['blocked']
        ip = persona_lookup.get(persona_name, {}).get('ip', '?')

        if is_real:
            rate = (blocked / sent * 100) if sent > 0 else 0
            rate_color = Color.GREEN if rate == 0 else Color.YELLOW if rate < 10 else Color.RED
            rate_label = 'FP: ' + ('%.1f' % rate) + '%'
        else:
            rate = (blocked / sent * 100) if sent > 0 else 0
            rate_color = Color.GREEN if rate >= 90 else Color.YELLOW if rate >= 70 else Color.RED
            rate_label = 'TP: ' + ('%.1f' % rate) + '%'

        icon = '👤' if is_real else '🤖'
        print('  ' + icon + ' ' + ('%-11s' % persona_name) + ' ' +
              ('%-15s' % ip) + ' ' + ('%6d' % sent) + ' ' +
              Color.GREEN + ('%8d' % allowed) + Color.RESET + ' ' +
              Color.RED + ('%8d' % blocked) + Color.RESET + ' ' +
              rate_color + ('%15s' % rate_label) + Color.RESET)

    # Detection accuracy
    real_sent = sum(stats.by_persona[u['name']]['sent'] for u in REAL_USERS)
    real_blocked = sum(stats.by_persona[u['name']]['blocked'] for u in REAL_USERS)
    bot_sent = sum(stats.by_persona[b['name']]['sent'] for b in BOTS)
    bot_blocked = sum(stats.by_persona[b['name']]['blocked'] for b in BOTS)

    fp_rate = (real_blocked / real_sent * 100) if real_sent > 0 else 0
    tp_rate = (bot_blocked / bot_sent * 100) if bot_sent > 0 else 0

    print()
    print(Color.BOLD + '🎯 Detection Accuracy:' + Color.RESET)
    print('  True Positives:    ' + Color.GREEN + str(bot_blocked) + '/' + str(bot_sent) +
          ' bots blocked (' + ('%.1f' % tp_rate) + '%)' + Color.RESET)
    fp_color = Color.GREEN if fp_rate < 5 else Color.YELLOW
    print('  False Positives:   ' + fp_color + str(real_blocked) + '/' + str(real_sent) +
          ' users blocked (' + ('%.1f' % fp_rate) + '%)' + Color.RESET)

    print()
    print(Color.BOLD + Color.CYAN + '=' * 80 + Color.RESET)
    print()


def main():
    duration = DEFAULT_DURATION
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            pass

    print_banner()
    print(Color.YELLOW + '⏱️  Running for ' + str(duration) + ' seconds...' + Color.RESET)
    print()

    threads = []
    all_personas = REAL_USERS + BOTS

    for persona in all_personas:
        t = threading.Thread(target=simulate_persona, args=(persona, duration))
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(0.2)

    for t in threads:
        t.join(timeout=duration + 5)

    print_summary()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print(Color.YELLOW + '⚠️  Interrupted by user' + Color.RESET)
        print_summary()