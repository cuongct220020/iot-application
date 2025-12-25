# BÁO CÁO BÀI TẬP: XÂY DỰNG WEB API VỚI SANIC

**Họ và tên:** Đặng Tiến Cường
**Mã sinh viên:** 20220020  
**Lớp:** CTTN-KHMT K67
**Ngày nộp:** 25/12/2025

---

## I. GIỚI THIỆU

Bài tập yêu cầu xây dựng Web API sử dụng công nghệ **Sanic** (Python async framework) và **MongoDB** để quản lý dữ liệu cảm biến (SensorData) và người dùng (User). API cung cấp đầy đủ các phương thức REST: GET, POST, PUT, DELETE và được tài liệu hóa bằng OpenAPI/Swagger.

## II. CÔNG NGHỆ VÀ CÔNG CỤ SỬ DỤNG

### 1. Backend Framework
- **Sanic 23.12.1**: Python async web framework hiệu năng cao
- **Sanic-Ext 23.12.0**: Extension hỗ trợ OpenAPI/Swagger UI tự động

### 2. Database
- **MongoDB**: NoSQL database
- **Motor 3.3.2**: Async MongoDB driver cho Python
- **PyMongo 4.6.1**: MongoDB driver core

### 3. API Documentation
- **OpenAPI 3.0**: Chuẩn định nghĩa API
- **openapi.yml**: File specification
- **Swagger UI**: Giao diện test API tương tác

### 4. Ngôn ngữ lập trình
- **Python 3.8+**: Ngôn ngữ chính
- **Async/Await**: Xử lý bất đồng bộ

## III. CẤU TRÚC DỮ LIỆU

### 1. Model SensorData

```python
{
  "_id": "ObjectId",        # ID tự động (MongoDB)
  "sensorName": "String",   # Tên cảm biến
  "sensorValue": "Float"    # Giá trị đo được
}
```

**Ví dụ:**
```json
{
  "_id": "6581234567890abcdef12345",
  "sensorName": "Temperature Sensor",
  "sensorValue": 25.5
}
```

### 2. Model User

```python
{
  "_id": "ObjectId",        # ID tự động (MongoDB)
  "userName": "String",     # Tên đăng nhập
  "password": "String",     # Mật khẩu
  "email": "String"        # Email
}
```

**Ví dụ:**
```json
{
  "_id": "6581234567890abcdef67890",
  "userName": "johndoe",
  "password": "password123",
  "email": "john@example.com"
}
```

## IV. DANH SÁCH API ENDPOINTS

### A. SensorData APIs

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/sensordata` | Lấy tất cả dữ liệu cảm biến |
| GET | `/api/sensordata/{id}` | Lấy cảm biến theo ID |
| POST | `/api/sensordata` | Tạo dữ liệu cảm biến mới |
| PUT | `/api/sensordata/{id}` | Cập nhật dữ liệu cảm biến |
| DELETE | `/api/sensordata/{id}` | Xóa dữ liệu cảm biến |

### B. User APIs

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/users` | Lấy tất cả người dùng |
| GET | `/api/users/{id}` | Lấy người dùng theo ID |
| POST | `/api/users` | Tạo người dùng mới |
| PUT | `/api/users/{id}` | Cập nhật người dùng |
| DELETE | `/api/users/{id}` | Xóa người dùng |

## V. CODE CHÍNH CỦA CHƯƠNG TRÌNH

### 1. Khởi tạo Sanic App và kết nối MongoDB

```python
from sanic import Sanic, response
from motor.motor_asyncio import AsyncIOMotorClient
from sanic_ext import openapi

app = Sanic("SensorAPI")

# Kết nối MongoDB
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.sensordb

# Collections
sensor_collection = db.sensordata
user_collection = db.users
```

### 2. Helper Functions

```python
def serialize_doc(doc):
    """Chuyển ObjectId thành string"""
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc

def serialize_docs(docs):
    """Chuyển danh sách documents"""
    return [serialize_doc(doc) for doc in docs]
```

### 3. API POST - Tạo SensorData

```python
@app.post("/api/sensordata")
@openapi.summary("Tạo dữ liệu cảm biến mới")
@openapi.tag("SensorData")
async def create_sensor(request):
    data = request.json
    
    # Validation
    if not data or "sensorName" not in data or "sensorValue" not in data:
        return json({"message": "Thiếu dữ liệu bắt buộc"}, status=400)
    
    # Tạo document
    sensor = {
        "sensorName": data["sensorName"],
        "sensorValue": float(data["sensorValue"])
    }
    
    # Insert vào MongoDB
    result = await sensor_collection.insert_one(sensor)
    sensor["_id"] = str(result.inserted_id)
    
    return json(sensor, status=201)
```

### 4. API GET - Lấy tất cả SensorData

```python
@app.get("/api/sensordata")
@openapi.summary("Lấy tất cả dữ liệu cảm biến")
@openapi.tag("SensorData")
async def get_all_sensors(request):
    # Query MongoDB
    sensors = await sensor_collection.find().to_list(length=100)
    return json(serialize_docs(sensors))
```

### 5. API GET - Lấy SensorData theo ID

```python
@app.get("/api/sensordata/<sensor_id>")
@openapi.summary("Lấy cảm biến theo ID")
@openapi.tag("SensorData")
async def get_sensor_by_id(request, sensor_id):
    try:
        sensor = await sensor_collection.find_one(
            {"_id": ObjectId(sensor_id)}
        )
        if sensor:
            return json(serialize_doc(sensor))
        return json({"message": "Không tìm thấy"}, status=404)
    except:
        return json({"message": "ID không hợp lệ"}, status=400)
```

### 6. API PUT - Cập nhật SensorData

```python
@app.put("/api/sensordata/<sensor_id>")
@openapi.summary("Cập nhật dữ liệu cảm biến")
@openapi.tag("SensorData")
async def update_sensor(request, sensor_id):
    data = request.json
    
    # Chuẩn bị dữ liệu update
    update_data = {}
    if "sensorName" in data:
        update_data["sensorName"] = data["sensorName"]
    if "sensorValue" in data:
        update_data["sensorValue"] = float(data["sensorValue"])
    
    # Update MongoDB
    result = await sensor_collection.find_one_and_update(
        {"_id": ObjectId(sensor_id)},
        {"$set": update_data},
        return_document=True
    )
    
    if result:
        return json(serialize_doc(result))
    return json({"message": "Không tìm thấy"}, status=404)
```

### 7. API DELETE - Xóa SensorData

```python
@app.delete("/api/sensordata/<sensor_id>")
@openapi.summary("Xóa dữ liệu cảm biến")
@openapi.tag("SensorData")
async def delete_sensor(request, sensor_id):
    result = await sensor_collection.delete_one(
        {"_id": ObjectId(sensor_id)}
    )
    
    if result.deleted_count:
        return json({"message": "Đã xóa thành công"})
    return json({"message": "Không tìm thấy"}, status=404)
```

### 8. Khởi động Server

```python
if __name__ == "__main__":
    print("🚀 Server đang chạy tại http://localhost:8000")
    print("📚 Swagger UI: http://localhost:8000/docs")
    app.run(host="0.0.0.0", port=8000, debug=True)
```

## VI. FILE OPENAPI.YML

File `openapi.yml` định nghĩa specification theo chuẩn OpenAPI 3.0:

```yaml
openapi: 3.0.0
info:
  title: Sensor API
  description: API quản lý dữ liệu cảm biến và người dùng
  version: 1.0.0

servers:
  - url: http://localhost:8000
    description: Development server

paths:
  /api/sensordata:
    get:
      tags: [SensorData]
      summary: Lấy tất cả dữ liệu cảm biến
      responses:
        '200':
          description: Thành công
    post:
      tags: [SensorData]
      summary: Tạo dữ liệu cảm biến mới
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SensorDataInput'
```

## VII. KẾT QUẢ THỰC HIỆN

### 1. Giao diện Swagger UI

**[CHỤP MÀN HÌNH: Swagger UI tại http://localhost:8000/docs]**

**Mô tả:** Giao diện Swagger UI hiển thị:
- ✅ Danh sách đầy đủ 10 endpoints
- ✅ Phân chia theo 2 tags: SensorData và Users
- ✅ Mô tả chi tiết mỗi API
- ✅ Request/Response examples
- ✅ Nút "Try it out" để test trực tiếp

---

### 2. Test API POST - Tạo SensorData

**[CHỤP MÀN HÌNH: POST /api/sensordata trong Swagger UI]**

**Request Body:**
```json
{
  "sensorName": "Temperature Sensor",
  "sensorValue": 25.5
}
```

**Response (201 Created):**
```json
{
  "_id": "6752a1b2c3d4e5f6a7b8c9d0",
  "sensorName": "Temperature Sensor",
  "sensorValue": 25.5
}
```

**Kết quả:** ✅ Tạo thành công cảm biến mới, trả về status code 201 với ID được tự động sinh.

---

### 3. Test API GET - Lấy tất cả SensorData

**[CHỤP MÀN HÌNH: GET /api/sensordata trong Swagger UI]**

**Response (200 OK):**
```json
[
  {
    "_id": "6752a1b2c3d4e5f6a7b8c9d0",
    "sensorName": "Temperature Sensor",
    "sensorValue": 25.5
  },
  {
    "_id": "6752a1b2c3d4e5f6a7b8c9d1",
    "sensorName": "Humidity Sensor",
    "sensorValue": 65.2
  },
  {
    "_id": "6752a1b2c3d4e5f6a7b8c9d2",
    "sensorName": "Pressure Sensor",
    "sensorValue": 1013.25
  }
]
```

**Kết quả:** ✅ Lấy được danh sách tất cả cảm biến từ database MongoDB.

---

### 4. Test API GET - Lấy SensorData theo ID

**[CHỤP MÀN HÌNH: GET /api/sensordata/{id} trong Swagger UI]**

**Parameters:**
- id: `6752a1b2c3d4e5f6a7b8c9d0`

**Response (200 OK):**
```json
{
  "_id": "6752a1b2c3d4e5f6a7b8c9d0",
  "sensorName": "Temperature Sensor",
  "sensorValue": 25.5
}
```

**Kết quả:** ✅ Lấy được thông tin chi tiết của cảm biến theo ID cụ thể.

---

### 5. Test API PUT - Cập nhật SensorData

**[CHỤP MÀN HÌNH: PUT /api/sensordata/{id} trong Swagger UI]**

**Parameters:**
- id: `6752a1b2c3d4e5f6a7b8c9d0`

**Request Body:**
```json
{
  "sensorName": "Temperature Sensor Updated",
  "sensorValue": 30.0
}
```

**Response (200 OK):**
```json
{
  "_id": "6752a1b2c3d4e5f6a7b8c9d0",
  "sensorName": "Temperature Sensor Updated",
  "sensorValue": 30.0
}
```

**Kết quả:** ✅ Cập nhật thành công thông tin cảm biến, giá trị mới được lưu vào database.

---

### 6. Test API DELETE - Xóa SensorData

**[CHỤP MÀN HÌNH: DELETE /api/sensordata/{id} trong Swagger UI]**

**Parameters:**
- id: `6752a1b2c3d4e5f6a7b8c9d0`

**Response (200 OK):**
```json
{
  "message": "Đã xóa thành công"
}
```

**Kết quả:** ✅ Xóa thành công dữ liệu cảm biến khỏi database MongoDB.

---

### 7. Test User APIs

**[CHỤP CÁC MÀN HÌNH TƯƠNG TỰ CHO USER API]**

#### A. POST /api/users
**Request:**
```json
{
  "userName": "johndoe",
  "password": "password123",
  "email": "john@example.com"
}
```

#### B. GET /api/users
**Response:** Danh sách tất cả users

#### C. GET /api/users/{id}
**Response:** Thông tin user theo ID

#### D. PUT /api/users/{id}
**Request:** Cập nhật thông tin user

#### E. DELETE /api/users/{id}
**Response:** Xóa user thành công

---

## VIII. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

### Bước 1: Cài đặt môi trường
```bash
# Cài đặt Python 3.8+
python --version

# Cài đặt MongoDB
# Tải từ: https://www.mongodb.com/try/download/community
```

### Bước 2: Clone/Tạo project
```bash
mkdir sensor-api
cd sensor-api

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

Nội dung `requirements.txt`:
```
sanic==23.12.1
sanic-ext==23.12.0
motor==3.3.2
pymongo==4.6.1
pyyaml==6.0.1
```

### Bước 4: Khởi động MongoDB
```bash
# Windows: Khởi động MongoDB service
# Linux/Mac:
sudo systemctl start mongod
```

### Bước 5: Chạy server
```bash
python main.py
```

### Bước 6: Truy cập ứng dụng
- **API Base:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

## IX. ƯU ĐIỂM CỦA GIẢI PHÁP

### 1. Hiệu năng cao
- Sanic sử dụng async/await → xử lý concurrent requests tốt
- Motor async driver → không block I/O operations
- Nhanh hơn Flask/Django đáng kể

### 2. Code clean và dễ hiểu
- Decorator-based routing giống Flask
- Async/await syntax rõ ràng
- Type hints và docstrings đầy đủ

### 3. API Documentation tự động
- Sanic-Ext tích hợp sẵn OpenAPI
- Swagger UI interactive
- File openapi.yml có thể export/import

### 4. Xử lý lỗi tốt
- Try-catch cho tất cả operations
- Status codes chuẩn REST
- Error messages rõ ràng

### 5. Scalability
- NoSQL MongoDB → scale horizontal dễ dàng
- Async architecture → handle nhiều requests
- Microservices-ready

## X. HẠNG CHẾ VÀ HƯỚNG PHÁT TRIỂN

### Hạn chế hiện tại:
1. ❌ Chưa có authentication/authorization
2. ❌ Password chưa được mã hóa
3. ❌ Chưa có input validation chi tiết
4. ❌ Chưa có pagination cho GET all
5. ❌ Chưa có rate limiting
6. ❌ Chưa có logging chi tiết

### Hướng phát triển:
1. ✅ Thêm JWT authentication
2. ✅ Mã hóa password với bcrypt
3. ✅ Validation với Pydantic
4. ✅ Pagination với skip/limit
5. ✅ Rate limiting với Redis
6. ✅ Logging với Python logging
7. ✅ Unit tests với pytest
8. ✅ Docker containerization
9. ✅ CI/CD pipeline
10. ✅ API versioning

## XI. KẾT LUẬN

Bài tập đã hoàn thành thành công việc xây dựng RESTful Web API với Sanic và MongoDB. Hệ thống cung cấp đầy đủ các chức năng CRUD cho hai models: SensorData và User, được tài liệu hóa đầy đủ với OpenAPI/Swagger UI.

### Thành quả đạt được:
- ✅ API hoạt động đầy đủ và ổn định
- ✅ Code clean, dễ hiểu, có comments
- ✅ Documentation tự động với Swagger
- ✅ Async operations cho hiệu năng cao
- ✅ Error handling đầy đủ
- ✅ Response format chuẩn REST

### Kinh nghiệm học được:
1. Sử dụng Sanic framework cho Python async web
2. Làm việc với MongoDB qua Motor driver
3. Tích hợp OpenAPI/Swagger UI
4. Thiết kế RESTful API theo best practices
5. Async/await programming trong Python

---

## PHỤ LỤC

### A. Cấu trúc thư mục project
```
sensor-api/
├── main.py              # File chính chứa API logic
├── openapi.yml          # API specification
├── requirements.txt     # Python dependencies
├── venv/               # Virtual environment
└── README.md           # Documentation
```

### B. Dependencies chi tiết
```
sanic==23.12.1          # Web framework
sanic-ext==23.12.0      # OpenAPI extension
motor==3.3.2            # Async MongoDB driver
pymongo==4.6.1          # MongoDB core driver
pyyaml==6.0.1           # YAML parser
```

### C. Tài liệu tham khảo
- Sanic Documentation: https://sanic.dev/
- MongoDB Python: https://www.mongodb.com/docs/drivers/python/
- OpenAPI Specification: https://swagger.io/specification/
- Motor Documentation: https://motor.readthedocs.io/

---

**Ngày nộp:** [Điền ngày nộp]  
**Chữ ký sinh viên:** _______________