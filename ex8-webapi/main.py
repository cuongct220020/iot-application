from sanic import Sanic, response
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sanic_ext import openapi
import yaml

app = Sanic("SensorAPI")

# Cấu hình CORS
app.config.CORS_ORIGINS = "*"

# Kết nối MongoDB
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.sensordb

# Collections
sensor_collection = db.sensordata
user_collection = db.users


# Helper function để convert ObjectId
def serialize_doc(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc


def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]


# ==================== SENSOR DATA APIs ====================

@app.get("/api/sensordata")
@openapi.summary("Lấy tất cả dữ liệu cảm biến")
@openapi.tag("SensorData")
@openapi.response(200, {"application/json": list})
async def get_all_sensors(request):
    """Lấy danh sách tất cả các cảm biến"""
    sensors = await sensor_collection.find().to_list(length=100)
    return json(serialize_docs(sensors))


@app.get("/api/sensordata/<sensor_id>")
@openapi.summary("Lấy cảm biến theo ID")
@openapi.tag("SensorData")
@openapi.parameter("sensor_id", str, "path")
@openapi.response(200, {"application/json": object})
@openapi.response(404, {"application/json": {"message": str}})
async def get_sensor_by_id(request, sensor_id):
    """Lấy thông tin cảm biến theo ID"""
    try:
        sensor = await sensor_collection.find_one({"_id": ObjectId(sensor_id)})
        if sensor:
            return json(serialize_doc(sensor))
        return json({"message": "Không tìm thấy cảm biến"}, status=404)
    except:
        return json({"message": "ID không hợp lệ"}, status=400)


@app.post("/api/sensordata")
@openapi.summary("Tạo dữ liệu cảm biến mới")
@openapi.tag("SensorData")
@openapi.body({"application/json": {
    "sensorName": str,
    "sensorValue": float
}})
@openapi.response(201, {"application/json": object})
async def create_sensor(request):
    """Tạo cảm biến mới"""
    data = request.json

    if not data or "sensorName" not in data or "sensorValue" not in data:
        return json({"message": "Thiếu dữ liệu bắt buộc"}, status=400)

    sensor = {
        "sensorName": data["sensorName"],
        "sensorValue": float(data["sensorValue"])
    }

    result = await sensor_collection.insert_one(sensor)
    sensor["_id"] = str(result.inserted_id)

    return json(sensor, status=201)


@app.put("/api/sensordata/<sensor_id>")
@openapi.summary("Cập nhật dữ liệu cảm biến")
@openapi.tag("SensorData")
@openapi.parameter("sensor_id", str, "path")
@openapi.body({"application/json": {
    "sensorName": str,
    "sensorValue": float
}})
@openapi.response(200, {"application/json": object})
async def update_sensor(request, sensor_id):
    """Cập nhật thông tin cảm biến"""
    try:
        data = request.json

        if not data:
            return json({"message": "Không có dữ liệu để cập nhật"}, status=400)

        update_data = {}
        if "sensorName" in data:
            update_data["sensorName"] = data["sensorName"]
        if "sensorValue" in data:
            update_data["sensorValue"] = float(data["sensorValue"])

        result = await sensor_collection.find_one_and_update(
            {"_id": ObjectId(sensor_id)},
            {"$set": update_data},
            return_document=True
        )

        if result:
            return json(serialize_doc(result))
        return json({"message": "Không tìm thấy cảm biến"}, status=404)
    except:
        return json({"message": "ID không hợp lệ"}, status=400)


@app.delete("/api/sensordata/<sensor_id>")
@openapi.summary("Xóa dữ liệu cảm biến")
@openapi.tag("SensorData")
@openapi.parameter("sensor_id", str, "path")
@openapi.response(200, {"application/json": {"message": str}})
async def delete_sensor(request, sensor_id):
    """Xóa cảm biến"""
    try:
        result = await sensor_collection.delete_one({"_id": ObjectId(sensor_id)})

        if result.deleted_count:
            return json({"message": "Đã xóa thành công"})
        return json({"message": "Không tìm thấy cảm biến"}, status=404)
    except:
        return json({"message": "ID không hợp lệ"}, status=400)


# ==================== USER APIs ====================

@app.get("/api/users")
@openapi.summary("Lấy tất cả người dùng")
@openapi.tag("Users")
@openapi.response(200, {"application/json": list})
async def get_all_users(request):
    """Lấy danh sách tất cả người dùng"""
    users = await user_collection.find().to_list(length=100)
    return json(serialize_docs(users))


@app.get("/api/users/<user_id>")
@openapi.summary("Lấy người dùng theo ID")
@openapi.tag("Users")
@openapi.parameter("user_id", str, "path")
@openapi.response(200, {"application/json": object})
async def get_user_by_id(request, user_id):
    """Lấy thông tin người dùng theo ID"""
    try:
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return json(serialize_doc(user))
        return json({"message": "Không tìm thấy người dùng"}, status=404)
    except:
        return json({"message": "ID không hợp lệ"}, status=400)


@app.post("/api/users")
@openapi.summary("Tạo người dùng mới")
@openapi.tag("Users")
@openapi.body({"application/json": {
    "userName": str,
    "password": str,
    "email": str
}})
@openapi.response(201, {"application/json": object})
async def create_user(request):
    """Tạo người dùng mới"""
    data = request.json

    if not data or "userName" not in data or "password" not in data or "email" not in data:
        return json({"message": "Thiếu dữ liệu bắt buộc"}, status=400)

    user = {
        "userName": data["userName"],
        "password": data["password"],
        "email": data["email"]
    }

    result = await user_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)

    return json(user, status=201)


@app.put("/api/users/<user_id>")
@openapi.summary("Cập nhật người dùng")
@openapi.tag("Users")
@openapi.parameter("user_id", str, "path")
@openapi.body({"application/json": {
    "userName": str,
    "password": str,
    "email": str
}})
@openapi.response(200, {"application/json": object})
async def update_user(request, user_id):
    """Cập nhật thông tin người dùng"""
    try:
        data = request.json

        if not data:
            return json({"message": "Không có dữ liệu để cập nhật"}, status=400)

        update_data = {}
        if "userName" in data:
            update_data["userName"] = data["userName"]
        if "password" in data:
            update_data["password"] = data["password"]
        if "email" in data:
            update_data["email"] = data["email"]

        result = await user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True
        )

        if result:
            return json(serialize_doc(result))
        return json({"message": "Không tìm thấy người dùng"}, status=404)
    except:
        return json({"message": "ID không hợp lệ"}, status=400)


@app.delete("/api/users/<user_id>")
@openapi.summary("Xóa người dùng")
@openapi.tag("Users")
@openapi.parameter("user_id", str, "path")
@openapi.response(200, {"application/json": {"message": str}})
async def delete_user(request, user_id):
    """Xóa người dùng"""
    try:
        result = await user_collection.delete_one({"_id": ObjectId(user_id)})

        if result.deleted_count:
            return json({"message": "Đã xóa thành công"})
        return json({"message": "Không tìm thấy người dùng"}, status=404)
    except:
        return json({"message": "ID không hợp lệ"}, status=400)


# ==================== ROOT ====================

@app.get("/")
async def index(request):
    """Trang chủ"""
    return json({
        "message": "Sensor API Server",
        "swagger": "/docs",
        "endpoints": {
            "sensordata": "/api/sensordata",
            "users": "/api/users"
        }
    })


if __name__ == "__main__":
    print("🚀 Server đang chạy tại http://localhost:8000")
    print("📚 Swagger UI: http://localhost:8000/docs")
    app.run(host="0.0.0.0", port=8000, debug=True)