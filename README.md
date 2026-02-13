# ĐỒ ÁN GAME WORDLE

**Sinh viên thực hiện:** Trần Hoàng Huy Anh  
**Trường:** Đại học Khoa học Tự nhiên, ĐHQG-HCM (HCMUS)  
**Thời gian thực hiện:** 01/01/2026 - 11/02/2026

---

## 1. Giới thiệu
Wordle là một trò chơi dựa trên web. Người chơi có sáu lần thử để đoán một từ gồm năm chữ cái, với phản hồi được cung cấp cho mỗi lần đoán dưới dạng các ô màu thể hiện khi chữ cái trùng hoặc nằm đúng vị trí.
Đồ án này là một phiên bản mô phỏng lại trò chơi Wordle nổi tiếng, được viết bằng ngôn ngữ **Python** và thư viện **Pygame**. 
Trò chơi bao gồm đầy đủ các chức năng cơ bản, các tính năng nâng cao và các chức năng mở rộng.

## 2. Hướng dẫn Cài đặt & Chạy chương trình

### Yêu cầu hệ thống

* Python 3.x
* Thư viện Pygame (Phiên bản khuyến nghị: 2.6.1)

### Các bước cài đặt
1.  Giải nén thư mục đồ án.
2.  Mở Terminal (hoặc Command Prompt) tại thư mục chứa mã nguồn.
3.  Cài đặt thư viện nếu chưa có:    
Copy lệnh này 
```bash
pip install pygame==2.6.1

```
4.Chạy trò chơi:
* Dùng cmd trong thư mục chứa file và copy lệnh này:
```bash
python main.py
```
* Nếu xài IDE như VS Code thì mở và run file main.

## 3. Cấu trúc Thư mục & Mã nguồn
* **`dictionary_vi.json`**: Từ điển Tiếng Việt.
* **`filtered-wordle-words.csv`**: File tổng hợp từ trong Wordle bản gốc.
* **`make_word_list.py`**: Chạy 1 lần để đọc word list từ 2 file từ vựng và ghi vô 2 file word_list.
* **`main.py`**: File chính để chạy chương trình, xử lý vòng lặp game và các sự kiện (Events).
* **`player.py`**: Định nghĩa class `Player`, quản lý toàn bộ dữ liệu của phiên chơi.
* **`graphics.py`**: Quản lý việc vẽ giao diện (UI), xử lý hình ảnh, màu sắc và font chữ.
* **`data_structure.py`**: Cài đặt cấu trúc dữ liệu Stack (dùng cho Undo/Redo và quản lý màn hình).
* **`word_list.py`**: Chứa kho từ vựng tiếng Anh cho trò chơi.
* **`word_list_vn.py`**: Chứa kho từ vựng tiếng Việt cho trò chơi.
* **`Game_image/`**: Thư mục chứa các tài nguyên hình ảnh (icon, nút bấm).
* **`data.json`**: File lưu trữ dữ liệu trò chơi.

## 4. Game Workflow (Luồng đi của trò chơi)
1.  **MENU**: Màn hình chính.
    * *New Game* -> **INPUT_NAME**.
    * *Top-20* ->  **TOP_20**.
    * *Resume* -> Khôi phục ván chơi gần nhất -> **PLAYING**.
    * *Save Slots* -> **SAVE_SLOTS**.
    * *Setting* -> **SETTING**.
    * *How to Play* -> **HOW_TO_PLAY**.

2.  **PLAYING**: Màn hình chơi game chính.
    * Nhập từ -> Kiểm tra đúng/sai -> Cập nhật màu sắc.
    * Thắng/Thua -> Chuyển sang **END_ROUND**.
    * Nhấn ESC -> Chuyển sang **WANT_TO_SAVE** (Hỏi lưu Slot hay Resume).

3.  **END_ROUND**: Kết thúc một vòng đấu.
    * *New Round* -> Tiếp tục chơi (Cộng dồn điểm/thời gian).
    * *Stop Here* -> Kết thúc -> Chuyển sang **FINISHED**.
    * Thua (Hết lượt) -> Tự động xóa Save Slot -> Chuyển sang **FINISHED**.

## 5. Bảng Tự Đánh Giá
| STT | Chức năng | Yêu cầu chi tiết | Mức độ hoàn thiện | Ghi chú thực hiện |
| :-- | :--- | :--- | :---: | :--- |
| **1** | **Màn hình bắt đầu** | | **100%** | |
| 1.1 | New Game | Nhập tên, kiểm tra trùng lặp trong Top-20. | 100% | Đã xử lý logic check trùng tên. |
| 1.2 | Top-20 List | Hiển thị danh sách, sắp xếp theo thời gian trung bình tăng dần. | 100% | Sử dụng thuật toán sắp xếp Bubble Sort khi cập nhật list. |
| 1.3 | Resume | Cho phép chơi tiếp ván đang dang dở (nút mờ đi nếu không có). | 100% | Tự động load lại trạng thái bàn cờ, màu sắc, thời gian. |
| **2** | **Màn hình chính** | | **100%** | |
| 2.1 | Gameplay | Logic đoán từ, tô màu (Xanh, Vàng, Xám). | 100% | Đã xử lý các trường hợp từ không hợp lệ, tự động |
| 2.2 | Game Settings | Cấu hình trò chơi. | 100% | |
| - | *Chế độ chơi* | Giới hạn thời gian và số lần chơi. | 100% | Đã cài đặt Cooldown Mode (Giới hạn thời gian chờ giữa các lần chơi). |
| - | *Bảng ký tự* | Tắt/Mở bảng phím ảo. | 100% | Có nút switch bật tắt trong Setting. |
| - | *Mode ngôn ngữ* | Chuyển chế độ VI/EN | 100% | Thêm nút chuyển ở MENU, mỗi chế độ lưu data (top 20, resume, save slot) khác nhau. |
| 2.3 | Undo/Redo | Cho phép đi lại bước đoán (trước khi Enter). | 100% | Sử dụng cấu trúc dữ liệu Stack |
| **3** | **Chức năng mở rộng** | | **100%** | |
| 3.1 | Mã hóa dữ liệu | Mã hóa file save để tránh gian lận. | 100% | Sử dụng thuật toán XOR kết hợp ghi file Binary (`wb/rb`). |
| 3.2 | Save Slots | Hỗ trợ 5 slot lưu trữ khác nhau. | 100% | Cho phép chọn Slot để lưu và chơi tiếp từ Slot cụ thể. |
| 3.3 | How To Play | Màn hình hướng dẫn chơi. | 100% | Lấy ý tưởng từ trò chơi gốc |
| 3.4 | Dark Mode / Light Mode. | 100% | Có nút switch bật tắt trong Setting. |

**Tổng kết mức độ hoàn thành:** 100% yêu cầu cơ bản + 100% yêu cầu mở rộng.

## 6. Các nguồn tham khảo (References)
- Word list Tiếng Anh: https://wordslibrary.com/wordle-dictionary-words/
- Word list Tiếng Việt: https://github.com/minhqnd/wordle-vietnamese/blob/main/lib/dictionary_vi.json

- Ảnh icon VN: https://uxwing.com/vietnam-flag-round-circle-icon/
- Ảnh icon UK: https://commons.wikimedia.org/wiki/File:United-kingdom_flag_icon_round.svg
- Ảnh game setting: https://www.istockphoto.com/vector/settings-vector-icon-isolated-on-transparent-background-settings-transparency-logo-gm1042664786-279141084
- Ảnh undo: https://creazilla.com/nodes/3206468-undo-icon
- Ảnh nút switch: https://www.vecteezy.com/vector-art/24208744-switch-button-or-turn-on-turn-off-power
- Ảnh nút mũi tên trái: http://pluspng.com/left-arrow-png-1200.html

- Cách dùng encode/decode để chuyển sang file nhị phân: https://mojoauth.com/character-encoding-decoding/utf-8-encoding--python#encoding-with-utf-8-in-python

- Thuật toán xor cipher: 
- https://www.geeksforgeeks.org/search/?gq=encrypt+python
- https://www.geeksforgeeks.org/python/encrypt-using-xor-cipher-with-repeating-key/	
- https://www.geeksforgeeks.org/dsa/xor-cipher/

- Tạo/lưu file json: 
- https://realpython.com/python-json/#convert-python-dictionaries-to-json

- cách dùng thư viện time: https://quantrimang.com/hoc/module-time-trong-python-165222#mcetoc_1dfpm2eda0

- các source code game wordle đã tham khảo:
- https://github.com/MikhaD/wordle (tham khảo giao diện và cách chuyển chế độ)
- https://github.com/baraltech/Wordle-PyGame
- https://github.com/agr17/pygame-wordle/blob/main/src/wordle.py
- https://www.freecodecamp.org/news/how-to-build-a-wordle-clone-using-python-and-rich/
- https://github.com/minhqnd/wordle-vietnamese
- https://wordle.global/vi

- Tham khảo cách sử dụng Pygame
- Pygame Tutorial for Beginners - Python Game Development Course by freeCodeCamp.org: https://youtu.be/FfWpgLFMI7w?si=jdbfh3JLnOUYORN7
- The ultimate introduction to Pygame by Clear Code: https://www.youtube.com/watch?v=AY9MnQ4x3zk
Và các reference khác nằm trong source code của đồ án này

## 7. Lưu ý cho người chơi
* File `data.json` là file chứa dữ liệu của game, tự động tạo nếu không có
* Nếu muốn reset toàn bộ dữ liệu về ban đầu thì phải xóa file `data.json`.
* Nếu người chơi load game từ **Slot 1**, khi lưu lại game sẽ tự động ghi đè vào **Slot 1** (trừ khi người chơi chủ động chọn Slot khác).
* Khi người chơi Thua (`Game Over`) hoặc Hoàn thành (`Finished`), dữ liệu Save Slot tương ứng sẽ tự động bị xóa.
* Đồ án chỉ sử dụng 1 thư viện ngoài là `pygame` và các thư viện chuẩn của Python (`json`, `time`, `random`).
* Mode Tiếng Việt và Tiếng Anh là 2 mode khác nhau, top-20, resume, save slot của 2 mode là khác nhau.

* Đôi khi nhập từ tiếng Việt trong mode Tiếng Việt sẽ không hiện dấu, khuyến nghị nên xài kiểu gõ VNI và nếu nhập không ra dấu thì lưu vô save_slots/resume rồi mở lại để chơi tiếp.
