import math
import pygame
from game.button import ChoiceButton
from game.adaptive_cpu import AdaptiveCPU
from game.icons import draw_icon


class GameEngine:
    # Each key beats the value it maps to
    BEATS = {
        "ROCK": "SCISSORS",
        "SCISSORS": "PAPER",
        "PAPER": "ROCK",
    }
    WIN_SCORE = 5

    # Round timing (milliseconds)
    COUNTDOWN_WORDS = ["Rock...", "Paper...", "Scissors..."]
    COUNTDOWN_STEP_MS = 330   # one fist pump per word
    SHAKE_HEIGHT = 12         # pixels
    POP_MS = 160              # reveal pop-in
    RESULT_HOLD_MS = 1800
    BANNER_DELAY_MS = 900     # let the final picks show before the banner

    OUTCOME_COLORS = {
        "PLAYER": (80, 230, 120),
        "CPU": (240, 80, 80),
        "TIE": (240, 210, 80),
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        btn_w, btn_h = 130, 60
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 80

        self.buttons = [
            ChoiceButton("ROCK", pygame.Rect(start_x, btn_y, btn_w, btn_h), (160, 50, 50), (200, 70, 70)),
            ChoiceButton("PAPER", pygame.Rect(start_x + btn_w + gap, btn_y, btn_w, btn_h), (40, 100, 170), (60, 130, 210)),
            ChoiceButton("SCISSORS", pygame.Rect(start_x + 2 * (btn_w + gap), btn_y, btn_w, btn_h), (180, 140, 30), (220, 180, 50)),
        ]

        panel_w, panel_h, panel_y = 104, 108, 92
        self.player_panel = pygame.Rect(0, 0, panel_w, panel_h)
        self.player_panel.midtop = (width // 2 - 105, panel_y)
        self.cpu_panel = pygame.Rect(0, 0, panel_w, panel_h)
        self.cpu_panel.midtop = (width // 2 + 105, panel_y)
        self.arena_icon_size = 58

        self.cpu = AdaptiveCPU(self.choices)

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)
        self.font_arena = pygame.font.SysFont(None, 32)
        self.font_banner = pygame.font.SysFont(None, 50)

        self.reset_match()

    # ---------- state ----------

    def reset_match(self):
        # Phases: idle -> countdown -> result -> idle, or countdown -> match_over
        self.phase = "idle"
        self.phase_start = pygame.time.get_ticks()

        self.player_choice = None
        self.cpu_choice = None
        self.last_outcome = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0
        self.match_winner = None  # "PLAYER" or "CPU"

        self.cpu.reset()

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"
        if self.BEATS[player] == cpu:
            return "PLAYER"
        return "CPU"

    def start_round(self, choice):
        self.player_choice = choice
        self.cpu_choice = None
        self.last_outcome = None
        self.result_text = self.COUNTDOWN_WORDS[0]
        self.result_color = (225, 225, 230)
        self.phase = "countdown"
        self.phase_start = pygame.time.get_ticks()

    def resolve_round(self):
        # CPU picks from past history only; this round's move is recorded afterwards
        self.cpu_choice = self.cpu.choose()
        self.cpu.record(self.player_choice)

        outcome = self.determine_winner(self.player_choice, self.cpu_choice)
        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = f"You Win! {self.player_choice} beats {self.cpu_choice}."
        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = f"You Lose! {self.cpu_choice} beats {self.player_choice}."
        else:
            self.result_text = f"It's a Draw! Both picked {self.player_choice}."

        self.last_outcome = outcome
        self.result_color = self.OUTCOME_COLORS[outcome]
        self.phase_start = pygame.time.get_ticks()

        if self.player_score >= self.WIN_SCORE:
            self.phase = "match_over"
            self.match_winner = "PLAYER"
        elif self.cpu_score >= self.WIN_SCORE:
            self.phase = "match_over"
            self.match_winner = "CPU"
        else:
            self.phase = "result"

    # ---------- loop hooks ----------

    def handle_event(self, event):
        if self.phase == "match_over":
            # Play is frozen; only R restarts
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_match()
            return

        if self.phase == "countdown":
            return  # no input mid-throw

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.start_round(btn.choice_name)
                    break

    def update(self):
        elapsed = pygame.time.get_ticks() - self.phase_start

        if self.phase == "countdown":
            step = elapsed // self.COUNTDOWN_STEP_MS
            if step >= len(self.COUNTDOWN_WORDS):
                self.resolve_round()
            else:
                self.result_text = self.COUNTDOWN_WORDS[step]

        elif self.phase == "result" and elapsed >= self.RESULT_HOLD_MS:
            self.phase = "idle"
            self.player_choice = None
            self.cpu_choice = None
            self.last_outcome = None
            self.result_text = "Make your move!"
            self.result_color = (190, 195, 205)

    # ---------- drawing ----------

    def render(self, screen):
        screen.fill((24, 28, 36))
        elapsed = pygame.time.get_ticks() - self.phase_start

        title_surf = self.font_title.render("Rock Paper Scissors", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 14))

        p_surf = self.font_hud.render(f"Player Score: {self.player_score}", True, (100, 180, 255))
        c_surf = self.font_hud.render(f"CPU Score: {self.cpu_score}", True, (255, 120, 120))
        screen.blit(p_surf, (35, 52))
        screen.blit(c_surf, (self.width - c_surf.get_width() - 35, 52))

        goal_surf = self.font_small.render(f"First to {self.WIN_SCORE} wins", True, (150, 158, 172))
        screen.blit(goal_surf, (self.width // 2 - goal_surf.get_width() // 2, 55))

        pygame.draw.line(screen, (45, 52, 66), (25, 82), (self.width - 25, 82), 2)

        self.render_panel(screen, self.player_panel, "YOU", "PLAYER", elapsed)
        self.render_panel(screen, self.cpu_panel, "CPU", "CPU", elapsed)

        vs_surf = self.font_hud.render("VS", True, (150, 158, 172))
        screen.blit(vs_surf, (self.width // 2 - vs_surf.get_width() // 2,
                              self.player_panel.centery - vs_surf.get_height() // 2))

        res_surf = self.font_arena.render(self.result_text, True, self.result_color)
        screen.blit(res_surf, (self.width // 2 - res_surf.get_width() // 2, 212))

        buttons_enabled = self.phase in ("idle", "result")
        for btn in self.buttons:
            btn.render(screen, enabled=buttons_enabled)

        if self.phase == "match_over" and elapsed >= self.BANNER_DELAY_MS:
            self.render_victory_banner(screen)

    def render_panel(self, screen, rect, label, side, elapsed):
        border = (60, 68, 84)
        if self.last_outcome in (side, "TIE"):
            border = self.OUTCOME_COLORS[self.last_outcome]

        pygame.draw.rect(screen, (32, 37, 48), rect, border_radius=10)
        pygame.draw.rect(screen, border, rect, width=2, border_radius=10)

        label_surf = self.font_small.render(label, True, (170, 178, 192))
        screen.blit(label_surf, (rect.centerx - label_surf.get_width() // 2, rect.top + 8))

        icon_center = (rect.centerx, rect.top + 66)

        if self.phase == "countdown":
            # Both fists pump once per countdown word
            t = (elapsed % self.COUNTDOWN_STEP_MS) / self.COUNTDOWN_STEP_MS
            offset = -round(math.sin(t * math.pi) * self.SHAKE_HEIGHT)
            draw_icon(screen, "ROCK", (icon_center[0], icon_center[1] + offset), self.arena_icon_size)
            return

        choice = self.player_choice if side == "PLAYER" else self.cpu_choice
        if choice is None:
            q_surf = self.font_banner.render("?", True, (110, 118, 135))
            screen.blit(q_surf, (icon_center[0] - q_surf.get_width() // 2,
                                 icon_center[1] - q_surf.get_height() // 2))
            return

        # Quick pop-in on reveal
        scale = 0.6 + 0.4 * min(1.0, elapsed / self.POP_MS)
        draw_icon(screen, choice, icon_center, round(self.arena_icon_size * scale))

    def render_victory_banner(self, screen):
        # Dim everything behind the banner
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        if self.match_winner == "PLAYER":
            headline = "YOU WIN THE MATCH!"
            accent = (80, 230, 120)
        else:
            headline = "CPU WINS THE MATCH!"
            accent = (240, 80, 80)

        banner = pygame.Rect(0, 0, 440, 160)
        banner.center = (self.width // 2, self.height // 2)
        pygame.draw.rect(screen, (32, 37, 48), banner, border_radius=12)
        pygame.draw.rect(screen, accent, banner, width=3, border_radius=12)

        head_surf = self.font_banner.render(headline, True, accent)
        score_surf = self.font_hud.render(
            f"Final Score  {self.player_score} - {self.cpu_score}", True, (225, 225, 230)
        )
        hint_surf = self.font_small.render("Press R to play again", True, (170, 178, 192))

        screen.blit(head_surf, (banner.centerx - head_surf.get_width() // 2, banner.top + 28))
        screen.blit(score_surf, (banner.centerx - score_surf.get_width() // 2, banner.top + 84))
        screen.blit(hint_surf, (banner.centerx - hint_surf.get_width() // 2, banner.top + 120))