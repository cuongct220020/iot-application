import paho.mqtt.client as mqtt
import time

# Cấu hình broker
BROKER = "localhost"
PORT = 1883

print("=" * 60)
print("KIỂM TRA KẾT NỐI MQTT BROKER")
print("=" * 60)
print(f"Broker: {BROKER}:{PORT}\n")


def test_connection():
    """Test kết nối đến broker"""

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Kết nối thành công!")
            print("Broker đang chạy bình thường")
            client.disconnect()
        else:
            print(f"Kết nối thất bại! Mã lỗi: {rc}")
            print("\nCác mã lỗi thường gặp:")
            print("  1: Connection refused - incorrect protocol version")
            print("  2: Connection refused - invalid client identifier")
            print("  3: Connection refused - server unavailable")
            print("  4: Connection refused - bad username or password")
            print("  5: Connection refused - not authorized")

    client = mqtt.Client(client_id="test_client")
    client.on_connect = on_connect

    try:
        print("Đang kết nối...")
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        time.sleep(3)
        client.loop_stop()
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        print("\nGợi ý:")
        print("  - Kiểm tra broker đã chạy chưa")
        print("  - Kiểm tra địa chỉ IP và port")
        print("  - Kiểm tra firewall")




print("Bước 1: Test kết nối cơ bản")
test_connection()

print("\n" + "=" * 60)
print("Bước 2: Hướng dẫn kiểm tra broker")
print("=" * 60)

print("""
Kiểm tra EMQX:
  - Dashboard: http://localhost:18083
  - Username: admin
  - Password: public
  - Xem: Connections, Subscriptions, Topics
""")

print("=" * 60)