# Dự án Game Cờ Tướng

## Mô tả
Dự án này là một trò chơi Cờ Tướng, được phát triển bằng Python với thư viện Pygame để xử lý giao diện người dùng (UI) và Minimax AI cho đối thủ máy. Người chơi có thể chơi với máy (PvE), chơi hai người (PvP) hoặc quan sát hai máy chơi.

## Tính năng
- Chơi Cờ Tướng giữa người chơi và máy (Player vs AI).
- Chơi hai người (Player1 vs Player2).
- Quan sát hai máy chơi (AI1 vs AI2).
- Giao diện đồ họa thân thiện với người dùng, hiển thị bàn cờ và các quân cờ.
- AI được phát triển bằng thuật toán Minimax kết hợp tối ưu bằng Alpha-Beta Pruning.
- Tích hợp các tài nguyên hình ảnh cho bàn cờ và quân cờ.
- Chức năng lưu trò chơi và undo/redo nước đi (nếu có thời gian phát triển thêm).

## Yêu cầu hệ thống
- Python 3.x
- Pygame

## Hướng dẫn cài đặt
1. Clone repo này về máy:
   ```bash
   git clone https://github.com/ngwkhai/China-Chess.git

2. Di chuyển vào thư mục dự án:
    ```bash
   cd China-Chess

3. Cài đặt các thư viện yêu cầu:
    ```bash
   pip install -r requirements.txt

## Cách chơi:
1. Chạy file main.py để khởi động trò chơi:
    ```bash
   python main.py

2. Chọn chế độ chơi từ menu chính:
- **PvE**: Người chơi đấu với máy.
- **PvP**: Hai người chơi.
- **EvE**: Quan sát hai máy chơi.

3. Sử dụng chuột để di chuyển quân cờ trên giao diện.

## Cấu trúc thư mục
    ├── game_state.py      # Quản lý trạng thái trò chơi
    ├── piece.py           # Quản lý quân cờ và nước đi hợp lệ
    ├── team.py            # Quản lý đội Đỏ và Đen
    ├── game_tree.py       # Cấu trúc cây trò chơi và AI Minimax
    ├── node.py            # Tạo các nút trong cây trò chơi
    ├── gui_utilities.py   # Quản lý giao diện người dùng
    ├── resource.py       # Tích hợp tài nguyên hình ảnh
    ├── main.py            # File khởi động chính
    └── resources/         # Thư mục chứa tài nguyên

## Cách đóng góp:
1. Tạo nhánh mới cho tính năng của bạn:
    ```bash
    git checkout -b feature/ten-tinh-nang
2. Commit các thay đổi:
    ```bash
   git commit -m "Mô tả ngắn gọn về thay đổi"
3. Đẩy nhánh của bạn lên GitHub:
    ```bash
   git push origin feature/ten-tinh-nang
4. Tạo Pull Request để review và hợp nhất vào nhánh develop.

## Giấy phép
Dự án này được phát hành dưới giấy phép MIT. Vui lòng xem file LICENSE để biết thêm chi tiết.

