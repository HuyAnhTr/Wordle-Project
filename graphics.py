import pygame

#Light mode
L_BG = (255, 255, 255)
L_TEXT = (18, 18, 19)
L_BORDER = (211, 214, 218)
L_KEYBOARD = (174, 174, 174)
L_GUIDE = (211, 214, 218)

#Dark mode
D_BG = (18, 18, 19)
D_TEXT = (255, 255, 255)
D_BORDER = (58, 58, 60)
D_KEYBOARD = (174, 174, 174)
D_GUIDE = (179, 179, 179)

#Khởi tạo trước thì mới gọi hàm được
COLOR_BG = D_BG
COLOR_TEXT = D_TEXT
COLOR_BORDER = D_BORDER
COLOR_KEYBOARD = D_KEYBOARD
COLOR_GUIDE = D_GUIDE

COLOR_GREEN = (106, 170, 100)
COLOR_YELLOW = (201, 180, 88)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (120, 124, 126)
COLOR_PURPLE = (255, 0, 255)

WIDTH, HEIGHT = 1000, 700 
SLOT_COUNT = 5
ICON_SIZE = (30, 30)
SWITCH_SIZE = (60, 40)

class GameGraphics:
    def __init__(self, screen):
        self.screen = screen
        #https://coderslegacy.com/python/pygame-font/
        #Có dùng LLM để tìm font phổ biến được hỗ trợ sẵn trong máy
        self.font_title = pygame.font.SysFont("segoeui", 60, bold=True)
        self.font_input = pygame.font.SysFont("segoeui", 40, bold=True)
        self.font_grid = pygame.font.SysFont("segoeui", 25, bold=True)
        self.font_menu = pygame.font.SysFont("segoeui", 20, bold=True)
        self.font_desc = pygame.font.SysFont("segoeui", 18, bold=True)
        
        #Dùng đường dẫn tương đối (Python sẽ tìm quanh file main trước trong khi chạy)
        self.game_image_link = "Game_image/"
        #Tạo ảnh placeholder (dự phòng) màu tím để dùng khi không load được ảnh thật
        self.placeholder_img = pygame.Surface(ICON_SIZE)
        self.placeholder_img.fill(COLOR_PURPLE) 

        self.images = self.load_all_images()
     
    def turn_to_dark_mode(self, dark_mode):
        global COLOR_BG, COLOR_TEXT, COLOR_BORDER, COLOR_KEYBOARD, COLOR_GUIDE
        if dark_mode:
            COLOR_BG = D_BG
            COLOR_TEXT = D_TEXT
            COLOR_BORDER = D_BORDER
            COLOR_KEYBOARD = D_KEYBOARD
            COLOR_GUIDE = D_GUIDE
        else:
            COLOR_BG = L_BG
            COLOR_TEXT = L_TEXT
            COLOR_BORDER = L_BORDER
            COLOR_KEYBOARD = L_KEYBOARD
            COLOR_GUIDE = L_GUIDE
            
    def load_all_images(self):
        def get_img(name, size=ICON_SIZE):
            path = self.game_image_link + name
            try:
                img = pygame.image.load(path).convert_alpha()
                return img if size is None else pygame.transform.scale(img, size)
            except:
                return pygame.transform.scale(self.placeholder_img, size if size else ICON_SIZE)
        
        return {
            'title': get_img('Wordle_title.png', None),
            'setting': get_img('game-setting.png'),
            'undo': get_img('undo-image.png'),
            'redo': pygame.transform.flip(get_img('undo-image.png', ICON_SIZE), True, False),
            'sw_on': get_img('switch_on.png', SWITCH_SIZE),
            'sw_off': get_img('switch_off.png', SWITCH_SIZE),
            'return': get_img('left-arrow.png'),
            'lang_en': get_img('uk_icon.png'),
            'lang_vn': get_img('vn_icon.png'),
        }

    def draw_centered_text(self, text, font, color, center_x, center_y):
        txt_surf = font.render(str(text), True, color)
        #https://stackoverflow.com/questions/42577197/pygame-how-to-correctly-use-get-rect
        rect = txt_surf.get_rect(center=(center_x, center_y))
        self.screen.blit(txt_surf, rect)
        return rect

    def draw_icon_button(self, x, y, img_key, bg_color=COLOR_GUIDE):
        """Hàm vẽ nút icon dùng chung cho mọi màn hình"""
        rect = pygame.Rect(x, y, 40, 40)
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
        
        if img_key in self.images:
            img = self.images[img_key]
            self.screen.blit(img, img.get_rect(center=rect.center))
        else:
            pygame.draw.rect(self.screen, COLOR_PURPLE, rect) # Vẽ màu tím báo lỗi
        return rect
    
    def draw_text_button(self, rect, text, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        self.draw_centered_text(text, self.font_menu, (255, 255, 255), rect.centerx, rect.centery)

    def draw_press_key_escape(self):
        self.draw_centered_text("Press ESC to return to Menu", self.font_menu, COLOR_GRAY, WIDTH // 2, HEIGHT - 50)
    
    def draw_lang_button(self, cur_lang):
        rect = pygame.Rect(20, 20, 110, 45) 
        pygame.draw.rect(self.screen, COLOR_GUIDE, rect, border_radius=8)
        
        img_key = 'lang_vn' if cur_lang == "VN" else 'lang_en'
        icon = self.images[img_key]
        
        icon_rect = icon.get_rect(midleft=(rect.left + 10, rect.centery))
        self.screen.blit(icon, icon_rect)
        
        lang_txt = self.font_menu.render(cur_lang, True, COLOR_TEXT)
        txt_rect = lang_txt.get_rect(midleft=(icon_rect.right + 10, rect.centery))
        self.screen.blit(lang_txt, txt_rect)
        
        return rect
    
    def draw_menu(self, dark_mode, has_resume, has_cooldown, cur_lang="EN", cooldown_time=0):
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)

        title = self.images['title']
        #https://stackoverflow.com/questions/21209496/getting-width-and-height-of-an-image-in-pygame
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))
        
        btn_setting = self.draw_icon_button(WIDTH - 60, 20, 'setting')

        btn_lang = self.draw_lang_button(cur_lang)
        
        day = cooldown_time // 86400
        hour = (cooldown_time - day * 86400) // 3600
        minute = (cooldown_time - day * 86400 - hour * 3600) // 60
        second = (cooldown_time - day * 86400 - hour * 3600 - minute * 60) // 1

        labels = ["NEW GAME" if (not has_cooldown or cooldown_time == 0) else f"{int(day)}:{int(hour)}:{int(minute)}:{int(second)}", "TOP-20 LIST", "RESUME", "SAVE SLOTS", "HOW TO PLAY"]
        colors = [COLOR_GREEN if (not has_cooldown or cooldown_time == 0) else COLOR_RED, COLOR_GREEN, COLOR_GREEN if has_resume else COLOR_GUIDE, COLOR_GREEN, COLOR_GREEN]
        
        rects = []
        start_y = HEIGHT // 6 + 150
        for i in range(5):
            r = pygame.Rect(WIDTH // 2 - 150, start_y + i * 75, 300, 60)
            self.draw_text_button(r, labels[i], colors[i])
            rects.append(r)

        return btn_setting, *rects, btn_lang

    def draw_input_name(self, dark_mode, name, name_valid = True):
        """Màn hình nhập tên người chơi"""
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)
        self.draw_centered_text("Enter Your Name:", self.font_input, COLOR_TEXT, WIDTH // 2, 250)
        
        input_rect = pygame.Rect(WIDTH // 2 - 400 // 2, 350, 400, 70)
        pygame.draw.rect(self.screen, COLOR_GRAY, input_rect, 2, border_radius=5)
        
        if not name_valid:
            self.draw_centered_text("This name already exists!", self.font_menu, COLOR_TEXT, WIDTH // 2, 430)

        txt = self.font_input.render(name, True, COLOR_GREEN)
        self.screen.blit(txt, (input_rect.x + 20, input_rect.y + 10))

        self.draw_centered_text("The name has maximum 15 characters.", self.font_menu, COLOR_GRAY, WIDTH // 2, 470)

        self.draw_press_key_escape()

    def draw_keyboard(self, used_letters):
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        key_width, key_height = 50, 60
        margin = 5
        start_y = HEIGHT - (key_height + margin) * 3 - 75

        row_index = 0
        for row in rows:
            start_x = WIDTH // 2 - (len(row) * (key_width + margin) - margin) // 2
            col_index = 0
            for char in row:
                rect = pygame.Rect(start_x + col_index * (key_width + margin), start_y + row_index * (key_height + margin), key_width, key_height)
                
                bg_color = COLOR_KEYBOARD
                state = used_letters[ord(char) - ord('A')]
                if state == 3: bg_color = COLOR_GREEN
                elif state == 2: bg_color = COLOR_YELLOW
                elif state == 1: bg_color = COLOR_GRAY

                pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)
                self.draw_centered_text(char, self.font_grid, (255, 255, 255), rect.centerx, rect.centery)

                col_index += 1
            row_index += 1

    def draw_timer(self, time_has_pass):
        hour = int(time_has_pass // 3600)
        minutes = int((time_has_pass % 3600) // 60)
        seconds = int(time_has_pass % 60)
        time_str = f"{hour:02d}:{minutes:02d}:{seconds:02d}"
        
        timer_text = self.font_menu.render(time_str, True, COLOR_GUIDE)
        self.screen.blit(timer_text, (WIDTH - 250, 20)) 
            
    def draw_playing_game(self, dark_mode, board, colors, time_has_pass, guess_valid = True, keyboard = False, used_letters = None):
        """Vẽ bảng 5x6 với trạng thái màu sắc"""
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)
        btn_setting = self.draw_icon_button(WIDTH - 60, 20, 'setting')
        btn_undo = self.draw_icon_button(WIDTH - 160, 20, 'undo')
        btn_redo = self.draw_icon_button(WIDTH - 110, 20, 'redo')

        self.draw_timer(time_has_pass)

        cell_size = 50
        margin = 10
        start_x = WIDTH // 2 - (5 * cell_size + 4 * margin) // 2 
        start_y = HEIGHT // 2 - (6 * cell_size + 5 * margin) // 2 - HEIGHT // 6

        if guess_valid == False:
            self.draw_centered_text("The word is not in the word list!", self.font_menu, COLOR_TEXT, WIDTH // 2, start_y - 50)

        for row in range(6):
            for col in range(5):
                char = board[row][col]
                state = colors[row][col] # 0: Trống, 1: Xám, 2: Vàng, 3: Xanh
                
                rect = pygame.Rect(start_x + col * (cell_size + margin), start_y + row * (cell_size + margin), cell_size, cell_size)
                
                # Xác định màu ô
                bg_color = L_BG
                if state == 1: bg_color = COLOR_GRAY
                elif state == 2: bg_color = COLOR_YELLOW
                elif state == 3: bg_color = COLOR_GREEN

                if state > 0:
                    pygame.draw.rect(self.screen, bg_color, rect, border_radius=3)
                    text_color = (255, 255, 255)

                else:
                    pygame.draw.rect(self.screen, COLOR_BORDER, rect, 2, border_radius=3)
                    text_color = COLOR_TEXT
                
                if char != "":
                    self.draw_centered_text(char, self.font_grid, text_color, rect.centerx, rect.centery)
        
        if keyboard and used_letters is not None:
            self.draw_keyboard(used_letters)

        self.draw_press_key_escape()

        return btn_setting, btn_undo, btn_redo

    def draw_top_20(self, dark_mode, top_list):
        """Vẽ màn hình danh sách 20 người chơi nhanh nhất"""
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)
        start_x = WIDTH // 2 - 400
        
        self.draw_centered_text("TOP-20 PLAYERS", self.font_menu, COLOR_TEXT, WIDTH // 2, 30)

        h_name = self.font_menu.render("Player Name", True, COLOR_GRAY)
        h_avg = self.font_menu.render("Average time(s)", True, COLOR_GRAY)
        h_time = self.font_menu.render("Total time(s)", True, COLOR_GRAY)

        self.screen.blit(h_name, (start_x, 80))
        self.screen.blit(h_avg, (start_x + 300, 80))
        self.screen.blit(h_time, (start_x + 600, 80))

        y_offset = 120
        i = 0
        for record in top_list:
            rank_txt = self.font_menu.render(f"{i+1}.", True, COLOR_TEXT)
            name_txt = self.font_menu.render(record['name'], True, COLOR_TEXT)

            self.screen.blit(rank_txt, (start_x, y_offset))
            self.screen.blit(name_txt, (start_x + 25, y_offset))
            
            self.draw_centered_text(f"{record['time_avg']}s", self.font_menu, COLOR_GREEN, start_x + 300 + h_avg.get_width() // 2, y_offset + 12)
            self.draw_centered_text(f"{record['total_time']}s", self.font_menu, COLOR_GREEN, start_x + 600 + h_time.get_width() // 2, y_offset + 12)

            y_offset += 30
            i += 1
            
        self.draw_press_key_escape()
    
    def draw_save_slots(self, dark_mode, save_slots):
        """Vẽ màn hình Save_slots chỉ với Player, Time và Rounds"""
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)
        self.draw_centered_text("SAVE SLOTS", self.font_title, COLOR_TEXT, WIDTH // 2, 50)
        
        slot_width = 500
        slot_height = 80
        margin = 20
        start_y = 150
        btn_list = []

        for i in range(SLOT_COUNT):
            rect = pygame.Rect(WIDTH // 2 - slot_width // 2, start_y + i * (slot_height + margin), slot_width, slot_height)
            
            border_color = COLOR_GREEN if i < len(save_slots) else COLOR_BORDER
            pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)

            if i < len(save_slots):
                slot = save_slots[i]
                name_txt = self.font_menu.render(f"Player: {slot['name']}", True, COLOR_TEXT)
                info_txt = self.font_menu.render(f"Time: {int(slot['timer'])}s  |  Round: {slot['round']}", True, COLOR_GRAY)
                
                self.screen.blit(name_txt, (rect.x + 20, rect.y + 15))
                self.screen.blit(info_txt, (rect.x + 20, rect.y + 45))
            else:
                self.draw_centered_text("Empty Slot", self.font_menu, COLOR_GUIDE, rect.centerx, rect.centery)
            
            btn_list.append(rect)
        
        self.draw_press_key_escape()
        return btn_list

    def draw_want_to_save_slot(self, dark_mode):
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)
        self.draw_centered_text("Do you want to save this game to a Save Slot?", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 100)
        self.draw_centered_text("(Choosing 'NO' will save to Resume instead)", self.font_menu, COLOR_GRAY, WIDTH // 2, HEIGHT // 2 - 60)

        btn_yes = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 100, 50)
        btn_no = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 20, 100, 50)

        self.draw_text_button(btn_yes, "YES", COLOR_GREEN)
        self.draw_text_button(btn_no, "NO", COLOR_RED)
        return btn_yes, btn_no

    def draw_resume(self, dark_mode, last_sessions):
        """Màn hình xác nhận có chơi lại lần chơi trước hay không"""
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)
        
        self.draw_centered_text("Resume Last Session?", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 50)
        
        self.draw_centered_text(f"Player: {last_sessions['name']}", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 + 140)

        count = 0
        for g in last_sessions["guesses"]:
            if g != ["", "", "", "", ""]:
                count += 1

        self.draw_centered_text(f"Guesses Made: {count} ", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 + 180)

        btn_yes = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 100, 50)
        btn_no = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 20, 100, 50)

        self.draw_text_button(btn_yes, "YES", COLOR_GREEN)
        self.draw_text_button(btn_no, "NO", COLOR_RED)

        self.draw_press_key_escape()
        return btn_yes, btn_no
    
    def draw_end_round(self, dark_mode, key_word, time_spent, round_played, time_has_played, win = True):
        """Vẽ màn hình sau khi chơi xong 1 màn"""
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)

        btn_next = btn_stop = None
        if win:
            self.draw_centered_text(f"Congratulations! You guessed the word '{key_word}' in {time_spent} seconds.", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 50)

            btn_next = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 + 100, 200, 50)
            btn_stop = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 100, 200, 50)

            self.draw_text_button(btn_next, "New Round", COLOR_GREEN)
            self.draw_text_button(btn_stop, "Stop here", COLOR_RED)
        else:
            self.draw_centered_text(f"The correct word was '{key_word}'. Better luck next time!", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 + 10)

        avg = round(time_has_played / round_played, 2)

        self.draw_centered_text(f"Round has played: {round_played}", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 100)
        self.draw_centered_text(f"Average time: {avg}", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 150)

        self.draw_press_key_escape()

        return btn_next, btn_stop
    
    def draw_finished(self, dark_mode, player_name, time_has_played, round_played):
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)

        self.draw_centered_text(f"Your name: {player_name}", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 150)
        self.draw_centered_text(f"Round has played: {round_played}", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 100)
        self.draw_centered_text(f"Average time: {round(time_has_played / round_played, 2)}", self.font_menu, COLOR_TEXT, WIDTH // 2, HEIGHT // 2 - 50)

        self.draw_press_key_escape()

    def draw_setting_screen(self, dark_mode=True, keyboard_state=False, has_cooldown=True, cooldown_time=["0","0","0","0"], active_idx=0):
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)

        btn_return = self.draw_icon_button(60, 20, 'return')
        self.draw_centered_text("SETTING", self.font_title, COLOR_TEXT, WIDTH // 2, 80)

        text_kb = self.font_menu.render("Show Virtual Keyboard", True, COLOR_TEXT)
        self.screen.blit(text_kb, (WIDTH // 2 - 165, 200))
        btn_keyboard = self.draw_icon_button(WIDTH // 2 + 100, 195, 'sw_on' if keyboard_state else 'sw_off', COLOR_BG)
        
        text_cooldown = self.font_menu.render("Cooldown Mode" if has_cooldown else "Infinite mode", True, COLOR_TEXT)
        self.screen.blit(text_cooldown, (WIDTH // 2 - 165, 280))
        btn_cooldown = self.draw_icon_button(WIDTH // 2 + 100, 275, 'sw_on' if has_cooldown else 'sw_off', COLOR_BG)
        
        input_rects = [] 

        if has_cooldown:
            input_size = (60, 40)
            margin = 40 
            start_x = WIDTH // 2 - (4 * input_size[0] + 3 * margin) // 2
            start_y = 350
            labels = ["d", "h", "m", "s"]

            for i in range(4):
                rect = pygame.Rect(start_x + i * (margin + input_size[0]), start_y, input_size[0], input_size[1])
                input_rects.append(rect)

                border_color = COLOR_GREEN if i == active_idx else COLOR_BORDER
                border_width = 3 if i == active_idx else 2
                pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=5)

                label_surf = self.font_menu.render(labels[i], True, COLOR_TEXT)
                self.screen.blit(label_surf, (rect.x + rect.width + 5, rect.y + 5))

                txt_surf = self.font_menu.render(cooldown_time[i], True, COLOR_TEXT)
                self.screen.blit(txt_surf, (rect.x + 10, rect.y + 5))
        
            self.draw_centered_text('Press Tab to switch time box', self.font_menu, COLOR_GUIDE, WIDTH // 2, start_y + input_size[1] + 25)
        
        text_dark_mode = self.font_menu.render("Dark Mode" if dark_mode else "White Mode", True, COLOR_TEXT)
        self.screen.blit(text_dark_mode, (WIDTH // 2 - 165, 415 + 50))
        btn_dark_mode = self.draw_icon_button(WIDTH // 2 + 100, 415 + 50, 'sw_on' if dark_mode else 'sw_off', COLOR_BG) 

        self.draw_press_key_escape()

        return btn_return, btn_keyboard, btn_cooldown, btn_dark_mode, input_rects
    
    def draw_how_to_play(self, dark_mode):
        self.turn_to_dark_mode(dark_mode)
        self.screen.fill(COLOR_BG)
        
        start_y = 60
        
        self.draw_centered_text("How To Play", self.font_input, COLOR_TEXT, WIDTH // 2, start_y)
        self.draw_centered_text("Guess the Wordle in 6 tries.", self.font_menu, COLOR_TEXT, WIDTH // 2, start_y + 40)

        desc1 = self.font_desc.render("Each guess must be a valid 5-letter word." , True, COLOR_TEXT)
        desc2 = self.font_desc.render("The color of the tiles will change to show how close your guess was.", True, COLOR_TEXT)
        self.screen.blit(desc1, (WIDTH // 2 - desc1.get_width() // 2, start_y + 80))
        self.screen.blit(desc2, (WIDTH // 2 - desc2.get_width() // 2, start_y + 110))
    
        def draw_example(text, colors, y_offset, explanation):
            x_start = WIDTH // 2 - 125
            for i in range(5):
                rect = pygame.Rect(x_start + i * 55, y_offset, 50, 50)
                bg = COLOR_BG
                if colors[i] == 3: bg = COLOR_GREEN
                elif colors[i] == 2: bg = COLOR_YELLOW
                elif colors[i] == 1: bg = COLOR_GRAY
                
                pygame.draw.rect(self.screen, bg if bg != COLOR_BG else COLOR_BORDER, rect, 0 if bg != COLOR_BG else 2)
                self.draw_centered_text(text[i], self.font_grid, D_TEXT if bg != COLOR_BG else COLOR_TEXT, rect.centerx, rect.centery)
            
            exp_surf = self.font_desc.render(explanation, True, COLOR_TEXT)
            self.screen.blit(exp_surf, (WIDTH // 2 - exp_surf.get_width() // 2, y_offset + 60))

        draw_example("WORDY", [3, 0, 0, 0, 0], start_y + 160, "W is in the word and in the correct spot.")
        draw_example("LIGHT", [0, 2, 0, 0, 0], start_y + 260, "I is in the word but in the wrong spot.")
        draw_example("ROGUE", [0, 0, 0, 1, 0], start_y + 360, "U is not in the word in any spot.")

        self.draw_press_key_escape()