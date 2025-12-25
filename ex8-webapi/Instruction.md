# 🚀 Sensor API - Sanic + MongoDB

Web API quản lý dữ liệu cảm biến và người dùng sử dụng Sanic framework và MongoDB.

## ⚡ Quick Start

### 1. Cài đặt
```bash
# Clone/tạo project
mkdir sensor-api && cd sensor-api

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Cài đặt packages
pip install sanic sanic-ext motor pymongo pyyaml
```

### 2. Tạo files
- `main.py` - Copy code từ artifact
- `openapi.yml` - Copy code từ artifact
- `requirements.txt` - Copy code từ artifact

### 3. Chạy MongoDB
```bash
# Khởi động MongoDB service
# hoặc mở MongoDB Compass
```

### 4. Chạy server
```bash
python main.py
```

### 5. Truy cập
- **Swagger UI:** http://localhost:8000/docs
- **API:** http://localhost:8000/api/sensordata

## 📋 Endpoints

### SensorData
- `GET /api/sensordata` - Lấy tất cả
- `GET /api/sensordata/{id}` - Lấy theo ID
- `POST /api/sensordata` - Tạo mới
- `PUT /api/sensordata/{id}` - Cập nhật
- `DELETE /api/sensordata/{id}` - Xóa

### Users
- `GET /api/users` - Lấy tất cả
- `GET /api/users/{id}` - Lấy theo ID
- `POST /api/users` - Tạo mới
- `PUT /api/users/{id}` - Cập nhật
- `DELETE /api/users/{id}` - Xóa

## 🧪 Test API

### Cách 1: Swagger UI
1. Mở http://localhost:8000/docs
2. Click endpoint → "Try it out"
3. Nhập data → "Execute"

### Cách 2: curl
```bash
# POST - Tạo sensor
curl -X POST http://localhost:8000/api/sensordata \
  -H "Content-Type: application/json" \
  -d '{"sensorName":"Temp","sensorValue":25.5}'

# GET - Lấy tất cả
curl http://localhost:8000/api/sensordata

# PUT - Cập nhật
curl -X PUT http://localhost:8000/api/sensordata/{id} \
  -H "Content-Type: application/json" \
  -d '{"sensorName":"Updated","sensorValue":30}'

# DELETE - Xóa
curl -X DELETE http://localhost:8000/api/sensordata/{id}
```

## 📸 Screenshots cần chụp

1. ✅ Swagger UI - Danh sách API
2. ✅ POST /api/sensordata - Request & Response
3. ✅ GET /api/sensordata - Response array
4. ✅ GET /api/sensordata/{id} - Response object
5. ✅ PUT /api/sensordata/{id} - Updated data
6. ✅ DELETE /api/sensordata/{id} - Success message
7. ✅ Tương tự cho /api/users

## 🛠️ Tech Stack

- **Sanic 23.12.1** - Python async web framework
- **MongoDB** - NoSQL database
- **Motor 3.3.2** - Async MongoDB driver
- **Sanic-Ext** - OpenAPI/Swagger integration
- **PyYAML** - YAML parser

## 📝 Cấu trúc project

```
sensor-api/
├── main.py           # API server code
├── openapi.yml       # API specification
├── requirements.txt  # Dependencies
└── venv/            # Virtual environment
```

## 🔧 Lỗi thường gặp

**MongoDB connection failed:**
```bash
# Khởi động MongoDB
sudo systemctl start mongod  # Linux
# hoặc khởi động service trên Windows
```

**Port 8000 đã được sử dụng:**
```python
# Đổi port trong main.py
app.run(port=8001)
```

**Module not found:**
```bash
pip install -r requirements.txt
```

## 📚 Docs

- Sanic: https://sanic.dev/
- MongoDB: https://www.mongodb.com/docs/
- OpenAPI: https://swagger.io/specification/

---

**Happy coding! 🎉**