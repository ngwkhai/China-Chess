# Dự án Game Cờ Tướng

## Mô tả
Dự án này là một trò chơi Cờ Tướng, được phát triển bằng Python với thư viện Pygame để xử lý giao diện người dùng (UI) và Minimax AI cho đối thủ máy. Người chơi có thể chơi với máy (PvE), chơi hai người (PvP), hoặc quan sát hai máy chơi (EvE). Trò chơi hiện hỗ trợ ba kiểu AI khác nhau, bao gồm AI Minimax cơ bản, Dynamic Minimax, và Deepening Minimax.

### Tính năng mới:
- **Dynamic Minimax**: Một biến thể tối ưu của Minimax, thay đổi chiều sâu tìm kiếm dựa trên trạng thái hiện tại của trò chơi.
- **Deepening Minimax**: Sử dụng kỹ thuật iterative deepening để tìm kiếm chiều sâu tốt nhất cho mỗi nước đi, giúp AI linh hoạt và thông minh hơn trong việc ra quyết định.

## Tính năng
- Chơi Cờ Tướng giữa người chơi và máy (Player vs AI).
- Chơi hai người (Player1 vs Player2).
- Quan sát hai máy chơi (AI1 vs AI2).
- Giao diện đồ họa thân thiện với người dùng, hiển thị bàn cờ và các quân cờ.
- AI sử dụng các thuật toán:
  - **Minimax** kết hợp với **Alpha-Beta Pruning**.
  - **Dynamic Minimax**: Tối ưu độ sâu tìm kiếm dựa trên tình trạng của bàn cờ.
  - **Deepening Minimax**: Sử dụng iterative deepening để đảm bảo nước đi chính xác trong thời gian cho phép.
- Tích hợp tài nguyên hình ảnh cho bàn cờ và quân cờ.
- Chức năng lưu trò chơi và undo/redo nước đi (nếu có thời gian phát triển thêm).

## Yêu cầu hệ thống
- Python 3.x
- Pygame

## Hướng dẫn cài đặt
1. Clone repo này về máy:
    ```bash
    git clone https://github.com/ngwkhai/China-Chess.git
    ```

2. Di chuyển vào thư mục dự án:
    ```bash
    cd China-Chess
    ```

3. Cài đặt các thư viện yêu cầu:
    ```bash
    pip install -r requirements.txt
    ```

## Cách chơi
1. Chạy file `main.py` để khởi động trò chơi:
    ```bash
    python main.py
    ```

2. Chọn chế độ chơi từ menu chính:
   - **PvE**: Người chơi đấu với máy.
   - **PvP**: Hai người chơi đấu với nhau.
   - **EvE**: Quan sát hai máy chơi.

3. Chọn AI cho đối thủ máy:
   - **Minimax**: AI cơ bản sử dụng thuật toán Minimax với Alpha-Beta Pruning.
   - **Dynamic Minimax**: AI sử dụng Minimax động, thay đổi độ sâu tìm kiếm theo tình hình bàn cờ.
   - **Deepening Minimax**: AI sử dụng kỹ thuật iterative deepening để chọn độ sâu tìm kiếm phù hợp.

4. Sử dụng chuột để di chuyển quân cờ trên giao diện.

## Cấu trúc thư mục
    ├── game_state.py      # Quản lý trạng thái trò chơi
    ├── piece.py           # Quản lý quân cờ và nước đi hợp lệ
    ├── team.py            # Quản lý đội Đỏ và Đen
    ├── game_tree.py       # Cấu trúc cây trò chơi và AI Minimax
    ├── node.py            # Tạo các nút trong cây trò chơi
    ├── gui_utilities.py   # Quản lý giao diện người dùng
    ├── resource.py        # Tích hợp tài nguyên hình ảnh
    ├── main.py            # File khởi động chính
    └── resources/         # Thư mục chứa tài nguyên

## Cách đóng góp
1. Tạo nhánh mới cho tính năng của bạn:
    ```bash
    git checkout -b feature/ten-tinh-nang
    ```
2. Commit các thay đổi:
    ```bash
    git commit -m "Mô tả ngắn gọn về thay đổi"
    ```
3. Đẩy nhánh của bạn lên GitHub:
    ```bash
    git push origin feature/ten-tinh-nang
    ```
4. Tạo Pull Request để review và hợp nhất vào nhánh develop.

## Giấy phép
Dự án này được phát hành dưới giấy phép MIT. Vui lòng xem file LICENSE để biết thêm chi tiết.
