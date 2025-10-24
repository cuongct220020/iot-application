# Bài 1. Giao tiếp sử dụng HTTP API

**Sinh viên:** Đặng Tiến Cường
**MSSV:** 20220020

## Yêu cầu
Viết chương trình (bằng ngôn ngữ tùy ý: C#, Java, python) thực hiện:

a) Gửi dữ liệu gồm 2 trường `field1`, `field2` lên Thinkspeak qua API theo 2 cách:

**Cách 1: Các trường `field1`, `field2` được đóng gói trong URL (urlencoded)**

```
GET https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5&field1=20&field2=33
```

**Cách 2: Các trường `field1`, `field2` được đóng gói trong body request bằng JSON.**

```
GET https://api.thingspeak.com/update?api_key=T7H40F0X82VGW7L5
```

Ví dụ: body request.

```json
{
  "field1": 20,
  "field2": 33
}
```

b) Lấy dữ liệu về từ Thingspeak API

```
GET https://api.thingspeak.com/channels/1529099/feeds.json?results=2
```

Parsing dữ liệu gửi về để lấy ra 2 trường `field1` (temperature) và `field2` (humidity) và hiển thị ra màn hình.

## Lập trình với API

*(This section refers to the Python code example and console output shown in the original PDF, which demonstrates how to implement the above requirements.)*