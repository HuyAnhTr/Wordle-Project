import pygame
import json
import random
import time
from graphics import GameGraphics, WIDTH, HEIGHT, SLOT_COUNT
from word_list import WORD_LIST, WORD_TEST
from word_list_vn import VN_LIST, VN_TEST
#WORD_LIST = WORD_TEST #Bỏ dấu thăng để chuyển sang bộ chữ test case
#VN_LIST = VN_TEST #Bỏ dấu thăng để chuyển sang bộ chữ test case
from data_structure import Stack
from player import Player

clock = pygame.time.Clock()
MY_KEY = "TRAN_HOANG_HUY_ANH"

def map_vn_char(char):
    mapping = {
        'Ă':'A','Â':'A','Á':'A','À':'A','Ả':'A','Ã':'A','Ạ':'A','Ắ':'A','Ằ':'A','Ẳ':'A','Ẵ':'A','Ặ':'A','Ấ':'A','Ầ':'A','Ẩ':'A','Ẫ':'A','Ậ':'A',
        'Đ':'D',
        'Ê':'E','É':'E','È':'E','Ẻ':'E','Ẽ':'E','Ẹ':'E','Ế':'E','Ề':'E','Ể':'E','Ễ':'E','Ệ':'E',
        'Í':'I','Ì':'I','Ỉ':'I','Ĩ':'I','Ị':'I',
        'Ô':'O','Ơ':'O','Ó':'O','Ò':'O','Ỏ':'O','Õ':'O','Ọ':'O','Ố':'O','Ồ':'O','Ổ':'O','Ỗ':'O','Ộ':'O','Ớ':'O','Ờ':'O','Ở':'O','Ỡ':'O','Ợ':'O',
        'Ư':'U','Ú':'U','Ù':'U','Ủ':'U','Ũ':'U','Ụ':'U','Ứ':'U','Ừ':'U','Ử':'U','Ữ':'U','Ự':'U',
        'Ý':'Y','Ỳ':'Y','Ỷ':'Y','Ỹ':'Y','Ỵ':'Y'
    }
    if char in mapping: return mapping[char]
    return char

def encrypt(data, key):
    """Mã hóa XOR trả về kiểu bytes để lưu file nhị phân"""
    res = bytearray() # Nguồn: https://docs.python.org/3/library/stdtypes.html#bytearray
    key_length = len(key)
    try:
        #Nếu là chuỗi thì encode, nếu là bytes thì giữ nguyên
        data = data.encode('utf-8')
    except:
        pass
    for i in range(len(data)):
        res.append(data[i] ^ ord(key[i % key_length]))
    return res

def save_game_data(full_data):
    """Lưu file nhị phân"""
    # ensure_ascii=False để hỗ trợ tiếng Việt hoặc ký tự đặc biệt
    string = json.dumps(full_data, indent=4, ensure_ascii=False)
    encrypted_bytes = encrypt(string, MY_KEY)
    
    with open("data.json", mode="wb") as f:
        f.write(encrypted_bytes)

def load_game_data():
    """Đọc file nhị phân"""
    default_data = {
        "current_language": "EN", 
        "VN": {"top_20": [], "last_session": None, "save_slots": [], "setting": None,"cooldown": None}, 
        "EN": {"top_20": [], "last_session": None, "save_slots": [], "setting": None,"cooldown": None}
    }
    try:
        with open("data.json", mode="rb") as f:
            data_raw = f.read()
        decrypted_bytes = encrypt(data_raw, MY_KEY)
            
        # Nguồn: https://docs.python.org/3/library/stdtypes.html#bytes.decode
        decode_data = decrypted_bytes.decode('utf-8')
        loaded_data = json.loads(decode_data)
        
        # Đồng bộ key thiếu nếu file cũ
        for key in default_data:
            if key not in loaded_data:
                loaded_data[key] = default_data[key]
        return loaded_data
    except:
        return default_data

class WordleGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Wordle")
        self.ui = GameGraphics(self.screen)
        self.game_data = None
        
        self.full_data = load_game_data()
        self.cur_lang = self.full_data["current_language"]
        
        self.switch_data_context()

        self.player = Player() 

        self.state = "MENU"
        self.state_history = Stack()
        
        self.player_name_valid = True
        self.target_word = ""
        
        self.time_spent = 0

        self.cooldown_input = ["0","0","0","10"]
        self.active_cooldown_index = 0
        self.cooldown_time = 10 
        self.has_cooldown = True
        
        self.dark_mode = True
        self.has_keyboard = True
    
        self.waiting = False
        self.remaining_time = 0
        
        self.move_stack = Stack() #Dùng cho nút left arrow trong setting
        self.has_resume = self.game_data["last_session"] is not None
        self.pending_save_data = None #Flag cho việc lưu vô save slot - nếu true thì khi nhấn vào save slot mới lưu được, còn ko thì bấm vào ko thay đổi gì
        self.is_quitting = False #Trước khi save slot mà ấn QUIT(tắt cửa sổ) thì bật True, sau khi save slot thì lập tức tắt
        self.running = True
        
        self.load_settings_from_data()
        
    def switch_data_context(self):
        if self.cur_lang not in self.full_data:
            self.full_data[self.cur_lang] = {"top_20": [], "last_session": None, "save_slots": [], "setting": None,"cooldown": None}
        self.game_data = self.full_data[self.cur_lang]
    
    def load_settings_from_data(self):
        if "setting" in self.game_data and self.game_data["setting"] is not None:
            if "dark_mode" in self.game_data["setting"]:
                self.dark_mode = self.game_data["setting"]["dark_mode"]
            else:
                self.dark_mode = True
                
            if "keyboard" in self.game_data["setting"]:
                self.has_keyboard = self.game_data["setting"]["keyboard"]
            else:
                self.has_keyboard = True
                
    def save_current(self):
        self.full_data["current_language"] = self.cur_lang 
        save_game_data(self.full_data)
        
    def reset_the_game(self):
        """Reset trạng thái game về ban đầu"""
        self.player.reset() 
        
        self.target_word = ""
        self.time_spent = 0
        self.move_stack = Stack()
        
        self.state_history = Stack()
        self.state = "MENU"

    def start_new_round(self):
        """Bắt đầu ván mới"""
        word_list = VN_LIST if self.cur_lang == "VN" else WORD_LIST
        new_target = random.choice(word_list).upper()
        self.player.reset_round_state(new_target)
        self.state = "PLAYING"

    def update_cooldown(self):
        d = int(self.cooldown_input[0]) if self.cooldown_input[0] != "" else 0
        h = int(self.cooldown_input[1]) if self.cooldown_input[1] != "" else 0
        m = int(self.cooldown_input[2]) if self.cooldown_input[2] != "" else 0
        s = int(self.cooldown_input[3]) if self.cooldown_input[3] != "" else 0
        
        self.cooldown_time = d * 86400 + h * 3600 + m * 60 + s
        
        old_start = 0
        if self.game_data["cooldown"] is not None:
            if "start_cooldown" in self.game_data["cooldown"]:
                old_start = self.game_data["cooldown"]["start_cooldown"]

        self.game_data["cooldown"] = {
            "has_cooldown": self.has_cooldown,
            "duration": self.cooldown_time,
            "input": self.cooldown_input,
            "start_cooldown": old_start 
        }
        self.save_current()
                
    def load_cooldown(self):
        if not self.has_cooldown:
            self.waiting = False
            return

        if "cooldown" in self.game_data and self.game_data["cooldown"] is not None:
            session = self.game_data["cooldown"]
            if "start_cooldown" in session and session["start_cooldown"] > 0:
                last_time = session["start_cooldown"]
                time_has_pass = time.time() - last_time
                if time_has_pass < self.cooldown_time:
                    self.waiting = True
                    self.remaining_time = self.cooldown_time - time_has_pass
                else:
                    self.waiting = False
                    self.remaining_time = 0
    
    def trigger_cooldown(self):
        if self.has_cooldown:
            self.game_data["cooldown"]["start_cooldown"] = time.time()
            self.save_current()
            self.waiting = True
            self.remaining_time = self.cooldown_time

    def update_resume(self):
        """Lưu trạng thái Player hiện tại vào resume"""
        self.game_data["last_session"] = self.player.to_dict()
        
        # Nếu đang ở End Round thì lưu state là End Round, ngược lại là Playing
        if self.state == "END_ROUND":
            self.game_data["last_session"]["state"] = "END_ROUND"
        else:
            self.game_data["last_session"]["state"] = "PLAYING"

        self.has_resume = self.game_data["last_session"] is not None
        self.save_current()

    def load_resume(self):
        """Khôi phục trạng thái từ file JSON vào class Player và Game"""
        session = self.game_data["last_session"]
        
        # Giữ lại slot index hiện tại nếu đang load từ save slot
        current_slot_index = self.player.slot_index

        self.player = Player(
            name=session["name"],
            target_word=session["target"],
            board=session["guesses"],
            colors=session["colors"],
            timer=session["timer"],
            total_time=session["time_previous"],
            rounds=session["round"],
            slot_index=current_slot_index, # Truyền lại slot index
            win_round=session["win_round"],
            word_valid=session["word_valid"],
            used_letters=session.get("used-letters", [0]*26)
        )
        
        # tính toán lại vị trí con trỏ
        self.player.calculate_cursor()
        
        # Xác định trạng thái
        if "state" in session:
            saved_state = session["state"]
        else:
            save_state = "PLAYING"
        self.target_word = session["target"]
        
        # Check trạng thái và fix lỗi chơi xong mà hiện lại từ khóa
        if self.player.current_row > 0:
            prev_row = self.player.current_row - 1
            if self.player.colors[prev_row] == [3, 3, 3, 3, 3]:
                self.player.win_round = True
                self.state = "END_ROUND"
            elif self.player.current_row == 6: 
                self.player.win_round = False
                self.state = "END_ROUND"
            else:
                self.state = saved_state
        else:
            self.state = saved_state

        if self.state == "PLAYING":
            self.player.start_time = time.time()

        self.has_resume = False

    def clear_player_session(self):
        """Xóa dữ liệu Save Slot/Resume khi chơi xong"""
        # Nếu đang chơi từ Slot -> Xóa Slot đó
        if self.player.slot_index is not None:
            idx = self.player.slot_index
            if idx < len(self.game_data["save_slots"]):
                new_list = []
                for i in range(len(self.game_data["save_slots"])):
                    if i == idx: continue
                    new_list.append(self.game_data["save_slots"][i])
                self.game_data["save_slots"] = new_list
            
            self.player.slot_index = None 

        self.game_data["last_session"] = None
        self.has_resume = False
        self.save_current()

    def update_top_20(self, time_avg, time_has_played):
        """Sắp xếp và giới hạn 20 người"""
        self.game_data["top_20"].append({"name": self.player.name, "time_avg": time_avg, "total_time": time_has_played})

        for i in range(len(self.game_data["top_20"]) - 1, 0, -1):
            for j in range(i):
                if self.game_data["top_20"][j]["time_avg"] > self.game_data["top_20"][j + 1]["time_avg"]:
                    temp = self.game_data["top_20"][j]
                    self.game_data["top_20"][j] = self.game_data["top_20"][j + 1]
                    self.game_data["top_20"][j + 1] = temp

        self.game_data["top_20"] = self.game_data["top_20"][:20] 
        self.save_current()
    
    def undo(self):
        r, c = self.player.current_row, self.player.current_col
        if c == 0:
            if r > 0:
                self.player.current_row -= 1
                r = self.player.current_row
                self.move_stack.push([self.player.board[r], self.player.colors[r]])
                self.player.board[r] = ["" for _ in range(5)]
                self.player.colors[r] = [0 for _ in range(5)]
        else:
            self.move_stack.push([self.player.board[r], self.player.colors[r]])
            self.player.board[r] = ["" for _ in range(5)]
            self.player.colors[r] = [0 for _ in range(5)]
            self.player.current_col = 0
        
    def redo(self):
        if not self.move_stack.is_empty():
            prev = self.move_stack.pop()
            r = self.player.current_row
            self.player.board[r] = prev[0]
            self.player.colors[r] = prev[1]

        if self.state == "PLAYING":
            self.player.calculate_cursor() 

    def check_word(self):
        r = self.player.current_row
        guess = "".join(self.player.board[r]).upper()
        current_list = VN_LIST if self.cur_lang == "VN" else WORD_LIST
        if guess not in [w.upper() for w in current_list]:
            self.player.word_valid = False
            return

        self.player.word_valid = True
        target_list = list(self.player.target_word)
        
        # Check Green
        for i in range(5):
            if guess[i] == self.player.target_word[i]:
                self.player.colors[r][i] = 3
                target_list[i] = None
                latin = map_vn_char(guess[i])
                self.player.used_letters[ord(latin) - ord('A')] = 3

        # Check Yellow/Gray
        for i in range(5):
            if self.player.colors[r][i] != 3:
                latin = map_vn_char(guess[i])
                idx = ord(latin) - ord('A')
                if guess[i] in target_list:
                    self.player.colors[r][i] = 2
                    for j in range(5):
                        if target_list[j] == guess[i]:
                            target_list[j] = None
                            self.player.used_letters[idx] = max(self.player.used_letters[idx], 2)
                            break
                else:
                    self.player.colors[r][i] = 1
                    self.player.used_letters[idx] = max(self.player.used_letters[idx], 1)

        if guess == self.player.target_word:
            # Cộng dồn thời gian vào player
            round_time = round(self.player.timer + (time.time() - self.player.start_time), 2)
            self.player.timer = round_time 
            self.player.total_time += round_time 
            self.player.rounds += 1
            
            self.player.win_round = True
            self.state = "END_ROUND"
            self.update_resume()

        elif self.player.current_row == 5:
            # Hết lượt mà chưa thắng -> Thua
            self.game_data["last_session"] = None
            self.player.rounds += 1
            self.save_current()
            self.state = "END_ROUND"
        else:
            self.player.current_row += 1
            self.player.current_col = 0

    def update_save_slots(self, slot_index=None):
        """Cập nhật dữ liệu vào Save Slot"""
        session_data = self.player.to_dict() # Lấy dữ liệu hiện tại của player
        #Nếu player đang chơi từ một slot có sẵn, ghi đè vào chính nó
        if self.player.slot_index is not None:
            idx = self.player.slot_index
            if idx < len(self.game_data["save_slots"]):
                self.game_data["save_slots"][idx] = session_data
                save_game_data(self.game_data)
                return
                
        # Nếu được truyền slot_index cụ thể từ màn hình chọn slot
        if slot_index is not None:
            if slot_index < len(self.game_data["save_slots"]):
                self.game_data["save_slots"][slot_index] = session_data
            else:
                self.game_data["save_slots"].append(session_data)
        #Nếu là ván mới hoàn toàn và slot còn trống
        else:
            if len(self.game_data["save_slots"]) < SLOT_COUNT:
                self.game_data["save_slots"].append(session_data)
        self.save_current()

    def run(self):
        while self.running:
            self.load_cooldown()

            if self.state == "MENU":
                btn_setting, btn_new, btn_top, btn_res, btn_save, btn_how_to_play, btn_lang = self.ui.draw_menu(self.dark_mode, self.has_resume, self.waiting, self.cur_lang, self.remaining_time)
                
            elif self.state == "INPUT_NAME":
                self.ui.draw_input_name(self.dark_mode, self.player.name, self.player_name_valid)

            elif self.state == "PLAYING":
                # Tính thời gian hiển thị: thời gian cũ đã lưu + thời gian trôi qua từ lúc start_time
                current_display_time = round(time.time() - self.player.start_time + self.player.timer, 2)
                btn_setting, btn_undo, btn_redo = self.ui.draw_playing_game(self.dark_mode, self.player.board, self.player.colors, current_display_time, self.player.word_valid, self.has_keyboard, self.player.used_letters)

            elif self.state == "END_ROUND":
                btn_next, btn_stop = self.ui.draw_end_round(self.dark_mode, self.player.target_word, round(self.player.timer, 2), self.player.rounds, self.player.total_time, self.player.win_round)

            elif self.state == "FINISHED":
                self.ui.draw_finished(self.dark_mode, self.player.name, self.player.total_time, self.player.rounds)
                if self.player.rounds > 0:
                    self.update_top_20(round(self.player.total_time / self.player.rounds, 2), round(self.player.total_time, 2))
                
                self.clear_player_session()
                self.trigger_cooldown()
                self.reset_the_game()

            elif self.state == "RESUME":
                btn_yes, btn_no = self.ui.draw_resume(self.dark_mode, self.game_data["last_session"])

            elif self.state == "TOP_20":
                self.ui.draw_top_20(self.dark_mode, self.game_data["top_20"])

            elif self.state == "SETTING":
                btn_return, btn_keyboard, btn_cooldown, btn_dark_mode, cooldown_boxes = self.ui.draw_setting_screen(self.dark_mode, self.has_keyboard, self.has_cooldown, self.cooldown_input, self.active_cooldown_index)

            elif self.state == "WANT_TO_SAVE":
                btn_yes, btn_no = self.ui.draw_want_to_save_slot(self.dark_mode)
            
            elif self.state == "SAVE_SLOTS":
                slot_btns = self.ui.draw_save_slots(self.dark_mode, self.game_data["save_slots"])
            
            elif self.state == "HOW_TO_PLAY":
                self.ui.draw_how_to_play(self.dark_mode)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.state == "PLAYING":
                        self.state = "WANT_TO_SAVE"
                        self.player.timer += time.time() - self.player.start_time # Cộng dồn timer
                        self.player.start_time = time.time()
                        self.is_quitting = True
                        continue
                    
                    elif self.state == "END_ROUND":
                        if self.player.win_round:
                            self.state = "WANT_TO_SAVE"
                            self.is_quitting = True
                            continue
                        else:
                            # Thua mà thoát -> Xóa luôn
                            self.trigger_cooldown()
                            if self.player.rounds > 0 and self.player.total_time > 0:
                                self.update_top_20(round(self.player.total_time / self.player.rounds, 2), self.player.total_time)
                            self.clear_player_session()

                    elif self.state == "FINISHED":
                        pass

                    self.update_cooldown()  
                    pygame.quit()
                    self.running = False
                    break
                #Có dùng LLM để biết rằng pygame hỗ trợ cả TEXTINPUT
                if event.type == pygame.TEXTINPUT:
                    if self.state == "PLAYING":
                        if self.player.current_col < 5:
                            char = event.text.upper()
                            latin = map_vn_char(char)
                            if 'A' <= latin <= 'Z':
                                self.player.board[self.player.current_row][self.player.current_col] = char
                                self.player.current_col += 1
                    elif self.state == "INPUT_NAME":
                        if len(self.player.name) < 15:
                            self.player.name += event.text.upper()
                            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "MENU":
                        if btn_lang.collidepoint(event.pos):
                            self.cur_lang = "VN" if self.cur_lang == "EN" else "EN"
                            self.switch_data_context()
                            self.load_settings_from_data()
                            self.player.reset()
                            self.save_current()
                            self.has_resume = self.game_data["last_session"] is not None
                        if btn_setting.collidepoint(event.pos):
                            self.state = "SETTING"
                        elif btn_new.collidepoint(event.pos):
                            if not self.waiting:
                                self.player.slot_index = None # Reset slot
                                self.state = "INPUT_NAME"
                        elif btn_top.collidepoint(event.pos):
                            self.state = "TOP_20"
                        elif btn_res.collidepoint(event.pos) and self.has_resume:
                            self.state = "RESUME"
                        elif btn_save.collidepoint(event.pos):
                            self.state = "SAVE_SLOTS"
                        elif btn_how_to_play.collidepoint(event.pos):
                            self.state = "HOW_TO_PLAY"

                    elif self.state == "PLAYING":
                        if btn_setting.collidepoint(event.pos):
                            self.state_history.push(self.state)
                            self.state = "SETTING"
                        elif btn_undo.collidepoint(event.pos):
                            self.undo()
                        elif btn_redo.collidepoint(event.pos):
                            self.redo()
                    
                    elif self.state == "RESUME":
                        if btn_yes.collidepoint(event.pos):
                            self.load_resume()
                        elif btn_no.collidepoint(event.pos):
                            self.has_resume = False
                            self.game_data["last_session"] = None
                            self.save_current()
                            self.reset_the_game()
                    
                    elif self.state == "END_ROUND":
                        if self.player.win_round:
                            if btn_next.collidepoint(event.pos):
                                self.start_new_round()
                            elif btn_stop.collidepoint(event.pos):
                                self.state = "FINISHED"
                            
                    elif self.state == "SETTING":
                        if btn_keyboard.collidepoint(event.pos):
                            self.has_keyboard = not self.has_keyboard
                        elif btn_return.collidepoint(event.pos):
                            self.update_cooldown()
                            if self.state_history.is_empty():
                                self.state = "MENU"
                            else:
                                self.state = self.state_history.pop()
                        elif btn_cooldown.collidepoint(event.pos):
                            self.has_cooldown = not self.has_cooldown
                        elif btn_dark_mode.collidepoint(event.pos):
                            self.dark_mode = not self.dark_mode
                        i = 0
                        for btn in cooldown_boxes:
                            if btn.collidepoint(event.pos): self.active_cooldown_index = i
                            i += 1
                    
                    elif self.state == "WANT_TO_SAVE":
                        if btn_yes.collidepoint(event.pos):
                            self.pending_save_data = True
                            self.state = "SAVE_SLOTS"
                        elif btn_no.collidepoint(event.pos):
                            self.update_resume()
                            if self.is_quitting:
                                pygame.quit()
                                self.running = False
                                break
                            else: self.reset_the_game()
                    
                    elif self.state == "SAVE_SLOTS":
                        for i in range(len(slot_btns)):
                            btn = slot_btns[i]
                            if btn.collidepoint(event.pos):
                                if self.pending_save_data:
                                    if self.player.slot_index is not None:
                                        self.update_save_slots()
                                    else:
                                        self.player.slot_index = i
                                        self.update_save_slots(i)
                                    self.game_data["last_session"] = None
                                    self.save_current()
                                    self.pending_save_data = False 
                                    if self.is_quitting:
                                        pygame.quit()
                                        self.running = False
                                        break
                                    else:
                                        self.reset_the_game()
                                        self.state = "MENU"
                                else:
                                    if i < len(self.game_data["save_slots"]):
                                        self.game_data["last_session"] = self.game_data["save_slots"][i]
                                        # Gán slot index để biết đường xóa
                                        self.player.slot_index = i 
                                        self.load_resume()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        while not self.state_history.is_empty(): self.state_history.pop()
                        self.update_cooldown()

                    if self.state == "INPUT_NAME":
                        if event.key == pygame.K_RETURN and self.player.name != "":
                            name_in_top_20 = [p["name"] for p in self.game_data["top_20"]]
                            name_in_save_slots = [p["name"] for p in self.game_data["save_slots"]]
                            if self.player.name in name_in_top_20 or self.player.name in name_in_save_slots:
                                self.player_name_valid = False
                            else: 
                                self.start_new_round()
                        elif event.key == pygame.K_BACKSPACE: 
                            self.player.name = self.player.name[:-1]
                            self.player_name_valid = True
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                            self.player_name_valid = True
                        
                    elif self.state == "TOP_20":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                    
                    elif self.state == "PLAYING":
                        if event.key == pygame.K_ESCAPE:
                            self.is_quitting = False
                            self.player.timer += time.time() - self.player.start_time
                            self.state = "WANT_TO_SAVE"
                        elif event.key == pygame.K_BACKSPACE:
                            if self.player.current_col > 0:
                                self.player.current_col -= 1
                                self.player.board[self.player.current_row][self.player.current_col] = ""
                                self.player.word_valid = True
                        elif event.key == pygame.K_RETURN and self.player.current_col == 5:
                            self.check_word()
                            self.move_stack = Stack()

                    elif self.state == "END_ROUND":
                        if event.key == pygame.K_ESCAPE:
                            if not self.player.win_round:
                                # Thua -> Xóa save
                                self.trigger_cooldown()
                                self.clear_player_session()
                                if self.player.rounds > 0 and self.player.total_time > 0:
                                    self.update_top_20(round(self.player.total_time / self.player.rounds, 2), self.player.total_time)
                                self.reset_the_game()
                            else:
                                self.is_quitting = False
                                self.player.timer += time.time() - self.player.start_time
                                self.state = "WANT_TO_SAVE"

                    elif self.state == "FINISHED":
                        if event.key == pygame.K_ESCAPE:
                            self.reset_the_game()
                            
                    elif self.state == "RESUME":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                    
                    elif self.state == "SAVE_SLOTS":
                        if event.key == pygame.K_ESCAPE:
                            if self.pending_save_data:
                                self.update_cooldown()
                                self.update_resume()
                            self.state = "MENU"
                    
                    elif self.state == "SETTING":
                        if event.key == pygame.K_ESCAPE:
                            self.update_cooldown()
                            self.state = "MENU"
                        elif self.has_cooldown:
                            if event.key == pygame.K_TAB:
                                self.active_cooldown_index = (self.active_cooldown_index + 1) % 4
                            elif event.unicode.isdigit():
                                if len(self.cooldown_input[self.active_cooldown_index]) < 2:
                                    self.cooldown_input[self.active_cooldown_index] += event.unicode
                            elif event.key == pygame.K_BACKSPACE:
                                if len(self.cooldown_input[self.active_cooldown_index]) == 2:
                                    self.cooldown_input[self.active_cooldown_index] = self.cooldown_input[self.active_cooldown_index][0]
                                else:
                                    self.cooldown_input[self.active_cooldown_index] = ""
                    
                    elif self.state == "HOW_TO_PLAY":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                            
            if self.running:
                pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = WordleGame()
    game.run()

#Kiếm word-list - Đã xong
#Tìm cách để chạy game trên một cửa sổ - Đã xong
#Kiếm logic làm game, cách mở/lưu data, cách nhận tín hiệu từ bàn phím, chuột- Đã xong
#Tìm cách vẽ màn hình - vẽ chữ - vẽ nút, dùng pygame.font, self.screen.fill và pygame.draw.rect: Đã xong
#Thống nhất màu game, chỉnh lại màn hình chính - Đã xong
#Vẽ màn hinh playing, thêm màn hình input name trước playing: Đã xong
#Thêm cách quay lại màn hình trước (esc để thoát về menu) - Đã xong
#Thêm màn hình top-20, resume - Đã xong
#Cập nhật logic input name, check-word, chơi song thì lưu vô top 20 rồi sort top 20 - Đã xong
#Sửa lại phần cập nhật top 20 theo timespent // số ván - Đã xong
#Bổ sung màn hình end_round trước màn hình Finished, hiển thị thời gian đã chơi trong vòng trước đó, thời gian trung bình, thêm 2 nút continue và stop here
#Stop here: chuyển sang màn hình finished và hiện số vòng/số từ đoán được, thời gian trung bình - Đã xong
#chỉnh lại cách tính thời gian khi resume - Đã xong
#Làm keyboard - setting - time scoring : Xong keyboard 
#làm tiếp phần hiện cooldown trên new game - Cần đồng bộ (lúc ấn top 20 về menu thì cooldown reset), kiểm tra các vị trí đặt update_resume và load_resume - Đã xong ?
#Fix logic reset cooldown và bắt đầu cooldown, tạo load cooldown để khôi phục trạng thái cooldown trước đó - Đã xong 
#Làm time scoring trong setting - mã hóa - save slots
#timer trong khi chơi - Đã xong
#tạo màn hình save-slot và lưu trong game data: đã xong
#Thống nhất workflow về resume và save slots, khi end-round thắng thì hiện màn hình want-to-save có 2 nút, nút save thì mở lại màn hình save-slot và ấn chuột để chọn, nút no save thì lưu vô resume - Đã xong
# Đưa curr play vô save-slot trong game data, một cái idx cho cái save khi mở để chơi tiếp, nếu thắng thì xóa cái save slot đó - Đã xong
#Bỏ time-scoring,
#Thêm mode tiếng việt
#thêm mã hóa file data bằng cách xor và nhị phân - Đã xong
#Thêm word-test và kiểm tra lần cuối - Đã xong