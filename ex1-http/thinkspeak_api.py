import requests
import json

# ====== CẤU HÌNH ======
API_KEY = "T7H40F0X82VGW7L5"
CHANNEL_ID = "1529099"
BASE_URL = f"https://api.thingspeak.com/"

# Cách 1: Gửi dữ liệu URL-encoded (qua query string)
def send_data_urlencoded(field1, field2):
    url = f"{BASE_URL}/update"
    params = {
        "api_key": API_KEY,
        "field1": field1,
        "field2": field2
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"[SUCCESS] Gửi thành công (URL encoded). Entry ID: {response.text}")
    else:
        print("[ERROR] Không gửi được:", response.status_code, response.text)

# Cách 2: Gửi dữ liệu JSON trong body
def send_data_json(field1, field2):
    url = f"{BASE_URL}/update?api_key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "field1": field1,
        "field2": field2
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"[SUCCESS] Gửi thành công (JSON body). Entry ID: {response.text}")
    else:
        print("[ERROR] Không gửi được:", response.status_code, response.text)

# Cách 3: Lấy dữ liệu mới nhất từ Channel
def get_data(results=2):
    url = f"{BASE_URL}/channels/{CHANNEL_ID}/feeds.json"
    params = {"results": results}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("\n DỮ LIỆU NHẬN VỀ:")
        feeds = data.get("feeds", [])
        for feed in feeds:
            field1 = feed.get("field1")
            field2 = feed.get("field2")
            created_at = feed.get("created_at")
            print(f"- Thời gian: {created_at}, field1 = {field1}, field2 = {field2}")
    else:
        print("[ERROR] Không lấy được dữ liệu:", response.status_code, response.text)

if __name__ == "__main__":
    print("=== GỬI DỮ LIỆU CÁCH 1: URL Encoded ===")
    send_data_urlencoded(20, 33)

    print("\n=== GỬI DỮ LIỆU CÁCH 2: JSON Body ===")
    send_data_json(25, 45)

    print("\n=== LẤY DỮ LIỆU MỚI NHẤT ===")
    get_data(results=2)
