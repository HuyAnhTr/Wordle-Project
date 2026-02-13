import time

class Player:
    def __init__(self, name="", target_word="", board=None, colors=None, timer=0, total_time=0, rounds=0, slot_index=None, win_round=False, word_valid=True, used_letters=None):
        self.name = name
        self.target_word = target_word
        
        self.board = board if board else [["" for _ in range(5)] for _ in range(6)]
        self.colors = colors if colors else [[0 for _ in range(5)] for _ in range(6)]
        self.used_letters = used_letters if used_letters else [0] * 26
        
        self.timer = timer # Thời gian chơi ván hiện tại
        self.total_time = total_time # Tổng thời gian tích lũy
        self.rounds = rounds # Số vòng đã chơi
        self.slot_index = slot_index # Vị trí slot (nếu load từ save)
        
        self.win_round = win_round
        self.word_valid = word_valid
        
        self.current_row = 0
        self.current_col = 0
        self.start_time = 0

    def calculate_cursor(self):
        """Tự động tính lại vị trí con trỏ dựa trên bảng màu"""
        self.current_row = 0
        self.current_col = 0
        
        for r in range(6):
            if self.colors[r][0] != 0: 
                self.current_row += 1
            else:
                count = 0
                for char in self.board[r]:
                    if char != "": count += 1
                self.current_col = count
                break

    def reset_round_state(self, new_target):
        """Reset bảng để chơi ván mới"""
        self.target_word = new_target
        self.board = [["" for _ in range(5)] for _ in range(6)]
        self.colors = [[0 for _ in range(5)] for _ in range(6)]
        self.used_letters = [0] * 26
        self.timer = 0
        self.win_round = False
        self.word_valid = True
        self.current_row = 0
        self.current_col = 0
        self.start_time = time.time()

    def reset(self):
        """Reset về trạng thái người chơi mới hoàn toàn"""
        self.name = ""
        self.total_time = 0
        self.rounds = 0
        self.slot_index = None
        self.reset_round_state("")

    def to_dict(self):
        """Chuyển object thành dict để lưu JSON"""
        return {
            "name": self.name,
            "target": self.target_word,
            "guesses": self.board,
            "colors": self.colors,
            "timer": self.timer,
            "time_previous": self.total_time, 
            "round": self.rounds,
            "win_round": self.win_round,
            "word_valid": self.word_valid,
            "used-letters": self.used_letters,
            "state": "PLAYING" # Mặc định
        }