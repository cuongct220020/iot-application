"""
Script để test API tự động
Chạy: python test_api.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """In kết quả response đẹp"""
    print(f"\n{'=' * 60}")
    print(f"🔍 {title}")
    print(f"{'=' * 60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'=' * 60}\n")


def test_sensor_apis():
    """Test các API của SensorData"""
    print("\n" + "🎯 TESTING SENSOR DATA APIs".center(60, "="))

    # 1. POST - Tạo sensor mới
    print("\n1️⃣  POST - Tạo sensor mới")
    sensor_data = {
        "sensorName": "Temperature Sensor",
        "sensorValue": 25.5
    }
    response = requests.post(f"{BASE_URL}/api/sensordata", json=sensor_data)
    print_response("POST /api/sensordata", response)

    # Lưu ID để test sau
    if response.status_code == 201:
        sensor_id = response.json()["_id"]
        print(f"✅ Đã tạo sensor với ID: {sensor_id}")
    else:
        print("❌ Tạo sensor thất bại!")
        return

    time.sleep(0.5)

    # 2. POST - Tạo thêm sensor
    print("\n2️⃣  POST - Tạo sensor thứ 2")
    sensor_data2 = {
        "sensorName": "Humidity Sensor",
        "sensorValue": 65.2
    }
    response = requests.post(f"{BASE_URL}/api/sensordata", json=sensor_data2)
    print_response("POST /api/sensordata (2)", response)

    time.sleep(0.5)

    # 3. GET - Lấy tất cả sensors
    print("\n3️⃣  GET - Lấy tất cả sensors")
    response = requests.get(f"{BASE_URL}/api/sensordata")
    print_response("GET /api/sensordata", response)

    time.sleep(0.5)

    # 4. GET - Lấy sensor theo ID
    print("\n4️⃣  GET - Lấy sensor theo ID")
    response = requests.get(f"{BASE_URL}/api/sensordata/{sensor_id}")
    print_response(f"GET /api/sensordata/{sensor_id}", response)

    time.sleep(0.5)

    # 5. PUT - Cập nhật sensor
    print("\n5️⃣  PUT - Cập nhật sensor")
    update_data = {
        "sensorName": "Temperature Sensor Updated",
        "sensorValue": 30.0
    }
    response = requests.put(f"{BASE_URL}/api/sensordata/{sensor_id}", json=update_data)
    print_response(f"PUT /api/sensordata/{sensor_id}", response)

    time.sleep(0.5)

    # 6. GET - Xác nhận đã update
    print("\n6️⃣  GET - Xác nhận đã update")
    response = requests.get(f"{BASE_URL}/api/sensordata/{sensor_id}")
    print_response(f"GET /api/sensordata/{sensor_id} (after update)", response)

    time.sleep(0.5)

    # 7. DELETE - Xóa sensor
    print("\n7️⃣  DELETE - Xóa sensor")
    response = requests.delete(f"{BASE_URL}/api/sensordata/{sensor_id}")
    print_response(f"DELETE /api/sensordata/{sensor_id}", response)

    time.sleep(0.5)

    # 8. GET - Xác nhận đã xóa (sẽ trả về 404)
    print("\n8️⃣  GET - Xác nhận đã xóa (expect 404)")
    response = requests.get(f"{BASE_URL}/api/sensordata/{sensor_id}")
    print_response(f"GET /api/sensordata/{sensor_id} (after delete)", response)


def test_user_apis():
    """Test các API của User"""
    print("\n" + "👥 TESTING USER APIs".center(60, "="))

    # 1. POST - Tạo user mới
    print("\n1️⃣  POST - Tạo user mới")
    user_data = {
        "userName": "johndoe",
        "password": "password123",
        "email": "john@example.com"
    }
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    print_response("POST /api/users", response)

    # Lưu ID
    if response.status_code == 201:
        user_id = response.json()["_id"]
        print(f"✅ Đã tạo user với ID: {user_id}")
    else:
        print("❌ Tạo user thất bại!")
        return

    time.sleep(0.5)

    # 2. GET - Lấy tất cả users
    print("\n2️⃣  GET - Lấy tất cả users")
    response = requests.get(f"{BASE_URL}/api/users")
    print_response("GET /api/users", response)

    time.sleep(0.5)

    # 3. GET - Lấy user theo ID
    print("\n3️⃣  GET - Lấy user theo ID")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}")
    print_response(f"GET /api/users/{user_id}", response)

    time.sleep(0.5)

    # 4. PUT - Cập nhật user
    print("\n4️⃣  PUT - Cập nhật user")
    update_data = {
        "userName": "johndoe_updated",
        "password": "newpassword123",
        "email": "john.new@example.com"
    }
    response = requests.put(f"{BASE_URL}/api/users/{user_id}", json=update_data)
    print_response(f"PUT /api/users/{user_id}", response)

    time.sleep(0.5)

    # 5. DELETE - Xóa user
    print("\n5️⃣  DELETE - Xóa user")
    response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
    print_response(f"DELETE /api/users/{user_id}", response)


def test_error_cases():
    """Test các trường hợp lỗi"""
    print("\n" + "⚠️  TESTING ERROR CASES".center(60, "="))

    # 1. POST với dữ liệu thiếu
    print("\n1️⃣  POST - Thiếu dữ liệu bắt buộc")
    bad_data = {"sensorName": "Test"}  # Thiếu sensorValue
    response = requests.post(f"{BASE_URL}/api/sensordata", json=bad_data)
    print_response("POST /api/sensordata (missing field)", response)

    time.sleep(0.5)

    # 2. GET với ID không tồn tại
    print("\n2️⃣  GET - ID không tồn tại")
    fake_id = "000000000000000000000000"
    response = requests.get(f"{BASE_URL}/api/sensordata/{fake_id}")
    print_response(f"GET /api/sensordata/{fake_id}", response)

    time.sleep(0.5)

    # 3. GET với ID không hợp lệ
    print("\n3️⃣  GET - ID không hợp lệ")
    bad_id = "invalid-id"
    response = requests.get(f"{BASE_URL}/api/sensordata/{bad_id}")
    print_response(f"GET /api/sensordata/{bad_id}", response)


def main():
    """Hàm chính"""
    print("\n" + "🚀 BẮT ĐẦU TEST API".center(60, "="))
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)

    try:
        # Kiểm tra server có chạy không
        print("\n🔍 Kiểm tra server...")
        response = requests.get(BASE_URL, timeout=2)
        print("✅ Server đang chạy!")

        # Test APIs
        test_sensor_apis()
        test_user_apis()
        test_error_cases()

        print("\n" + "✅ HOÀN THÀNH TẤT CẢ TESTS".center(60, "=") + "\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ LỖI: Không thể kết nối tới server!")
        print("Vui lòng chạy server trước: python main.py")
        print(f"Server cần chạy tại: {BASE_URL}\n")
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}\n")


if __name__ == "__main__":
    main()