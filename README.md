<h1 align="center">🔐 The Digital Sieve Optimizing Infrastructure Costs via Serverless Bot Defense</h1>

<p align="center">
  <em>
    Fail‑fast bot defense at the edge — filter early, scale automatically, pay only for value.
  </em>
</p>

<p align="center">
  <code>#AWS</code>
  <code>#Serverless</code>
  <code>#CyberSecurity</code>
  <code>#CloudEngineering</code>
  <code>#TheDigitalSieve</code>
</p>

---

## 🚀 1. บทนำ (Introduction)

### 🌐 1.1 สภาพแวดล้อมและปัญหา (The Problem)

ในยุคที่การเปลี่ยนผ่านสู่ดิจิทัลเกิดขึ้นอย่างรวดเร็ว แพลตฟอร์ม **E-commerce** และระบบ **Analytics** ต้องเผชิญกับความท้าทายจากปริมาณทราฟฟิกที่มีความผันผวนสูง (High Volatility) และไม่สามารถคาดการณ์ได้ล่วงหน้า

หนึ่งในภัยเงียบที่สำคัญที่สุด คือ **บอท (Bots)** ซึ่งเป็นซอฟต์แวร์อัตโนมัติที่พยายามปลอมแปลงตัวตนเป็นผู้ใช้งานจริง (Spoofing) เพื่อแทรกซึมเข้าสู่ระบบ หากไม่มีการคัดกรองที่มีประสิทธิภาพ จะก่อให้เกิดผลกระทบแบบลูกโซ่ (Chain Reaction) ดังนี้:

- **Increased Infrastructure Cost** ต้นทุนพุ่งสูงจากการใช้ทรัพยากรประมวลผล (Compute) และพื้นที่จัดเก็บข้อมูล (Storage) ไปกับ Request ที่ไม่มีมูลค่าทางธุรกิจ

- **Distorted Analytics** ข้อมูลขยะ (Garbage Data) ปะปนในระบบ ส่งผลให้รายงานวิเคราะห์ผิดเพี้ยน และนำไปสู่การตัดสินใจเชิงกลยุทธ์ที่ผิดพลาด

- **Late-stage Detection Limitation** การตรวจจับที่เกิดขึ้นชั้นในของระบบ (Core System) ทำให้โครงสร้างพื้นฐานรับภาระตั้งแต่ต้นทางโดยไม่จำเป็น

## 

### 💡 1.2 แนวคิด “The Digital Sieve”

โครงการนี้นำเสนอจุดเปลี่ยนเชิงกลยุทธ์ผ่านแนวคิด **“The Digital Sieve”** กลไกการคัดกรองบอทแบบเรียลไทม์ 5 ชั้น (5-Layer Intelligent Filtering) ที่เน้นการสกัดกั้นภัยคุกคามตั้งแต่ **Ingestion Layer** สถาปัตยกรรมถูกออกแบบในรูปแบบ 
**Event-driven Serverless บน Amazon Web Services (AWS)** เพื่อให้ระบบสามารถปรับขนาด (Auto-scaling) ได้โดยอัตโนมัติ พร้อมรักษาต้นทุนให้ต่ำที่สุด

##

### 💎 1.3 ความคุ้มค่าและมาตรฐานระดับ Enterprise

ระบบถูกออกแบบเพื่อสร้างคุณค่าเชิงธุรกิจควบคู่กับความยั่งยืนระยะยาว:

- **Micro-Cost Architecture** ต้นทุนการดำเนินงานต่ำมาก ≈ **$2.00 ต่อ 1 ล้าน Requests**

- **AWS Well-Architected Framework** สอดคล้องกับทั้ง **6 เสาหลัก** โดยเฉพาะด้าน:
  - Cost Optimization (Pay-as-you-go)
  - Sustainability (ลดพลังงานและทรัพยากรที่สูญเสียไปกับข้อมูลขยะ)

---

## 🎯 2. วัตถุประสงค์ของโครงการ (Project Objectives)

1. เพื่อสกัดกั้นบอทตั้งแต่ชั้น Data Ingestion Layer ก่อนที่ข้อมูลขยะจะเข้าสู่ระบบประมวลผลหลัก (Core System)

2. ออกแบบสถาปัตยกรรมระบบโดยใช้ Event-driven & Serverless Computing เพื่อรองรับโหลดแบบฉับพลัน โดยไม่ต้องตั้งเซิร์ฟเวอร์ล่วงหน้า

3. ระบบสามารถตัด Request ที่ไม่มีมูลค่าทางธุรกิจตั้งแต่ต้นทาง เพื่อลด Infrastructure Cost และเพิ่ม Data Purity สำหรับงาน Analytics

---

## 🏗️ 3. สถาปัตยกรรมระบบ (System Architecture)

ระบบถูกออกแบบภายใต้แนวคิด **Event-driven Serverless Architecture บน AWS** เพื่อให้ทุกองค์ประกอบทำงานร่วมกันอย่างยืดหยุ่น อัตโนมัติ และมีความทนทานสูง

### 🛠️ 3.1 ส่วนประกอบหลักของระบบ (Core Components)

- **1. Amazon API Gateway** ทำหน้าที่เป็น Entry Point สำหรับรับ HTTP Requests ทั้งหมดจาก Client

- **2. AWS Lambda - BotDetector** Processing Engine หลัก บรรจุตรรกะการคัดกรองบอททั้ง 5 ชั้น

- **3. Amazon DynamoDB** ฐานข้อมูล NoSQL แบบ Single-table Design ใช้จัดเก็บ:
  - IP Blacklist
  - Valid Events

- **4. Amazon CloudWatch** ระบบ Logging & Monitoring รองรับ Audit Trail และ Behavioral Analysis

- **5. Amazon S3 (Static Website Hosting)** ใช้ Deploy Dashboard สำหรับแสดงผลสถิติการคัดกรองแบบ Real-time

##

### ⚖️ 3.2 การวิเคราะห์เปรียบเทียบและเหตุผลความจำเป็นทางสถาปัตยกรรม

**AWS Lambda**
- **ข้อดี (Pros):**
   - Cost Efficiency: มีโครงสร้างต้นทุนแบบจ่ายตามการใช้งานจริง (Pay-as-you-go) และไม่ต้องเสียค่าใช้จ่ายในช่วงที่ไม่มีทราฟฟิก (Zero Idle Cost)
   - Auto-scaling: สามารถขยายตัวรองรับทราฟฟิกพร้อมกัน (Concurrent)
- **ข้อเสีย/ข้อจำกัด (Cons):**
   - High Operational Cost for Sustained Heavy Loads: ในกรณีที่ระบบต้องรองรับทราฟฟิกในปริมาณมหาศาลและมีความต่อเนื่องตลอดเวลา (Constant High Traffic) รูปแบบการเก็บเงินแบบจ่ายตามการเรียกใช้งาน (Pay-per-use) ของ Lambda อาจทำให้มียอดค่าใช้จ่ายรวมที่สูง
   - Cold Start: หากฟังก์ชันไม่ได้ถูกเรียกใช้งานนานเกินไป การเริ่มทำงานครั้งแรกอาจมีความหน่วง
- **ทางเลือกอื่น (Alternatives):**
   - AWS WAF: มีระบบ Bot Control ในตัวโดยไม่ต้องเขียนโค้ด แต่มีค่าใช้จ่ายคงที่รายเดือนสูง
   - Amazon EC2: ควบคุมสภาพแวดล้อมได้ทั้งหมดและไม่มี Cold Start แต่ต้องเสียค่า Idle Cost ตลอดเวลาและต้องดูแลระบบเอง

**Amazon DynamoDB**
- **ข้อดี (Pros):**
   - Single-table Design: การรวม Blacklist และ Valid Events ไว้ในตารางเดียว ซึ่งจะช่วยลดต้นทุน (Read/Write Capacity) และเพิ่มประสิทธิภาพในการขยายตัว
   - Automated Lifecycle (TTL): ฟีเจอร์ Time To Live ช่วยลบข้อมูล Blacklist ที่หมดอายุได้อัตโนมัติ ช่วยลดภาระงานและประหยัดค่าใช้จ่าย
- **ข้อเสีย/ข้อจำกัด (Cons):**
   - Query Constraints: ความยืดหยุ่นในการค้นหาข้อมูลน้อยกว่าฐานข้อมูล SQL โดยต้องวางแผนการเข้าถึงข้อมูลล่วงหน้าอย่างละเอียด
- **ทางเลือกอื่น (Alternatives):**
   - Amazon ElastiCache (Redis): ให้ความเร็วสูงกว่าในระดับไมโครวินาที เหมาะสำหรับเก็บข้อมูลชั่วคราวอย่าง Rate Limit แต่มีค่าใช้จ่ายในการเปิดเซิร์ฟเวอร์ทิ้งไว้
   - Amazon EC2: ควบคุมสภาพแวดล้อมได้ทั้งหมดและไม่มี Cold Start แต่ต้องเสียค่า Idle Cost ตลอดเวลาและต้องดูแลระบบเอง

##

### 🔄 3.3 System Architecture Diagram
```mermaid
flowchart LR
    Client["Client<br/>(Browser / Bot)"]
    APIGW["Amazon API Gateway"]
    Lambda["AWS Lambda<br/>BotDetector"]
    CW["CloudWatch Logs"]
    DDB[("DynamoDB")]
    S3["S3 Static Website<br/>Dashboard"]
    Admin["Admin / System Operator"]

    Client -->|HTTP Request| APIGW
    APIGW --> Lambda

    Lambda -->|Block| CW
    Lambda -->|Metrics| CW
    Lambda -->|Allow| DDB

    DDB -->|Valid Events| S3

    CW -->|Monitoring| Admin
    S3 -->|Visualization| Admin
```

##

## 🧹 4. Data Cleansing

### 4.1 การปรับรูปแบบข้อมูลนำเข้า (Input Normalization)
- **HTTP Headers:** แปลง Key ทั้งหมดใน Headers เป็น Lowercase เพื่อแก้ปัญหา Case-sensitive ระหว่างโปรโตคอล HTTP กับ Python Dictionary ทำให้การเรียกใช้ user-agent มีความถูกต้องเสมอ
- **User-Agent Signature:** แปลงค่า User-Agent เป็น Lowercase ทั้งหมดก่อนนำไปตรวจสอบกับฐานข้อมูลบอท เพื่อสกัดกั้นบอทที่พยายามบิดเบือนตัวพิมพ์ เช่น CURL, Curl หรือ cURL
- **Access Path:** ปรับ Path ที่เรียกเข้ามาให้เป็น Lowercase และใช้ตรรกะตัดเครื่องหมาย / ที่ต่อท้ายออก เพื่อป้องกันบอทที่พยายามเรียก Path กับดักในรูปแบบต่าง ๆ เช่น /Admin, /admin/ หรือ /.ENV

### 4.2 การสกัดและการตรวจสอบข้อมูล (Data Extraction & Validation)
- **IP Address Sanitization:** ในกรณีที่มีการใช้งานผ่าน Proxy ระบบจะสกัด IP จาก Header X-Forwarded-For โดยทำการ Split เพื่อเอาเฉพาะ IP ต้นทาง และใช้การ Strip เพื่อตัดช่องว่างที่อาจปะปนมาออก
- **Payload Size Verification:** มีการตรวจสอบค่าว่าง (None Check) ของ Body Size ก่อนนำไปบันทึกลงฐานข้อมูล เพื่อป้องกันความผิดพลาด (Runtime Error) ในกรณีที่ Request ไม่มีข้อมูลส่วน Body ส่งมาด้วย

### 4.3 การจัดการข้อมูลเพื่อการแสดงผล (Data Sanitization for Presentation)
- **Prefix Stripping:** ในหน้า Dashboard ระบบจะทำการลบค่า Internal Prefix (BL#) ออกจาก IP Address ก่อนการแสดงผล เพื่อให้ข้อมูลในตาราง Blacklist ดูสะอาดและไม่แสดงโครงสร้างการจัดเก็บภายในให้ผู้ใช้ทั่วไปเห็น

---

## 🛡️ 5. AWS Lambda BotDetector

### 🤖 5.1 กระบวนการคัดกรองบอท 5 ชั้น (5-Layer Intelligent Filtering)

### 🪤 Layer 1: Honeypot
เลเยอร์ที่เร็วที่สุดและแม่นยำที่สุด โดยการตรวจสอบ Path ที่ Client เรียกเข้ามา หากตรงกับ "กับดัก" ที่ตั้งไว้ (เช่น /admin, /.env, /wp-login.php) ระบบจะตัดสินว่าเป็นบอททันที
- Zero-False-Positive: ผู้ใช้งานจริงไม่มีเหตุผลที่จะเข้าถึง Path เหล่านี้
- Action: บล็อก IP เข้าสู่ Blacklist ทันที และตอบกลับด้วย 404 Not Found (Stealth Mode)

**ฟังก์ชัน is_honeypot_path()** 
```python
def is_honeypot_path(path):
    if not path:
        return False
    
    path_lower = path.lower()
    
    for trap in HONEYPOT_PATHS:
        if path_lower.startswith(trap):
            return True
    
    return False
```

##

### 🚫 Layer 2: IP Blacklist
ระบบจะตรวจสอบ IP Address ในฐานข้อมูล RateLimitTracker ว่าเคยถูกแบนจากการติดกับดัก Honeypot หรือไม่
- Efficiency: หากพบใน Blacklist ระบบจะยุติการทำงานทันทีโดยไม่ต้องไปตรวจสอบเลเยอร์ที่เหลือ
- Auto-Expiry: ใช้ฟีเจอร์ TTL ของ DynamoDB เพื่อลบข้อมูลที่หมดอายุ (24 ชั่วโมง) อัตโนมัติ

**ฟังก์ชัน is_blacklisted(ip_address)**
  
```python
def is_blacklisted(ip_address):
    try:
        bl_key = f"BL#{ip_address}"
        response = rate_limit_table.get_item(Key={"ip_address": bl_key})
        item = response.get("Item")
        
        if not item:
            return None
        
        expires_at = int(item.get("expires_at", 0))
        if expires_at < int(time.time()):
            return None  # หมดอายุแล้ว
        
        return item.get("reason", "blacklisted")
    except Exception as e:
        print(f"Error checking blacklist: {e}")
        return None
```

**ฟังก์ชัน add_to_blacklist(ip_address, reason)**

```python
def add_to_blacklist(ip_address, reason):
    try:
        bl_key = f"BL#{ip_address}"
        now = int(time.time())
        expires_at = now + BLACKLIST_DURATION
        
        rate_limit_table.put_item(Item={
            "ip_address": bl_key,
            "blacklisted": True,
            "reason": reason,
            "banned_at": now,
            "expires_at": expires_at
        })
        print(f"[BLACKLIST] Added {ip_address} - reason: {reason}")
    except Exception as e:
        print(f"Error adding to blacklist: {e}")
```

##

### 🤖 Layer 3: User-Agent Analysis
ตรวจสอบข้อมูล User-Agent ใน Header เพื่อค้นหา Signature ของซอฟต์แวร์อัตโนมัติมาตรฐาน
- Detection: ตรวจจับคำสำคัญเช่น curl, wget, python-requests, scrapy, bot, crawler
- Case Insensitive: แปลงข้อความเป็นตัวพิมพ์เล็กทั้งหมดก่อนตรวจสอบเพื่อให้ครอบคลุมทุกรูปแบ

**ฟังก์ชัน is_bot_user_agent()**

```python
def is_bot_user_agent(user_agent):
    if not user_agent:
        return "empty_user_agent"
    
    user_agent_lower = user_agent.lower()
    
    for bot_sig in BOT_USER_AGENTS:
        if bot_sig in user_agent_lower:
            return f"bot_signature: {bot_sig}"
    
    return None
```

##

### ⏱️ Layer 4: Rate Limiting
ป้องกันการยิง Request ถี่เกินไปโดยใช้ตรรกะ Sliding Window
- Threshold: อนุญาตสูงสุด 10 Requests ต่อรอบเวลา 60 วินาที
- Stateful Tracking: บันทึกตัวนับ (Counter) และเวลาเริ่มต้นหน้าต่างลงใน DynamoDB แยกตาม IP
- Action: หากเกินกำหนดจะตอบกลับด้วยสถานะ 429 Too Many Requests

**ฟังก์ชัน check_rate_limit()**

```python
def check_rate_limit(ip_address):
    try:
        now = int(time.time())
        window_start = now - RATE_LIMIT_WINDOW
        
        response = rate_limit_table.get_item(
            Key={"ip_address": ip_address}
        )
        item = response.get("Item")
        
        if not item:
            rate_limit_table.put_item(Item={
                "ip_address": ip_address,
                "count": 1,
                "window_start": now,
                "expires_at": now + RATE_LIMIT_WINDOW * 2
            })
            return True, 1
        
        item_window_start = int(item.get("window_start", 0))
        count = int(item.get("count", 0))
        
        if item_window_start < window_start:
            rate_limit_table.put_item(Item={
                "ip_address": ip_address,
                "count": 1,
                "window_start": now,
                "expires_at": now + RATE_LIMIT_WINDOW * 2
            })
            return True, 1
        
        new_count = count + 1
        if new_count > RATE_LIMIT_MAX_REQUESTS:
            return False, new_count
        
        rate_limit_table.update_item(
            Key={"ip_address": ip_address},
            UpdateExpression="SET #c = :c",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":c": new_count}
        )
        return True, new_count
    except Exception as e:
        print(f"Error in rate limit: {e}")
        return True, 0

```

##

### 💾 Layer 5: Event Persistence
เลเยอร์สุดท้ายสำหรับ Request ที่ผ่านการทดสอบครบทุกด่าน
- Data Integrity: บันทึกข้อมูลที่สะอาดลงในตาราง ValidEvents พร้อม Request ID ที่ไม่ซ้ำกัน (UUID)
- Comprehensive Logging: เก็บข้อมูลทั้ง IP, Path, Method, User-Agent และ Body Size เพื่อใช้ในการวิเคราะห์เชิงลึก

**ฟังก์ชัน save_valid_event()**

```python
def save_valid_event(request_id, ip_address, user_agent, path, method, body_size):
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        valid_events_table.put_item(Item={
            "request_id": request_id,
            "timestamp": timestamp,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "path": path,
            "method": method,
            "body_size": body_size
        })
    except Exception as e:
        print(f"Error saving event: {e}")
```

##

### 🧠 5.2 flowchart แสดงการตัดสินใจของ Lambda BotDetector

```mermaid
flowchart TD
    A["Request Ingestion<br/>(API Gateway)"]

    B["Layer 1: Honeypot Detection"]
    C["Layer 2: IP Blacklist Enforcement"]
    D["Layer 3: User-Agent Analysis"]
    E["Layer 4: Rate Limiting<br/>(Sliding Window)"]
    F["Layer 5: Event Validation"]

    X1["Reject Request"]
    X2["Block IP (24h)"]
    X3["Reject Request"]
    X4["Throttle Request"]
    Y1["Store Valid Event<br/>(DynamoDB)"]
    Y2["Drop Event"]

    A --> B

    B -->|Matched| X1
    B -->|Pass| C

    C -->|Blacklisted| X2
    C -->|Pass| D

    D -->|Bot Signature| X3
    D -->|Pass| E

    E -->|Rate Exceeded| X4
    E -->|Pass| F

    F -->|Valid| Y1
    F -->|Invalid| Y2

```

##

### 🧪 5.3 Example Request Scenarios

**Case 1. Normal Request (Expected to Pass)**
```python
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/prod/track \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"event":"page_view"}'
```
**ผลลัพธ์:** ผ่านทุก filtering layer Event ถูก store ลง DynamoDB

##

**Case 2. Honeypot Access (Blocked Immediately)**
```python
curl https://<api-id>.execute-api.<region>.amazonaws.com/.env
```
**ผลลัพธ์:** ถูก catch ที่ Layer 1 Lambda terminate early และ ไม่มี downstream cost

##

**Case 3. Bot User-Agent (Rejected)**
```python
curl -H "User-Agent: python-requests/2.31" \
  https://<api-id>.execute-api.<region>.amazonaws.com/prod/track
```
**ผลลัพธ์:** ถูก Blocked at Layer 3 IP ยังไม่ถูก ban (behavioral vs enforcement)

##

**Case 4. Rate Limit Exceeded (Throttled)**
```python
for i in {1..20}; do
  curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/track
done
```
**ผลลัพธ์:** Throttled at Layer 4 Event ไม่เข้าสู่ persistence

---

## 📊 6. ผลการทดสอบและความแม่นยำ (Performance & Metrics)
เพื่อพิสูจน์ประสิทธิภาพของแนวคิด "The Digital Sieve" ระบบได้ผ่านการทดสอบด้วยสคริปต์จำลองทราฟฟิก (traffic_simulator.py) โดยใช้ 9 Personas (5 มนุษย์จริง และ 4 บอท) เพื่อวัดค่าความแม่นยำและความเร็วในการประมวลผล

### 6.1 ตัวบ่งชี้ประสิทธิภาพหลัก (Key Performance Indicators)

| ตัวชี้วัด (Metric) | ผลการทดสอบ (Result) | คำอธิบาย |
|------------------|-------------------|---------|
| **True Positive (TP)** | **91.3%** | ความสามารถในการตรวจจับบอทมาตรฐานได้อย่างถูกต้อง |
| **False Positive (FP)** | **14.5%** | อัตราการตรวจจับผิดพลาด (ส่วนใหญ่เกิดจากผู้ใช้จริงที่ใช้งานเร็วเกินเกณฑ์) |
| **Average Latency (p95)** | **164.7 ms** | ความหน่วงของระบบในระดับเปอร์เซ็นไทล์ที่ 95 ซึ่งอยู่ในเกณฑ์ดีเยี่ยม |
| **Operational Cost** | **~$2.00** | ต้นทุนประมาณการต่อ 1 ล้าน Requests (Pay‑as‑you‑go) |

##

### 6.2 การวิเคราะห์ด้านต้นทุน (Cost Analysis) 
- **Amazon API Gateway:** ประมาณ $1.00 ต่อ 1 ล้านครั้ง (คิดตามจำนวน API Calls จริง)
- **AWS Lambda:** ประมาณ $0.20 ต่อ 1 ล้านครั้ง (คิดตามจำนวนการประมวลผล โดยยังไม่รวมส่วนลดจาก Free Tier 1 ล้านครั้งแรก)
- **Amazon DynamoDB (On-Demand):** ประมาณ $0.25 - $1.25 แปรผันตามปริมาณการอ่านและเขียนข้อมูลจริง
- **Amazon CloudWatch:** บริหารจัดการภายใต้โควตาฟรี 5GB Log Ingestion ต่อเดือน
- **Amazon S3 Hosting:** 1GB แรกอยู่ที่ประมาณ $0.023 Free Tier (5GB)

##

### 6.3 การวิเคราะห์ความหน่วง (Latency Breakdown)
- p50 (Median): การประมวลผลส่วนใหญ่อยู่ในระดับที่รวดเร็วมาก
- p99 (Worst Case): อาจมีความหน่วงถึง 455ms ในบางกรณี ซึ่งเกิดจากอาการ Cold Start ของ Lambda ในการเรียกใช้งานครั้งแรกหลังจากหยุดพัก

---

## 🖥️ 7. ระบบแสดงผล (Real-time Dashboard)
เพื่อให้สามารถติดตามการทำงานของระบบ โครงการนี้ได้พัฒนาหน้า Dashboard ที่ดึงข้อมูลผ่าน GetStats Lambda โดยระบบจะทำการ Fetch ข้อมูลใหม่ทุกๆ 5 วินาที ดังรูป

<p align="center">
  <a href="http://bot-detection-dashboard-tharadon.s3-website-us-east-1.amazonaws.com/" target="_blank">
    <img src="Material/Dashboard.png" alt="Live Bot Detection Dashboard" width="800">
  </a>
</p>

<p align="center">
  <strong>Live Bot Detection Dashboard</strong><br>
  <em>Click the image to open the dashboard</em>
</p>

##

**โดยหน้าจอประกอบไปด้วย**
- Stats Cards: สรุปจำนวน Valid Requests, Unique Users และจำนวน IP ที่ถูก Blacklist
- Top 5 Analysis: กราฟแท่งแสดงอันดับ User-Agents และ Path ที่ถูกเรียกใช้งานบ่อยที่สุด
- Activity Logs: รายการเหตุการณ์ล่าสุด (Recent Events) 
- รายชื่อ IP ที่ติด Blacklist พร้อมเหตุผลและเวลาที่หมดอายุ

---

## ⚙️ 8. การติดตั้งและใช้งาน (Getting Started)
ส่วนนี้จะอธิบายขั้นตอนการตั้งค่าระบบเพื่อใช้งาน ทั้งในส่วนของ AWS Cloud และการรัน Traffic Simulator

### 8.1 สิ่งที่ต้องเตรียม (Prerequisites)
- บัญชีผู้ใช้งาน AWS (AWS Account)
- Python 3.9+
- AWS Credentials

##

### 8.2 การตั้งค่าบน AWS (Cloud Setup)

**Step 1: DynamoDB Tables**
- สร้างตารางชื่อ ValidEvents (Partition Key: request_id)
- สร้างตารางชื่อ RateLimitTracker (Partition Key: ip_address)
- เปิดใช้งานฟีเจอร์ TTL (Time to Live) ในตาราง RateLimitTracker โดยตั้งชื่อฟิลด์เป็น expires_at เพื่อให้ระบบลบข้อมูล Blacklist และ Counter เก่าอัตโนมัติ

**Step 2: AWS Lambda**
- สร้าง Lambda Function 2 ชุด BotDetector และ GetStats
- คัดลอกโค้ดจาก lambda_function.py และ get_stats_lambda.py ไปวางตามลำดับ
- IAM Permissions: ตั้งค่า Role ให้ Lambda มีสิทธิ์ GetItem, PutItem, UpdateItem และ Scan บนตาราง DynamoDB ทั้งสองตาราง

**Step 3: API Gateway**
- สร้าง HTTP API และตั้งค่า Route (เช่น ANY / สำหรับการตรวจจับ และ GET /stats สำหรับสถิติ)
- เชื่อมต่อ (Integrate) เข้ากับ Lambda ที่เตรียมไว้

**Step 4: S3 Dashboard**
- อัปโหลดไฟล์ dashboard.html ขึ้น S3 Bucket และเปิดใช้งาน Static Website Hosting
- อย่าลืมแก้ไขตัวแปร API_URL ในไฟล์ HTML ให้ตรงกับ URL ของ API Gateway ของคุณ

**Step 5: การรันโปรแกรมจำลอง (Local Simulation)**
สามารถทดสอบประสิทธิภาพของระบบได้ทันทีผ่าน traffic_simulator.py ซึ่งจะจำลองพฤติกรรมของ 9 Personas (5 มนุษย์จริง และ 4 บอท)
- **เปิด AWS CloudShell:** ล็อกอินเข้า AWS Console แล้วคลิกไอคอน CloudShell (รูปเทอร์มินัล >_) บริเวณแถบเมนูด้านบน
- **Upload ไฟล์:** คลิกที่เมนู Actions ในหน้าต่าง CloudShell แล้วเลือก Upload file เพื่ออัปโหลดไฟล์ traffic_simulator.py เข้าสู่ระบบคลาวด์
- **ตั้งค่าเป้าหมาย:** ใช้คำสั่งเทอร์มินัลแก้ไขค่าตัวแปร target_url ในไฟล์ให้ตรงกับ URL ของ API Gateway ที่คุณสร้างไว้ (แนะนำให้ใช้คำสั่ง nano traffic_simulator.py เพื่อแก้ไขได้ทันที)
- **เริ่มการจำลอง:** ระบบจะแสดง Log การทำงานแบบเรียลไทม์ พร้อมสีสันแยกแยะระหว่างผู้ใช้ (สีเขียว) และบอท (สีแดง)

##

### 🎥 8.3 ตัวอย่างวีดีโอแสดงการทำงานของระบบ

<p align="center">
  <a href="https://www.youtube.com/watch?v=VIDEO_ID">
    <img src="https://img.youtube.com/vi/VIDEO_ID/0.jpg" 
         alt="The Digital Sieve Demo" 
         width="640">
  </a>
</p>

<p align="center">
  <em>Click the image to watch the live demo</em>
</p>


---

## 🏛️ 9. การวิเคราะห์ตามหลัก AWS Well-Architected Framework (6 Pillars)
โครงการนี้ได้รับการออกแบบโดยยึดตามมาตรฐานสากลของ AWS เพื่อให้มั่นใจว่าระบบมีความยืดหยุ่น ปลอดภัย และมีประสิทธิภาพสูงสุด ดังนี้

**1. Operational Excellence (การดำเนินการที่เป็นเลิศ)** เน้นการจัดการระบบและการติดตามผลเพื่อให้ธุรกิจดำเนินไปได้อย่างต่อเนื่อง
- Real-time Monitoring: ใช้ CloudWatch Logs สำหรับจัดเก็บ Audit Trail เพื่อติดตามเหตุการณ์และวิเคราะห์ย้อนหลังได้ทุก Request
- Live Dashboard: หน้า Dashboard ที่อัปเดตทุก 5 วินาที เพื่อให้มองเห็นภาพรวมของระบบและพฤติกรรมบอทได้ทันที

**⭐2. Security (ความปลอดภัย)⭐** เน้นการจัดการระบบและการติดตามผลเพื่อให้ธุรกิจดำเนินไปได้อย่างต่อเนื่อง
- Ingestion Layer Filtering: การตั้งปราการด่านแรกที่ API Gateway และ Lambda ช่วยลดพื้นที่การโจมตี (Attack Surface) ของระบบหลัก
- Multi-layer Defense: ใช้การป้องกัน 5 ชั้น ตั้งแต่ Honeypot ไปจนถึง Rate Limiting เพื่อสกัดกั้นภัยคุกคามทุกรูปแบบ

**3. Reliability (ความเชื่อถือได้)** ความสามารถในการทำงานได้อย่างถูกต้องและต่อเนื่อง แม้จะมีทราฟฟิกพุ่งสูง
- High Availability: เลือกใช้ AWS Managed Services (Lambda, DynamoDB, API Gateway) ที่มีการสำรองข้อมูลและกระจายการทำงานข้าม Zone โดยอัตโนมัติ
- Auto-scaling: สถาปัตยกรรม Serverless สามารถขยายตัวรองรับ Request ที่พุ่งสูงขึ้น (Spike) ได้ถึง 1,000 Concurrent ทันทีโดยไม่ต้องตั้งค่าเพิ่ม

**4. Performance Efficiency (ประสิทธิภาพในการทำงาน)** การใช้ทรัพยากรอย่างคุ้มค่าเพื่อตอบสนองความต้องการของระบบ
- Event-driven Response: ระบบจะทำงานเฉพาะเมื่อมี Request เข้ามาเท่านั้น ทำให้ไม่มีทรัพยากรสูญเปล่าในช่วงเวลาที่ไม่มีทราฟฟิก
- Low Latency (p95): การประมวลผลทั้ง 5 เลเยอร์ใช้เวลาเฉลี่ยเพียง 164.7 มิลลิวินาที ทำให้ไม่ส่งผลกระทบต่อประสบการณ์ของผู้ใช้งานจริง
- Logic Optimization: เรียงลำดับการตรวจเช็คจาก "ประหยัดทรัพยากร" ไปหา "ใช้ทรัพยากรสูง" เพื่อลดภาระการประมวลผล

**⭐ 5. Cost Optimization (การเพิ่มประสิทธิภาพต้นทุน) ⭐** การบริหารจัดการเพื่อให้ได้ผลลัพธ์สูงสุดในราคาที่ต่ำที่สุด
- Pay-as-you-go: จ่ายเงินตามจำนวน Request จริงที่เกิดขึ้น โดยไม่มีค่าใช้จ่ายแอบแฝงในช่วงที่ไม่มีการใช้งาน (Zero Idle Cost)
- Single-table Design: ออกแบบ DynamoDB ให้เก็บข้อมูลทุกประเภทไว้ในตารางเดียว เพื่อลดค่าใช้จ่ายในการจองทรัพยากร (Read/Write Capacity)
- Downstream Savings: การบล็อกบอทตั้งแต่ต้นทางช่วยลดค่าใช้จ่ายในส่วนประมวลผล และการจัดเก็บข้อมูลของระบบหลัก

**⭐ 6. Sustainability (ความยั่งยืน) ⭐** การลดผลกระทบต่อสิ่งแวดล้อมจากการใช้พลังงานคอมพิวเตอร์
- Resource Efficiency: การใช้ Serverless ช่วยลดการใช้พลังงานในศูนย์ข้อมูลได้ดีกว่าการเปิดเซิร์ฟเวอร์ทิ้งไว้ตลอดเวลา
- Waste Traffic Mitigation: การตัด Request ที่ไม่มีมูลค่าทิ้งทันทีช่วยลดการใช้พลังงานประมวลผลข้อมูลขยะ ซึ่งเป็นส่วนสำคัญในการลด Carbon Footprint ขององค์กร

---
















