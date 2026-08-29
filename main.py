import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

class AdvancedTicTacToeApp(App):
    def build(self):
        self.mode = "1P"              # "1P" या "2P"
        self.difficulty = "Medium"     # "Easy", "Medium", "Hard"
        self.score_p1 = 0
        self.score_p2 = 0
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False

        # मेन लेआउट
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # 1. मोड और डिफिकल्टी कंट्रोल बार
        controls_layout = BoxLayout(size_hint=(1, 0.08), spacing=5)
        
        self.mode_btn = Button(text="Mode: 1-Player", font_size=14, background_color=(0.3, 0.5, 0.8, 1))
        self.mode_btn.bind(on_press=self.toggle_mode)
        controls_layout.add_widget(self.mode_btn)

        self.diff_btn = Button(text="Bot: Medium", font_size=14, background_color=(0.8, 0.5, 0.2, 1))
        self.diff_btn.bind(on_press=self.toggle_difficulty)
        controls_layout.add_widget(self.diff_btn)

        main_layout.add_widget(controls_layout)

        # 2. लाइव स्कोरबोर्ड
        self.score_label = Label(
            text=f"X: {self.score_p1}  |  O (Bot): {self.score_p2}",
            font_size=18,
            bold=True,
            size_hint=(1, 0.06),
            color=(0.95, 0.85, 0.2, 1)
        )
        main_layout.add_widget(self.score_label)

        # 3. गेम स्टेटस लेबल
        self.status_label = Label(
            text="Player X की बारी",
            font_size=20,
            size_hint=(1, 0.08),
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(self.status_label)

        # 4. 3x3 गेम ग्रिड
        self.grid = GridLayout(cols=3, spacing=6, size_hint=(1, 0.6))
        self.buttons = []

        for i in range(9):
            btn = Button(
                text='',
                font_size=36,
                bold=True,
                background_color=(0.2, 0.2, 0.25, 1)
            )
            btn.bind(on_press=lambda instance, idx=i: self.on_tile_click(instance, idx))
            self.buttons.append(btn)
            self.grid.add_widget(btn)

        main_layout.add_widget(self.grid)

        # 5. एक्शन बटन्स (Restart & Reset Score)
        action_layout = BoxLayout(size_hint=(1, 0.1), spacing=6)
        
        restart_btn = Button(text='New Round', font_size=16, background_color=(0.2, 0.7, 0.4, 1))
        restart_btn.bind(on_press=self.restart_round)
        action_layout.add_widget(restart_btn)

        reset_score_btn = Button(text='Reset Score', font_size=16, background_color=(0.8, 0.3, 0.3, 1))
        reset_score_btn.bind(on_press=self.reset_all_scores)
        action_layout.add_widget(reset_score_btn)

        main_layout.add_widget(action_layout)

        return main_layout

    def toggle_mode(self, instance):
        self.mode = "2P" if self.mode == "1P" else "1P"
        self.mode_btn.text = f"Mode: {'2-Player' if self.mode == '2P' else '1-Player'}"
        self.diff_btn.disabled = (self.mode == "2P")
        self.reset_all_scores(None)

    def toggle_difficulty(self, instance):
        diffs = ["Easy", "Medium", "Hard"]
        current_idx = diffs.index(self.difficulty)
        self.difficulty = diffs[(current_idx + 1) % len(diffs)]
        self.diff_btn.text = f"Bot: {self.difficulty}"

    def on_tile_click(self, button, index):
        if self.board[index] != '' or self.game_over:
            return

        self.apply_move(index, self.current_player)

        if self.check_winner(self.current_player):
            self.end_game(f"🎉 Player {self.current_player} जीत गया!", winner=self.current_player)
            return

        if '' not in self.board:
            self.end_game("मैच टाई (Draw) हो गया!")
            return

        if self.mode == "1P":
            self.game_over = True
            self.status_label.text = "🤖 Bot सोच रहा है..."
            Clock.schedule_once(self.trigger_bot_move, 0.4)
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.status_label.text = f"Player {self.current_player} की बारी"

    def trigger_bot_move(self, dt):
        if '' not in self.board:
            return

        move = self.calculate_bot_move()
        self.apply_move(move, 'O')

        if self.check_winner('O'):
            self.end_game("🤖 Bot जीत गया!", winner='O')
        elif '' not in self.board:
            self.end_game("मैच टाई (Draw) हो गया!")
        else:
            self.current_player = 'X'
            self.status_label.text = "Player X की बारी"
            self.game_over = False

    def calculate_bot_move(self):
        empty = [i for i, v in enumerate(self.board) if v == '']

        if self.difficulty == "Easy":
            return random.choice(empty)

        elif self.difficulty == "Medium":
            # Win or Block
            for p in ['O', 'X']:
                for i in empty:
                    self.board[i] = p
                    if self.check_winner(p, highlight=False):
                        self.board[i] = ''
                        return i
                    self.board[i] = ''
            return 4 if 4 in empty else random.choice(empty)

        elif self.difficulty == "Hard":
            # Unbeatable (Minimax Algorithm)
            best_score = -float('inf')
            best_move = empty[0]
            for i in empty:
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
            return best_move

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O', highlight=False):
            return 10 - depth
        if self.check_winner('X', highlight=False):
            return depth - 10
        if '' not in board:
            return 0

        empty = [i for i, v in enumerate(board) if v == '']
        if is_maximizing:
            max_eval = -float('inf')
            for i in empty:
                board[i] = 'O'
                eval_score = self.minimax(board, depth + 1, False)
                board[i] = ''
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for i in empty:
                board[i] = 'X'
                eval_score = self.minimax(board, depth + 1, True)
                board[i] = ''
                min_eval = min(min_eval, eval_score)
            return min_eval

    def apply_move(self, index, player):
        self.board[index] = player
        btn = self.buttons[index]
        btn.text = player
        btn.color = (0.2, 0.7, 1, 1) if player == 'X' else (1, 0.6, 0.2, 1)

    def check_winner(self, player, highlight=True):
        combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in combos:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == player:
                if highlight:
                    for idx in combo:
                        self.buttons[idx].background_color = (0.2, 0.8, 0.3, 1)
                return True
        return False

    def end_game(self, message, winner=None):
        self.status_label.text = message
        self.game_over = True
        if winner == 'X':
            self.score_p1 += 1
        elif winner == 'O':
            self.score_p2 += 1
        self.update_score_display()

    def update_score_display(self):
        p2_title = "Player O" if self.mode == "2P" else "Bot (O)"
        self.score_label.text = f"X: {self.score_p1}  |  {p2_title}: {self.score_p2}"

    def restart_round(self, instance):
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        self.status_label.text = "Player X की बारी"
        for btn in self.buttons:
            btn.text = ''
            btn.background_color = (0.2, 0.2, 0.25, 1)

    def reset_all_scores(self, instance):
        self.score_p1 = 0
        self.score_p2 = 0
        self.update_score_display()
        self.restart_round(None)

if __name__ == '__main__':
    AdvancedTicTacToeApp().run()
        
