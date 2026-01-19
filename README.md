# 🎮 Tic-Tac-Toe Online (Socket Python)

Game Cờ Caro (Tic-Tac-Toe) nhiều người chơi qua mạng LAN/Localhost, được xây dựng bằng **Python**, sử dụng kỹ thuật **Socket Programming** (TCP/IP) và giao diện đồ họa **Tkinter**.

## 🚀 Tính năng nổi bật

* **Mô hình Client-Server:** Hỗ trợ nhiều cặp người chơi cùng lúc (Multi-threading).
* **Giao diện đồ họa (GUI):** Sử dụng Tkinter thân thiện, dễ sử dụng.
* **Hệ thống đăng nhập:** Người chơi nhập tên trước khi vào phòng.
* **Server Authoritative (Bảo mật):**
    * Server quản lý toàn bộ bàn cờ và logic game.
    * Server kiểm tra tính hợp lệ của nước đi và xác định người thắng (chống gian lận từ Client).
* **Xử lý ngắt kết nối:** Tự động xử thắng cho người còn lại nếu đối thủ thoát đột ngột.
* **Tính năng Rematch (Chơi lại):** Cho phép reset bàn cờ khi cả 2 người chơi cùng đồng ý mà không cần tắt ứng dụng.
* **Thông báo trạng thái:** Hiển thị lượt đi, tên đối thủ, và kết quả thắng/thua/hòa rõ ràng.

## 🛠️ Công nghệ sử dụng

* **Ngôn ngữ:** Python 3.x
* **Giao thức mạng:** TCP Sockets
* **Xử lý đa luồng:** Python `threading` module (để xử lý nhiều Client và lắng nghe tin nhắn song song với GUI).
* **Giao diện:** Tkinter (Thư viện chuẩn của Python).

## 📂 Cấu trúc dự án

```text
TicTacToe-Socket/
├── server.py       # Mã nguồn Server (Chạy trước)
├── client.py       # Mã nguồn Client (Người chơi)
└── README.md       # Tài liệu hướng dẫn
**⚙️ Hướng dẫn cài đặt và chạy**

**1. Yêu cầu hệ thống**
Đã cài đặt Python 3.x.
Không cần cài thêm thư viện ngoài (các thư viện socket, threading, tkinter đều có sẵn trong Python chuẩn).

**2. Các bước chạy game**
Bạn cần mở 3 cửa sổ Terminal (Command Prompt) riêng biệt để mô phỏng:
**Bước 1:** Khởi động Server Mở terminal đầu tiên và chạy:
python server.py
Server sẽ bắt đầu lắng nghe tại 127.0.0.1:55555.
**Bước 2:** Khởi động Client 1 (Người chơi 1) Mở terminal thứ hai và chạy:
python client.py
Nhập tên (ví dụ: Alice) và bấm "Tìm trận đấu".
Trạng thái sẽ là "Đang tìm đối thủ...".
**Bước 3:** Khởi động Client 2 (Người chơi 2) Mở terminal thứ ba và chạy:
python client.py
Nhập tên (ví dụ: Bob) và bấm "Tìm trận đấu".
Server sẽ ghép cặp Alice và Bob. Game bắt đầu!
