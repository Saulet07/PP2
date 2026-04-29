import pygame

WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
GRAY    = (100, 100, 100)
DKGRAY  = ( 40,  40,  40)
RED     = (220,  30,  30)
GREEN   = ( 30, 200,  80)
YELLOW  = (255, 220,   0)
ORANGE  = (255, 140,   0)
CYAN    = (  0, 210, 210)
BLUE    = ( 50, 120, 220)
BG      = ( 20,  20,  40)
ACCENT  = ( 80, 160, 255)

CAR_COLOR_OPTIONS = ["red", "blue", "green", "yellow"]
CAR_DISPLAY_COLS  = {
    "red":    (220,  30,  30),
    "blue":   ( 30, 100, 220),
    "green":  ( 30, 200,  80),
    "yellow": (255, 220,   0),
}
DIFFICULTY_OPTIONS = ["easy", "medium", "hard"]


# ── generic button ────────────────────────────────────────────────────────────

class Button:
    def __init__(self, rect, text, color=ACCENT, text_color=WHITE, font_size=24):
        self.rect       = pygame.Rect(rect)
        self.text       = text
        self.color      = color
        self.text_color = text_color
        self.font       = pygame.font.SysFont("Arial", font_size, bold=True)
        self.hovered    = False

    def draw(self, surf):
        col = tuple(min(255, c + 30) for c in self.color) if self.hovered else self.color
        pygame.draw.rect(surf, col, self.rect, border_radius=8)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=8)
        lbl = self.font.render(self.text, True, self.text_color)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


def draw_title(surf, text, y, font):
    lbl = font.render(text, True, YELLOW)
    surf.blit(lbl, lbl.get_rect(centerx=surf.get_width() // 2, y=y))


def draw_bg(surf):
    surf.fill(BG)
    W, H = surf.get_size()
    for i in range(0, H, 40):
        alpha = 30
        pygame.draw.line(surf, (255, 255, 255), (80, i), (W - 80, i), 1)


# ── Main Menu ─────────────────────────────────────────────────────────────────

class MainMenu:
    def __init__(self, width, height):
        W, H = width, height
        self.font_title = pygame.font.SysFont("Arial", 52, bold=True)
        self.font_sub   = pygame.font.SysFont("Arial", 18)
        cx = W // 2
        self.buttons = {
            "play":        Button((cx - 100, 260, 200, 48), "PLAY"),
            "leaderboard": Button((cx - 100, 320, 200, 48), "LEADERBOARD", GRAY),
            "settings":    Button((cx - 100, 380, 200, 48), "SETTINGS", GRAY),
            "quit":        Button((cx - 100, 440, 200, 48), "QUIT", RED),
        }

    def handle(self, event):
        for key, btn in self.buttons.items():
            if btn.clicked(event):
                return key
        return None

    def draw(self, surf):
        draw_bg(surf)
        W = surf.get_width()
        # title
        t = self.font_title.render("RACER", True, YELLOW)
        surf.blit(t, t.get_rect(centerx=W // 2, y=80))
        t2 = self.font_title.render("ARCADE", True, ORANGE)
        surf.blit(t2, t2.get_rect(centerx=W // 2, y=145))
        sub = self.font_sub.render("TSIS3 Edition", True, (180, 180, 180))
        surf.blit(sub, sub.get_rect(centerx=W // 2, y=205))
        # decorative cars
        pygame.draw.rect(surf, (220, 30, 30), (W // 2 - 18, 225, 36, 26), border_radius=5)
        mouse = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.update(mouse)
            btn.draw(surf)


# ── Username entry ────────────────────────────────────────────────────────────

class UsernameScreen:
    def __init__(self, width, height):
        W, H = width, height
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_input = pygame.font.SysFont("Arial", 28)
        self.font_hint  = pygame.font.SysFont("Arial", 16)
        self.name       = ""
        self.active     = True
        cx = W // 2
        self.btn_ok   = Button((cx - 80, H // 2 + 70, 160, 44), "START RACE", GREEN)
        self.btn_back = Button((cx - 80, H // 2 + 125, 160, 44), "BACK", GRAY)
        self.rect     = pygame.Rect(cx - 140, H // 2 - 20, 280, 44)
        self.W, self.H = W, H

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.name.strip():
                return ("start", self.name.strip())
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == pygame.K_ESCAPE:
                return ("back", None)
            elif len(self.name) < 16 and event.unicode.isprintable():
                self.name += event.unicode
        if self.btn_ok.clicked(event) and self.name.strip():
            return ("start", self.name.strip())
        if self.btn_back.clicked(event):
            return ("back", None)
        return None

    def draw(self, surf):
        draw_bg(surf)
        W, H = self.W, self.H
        draw_title(surf, "Enter Your Name", H // 2 - 100,
                   self.font_title)
        # input box
        pygame.draw.rect(surf, DKGRAY, self.rect, border_radius=6)
        pygame.draw.rect(surf, ACCENT, self.rect, 2, border_radius=6)
        name_surf = self.font_input.render(self.name + "|", True, WHITE)
        surf.blit(name_surf, (self.rect.x + 8, self.rect.y + 8))
        hint = self.font_hint.render("Type your name, then press ENTER or START", True, GRAY)
        surf.blit(hint, hint.get_rect(centerx=W // 2, y=H // 2 + 40))
        mouse = pygame.mouse.get_pos()
        for btn in (self.btn_ok, self.btn_back):
            btn.update(mouse)
            btn.draw(surf)


# ── Settings ──────────────────────────────────────────────────────────────────

class SettingsScreen:
    def __init__(self, width, height, settings):
        W, H = width, height
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font       = pygame.font.SysFont("Arial", 20, bold=True)
        self.settings   = dict(settings)
        self.W, self.H  = W, H
        cx = W // 2
        self.btn_back = Button((cx - 80, H - 80, 160, 44), "BACK & SAVE", GREEN)

    def handle(self, event):
        if self.btn_back.clicked(event):
            return ("save", self.settings)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return ("save", self.settings)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # sound toggle
            sr = pygame.Rect(self.W // 2 + 20, 180, 100, 36)
            if sr.collidepoint(mx, my):
                self.settings["sound"] = not self.settings["sound"]
            # car color
            for i, col in enumerate(CAR_COLOR_OPTIONS):
                cr = pygame.Rect(self.W // 2 - 130 + i * 70, 260, 52, 36)
                if cr.collidepoint(mx, my):
                    self.settings["car_color"] = col
            # difficulty
            for i, diff in enumerate(DIFFICULTY_OPTIONS):
                dr = pygame.Rect(self.W // 2 - 130 + i * 95, 340, 85, 36)
                if dr.collidepoint(mx, my):
                    self.settings["difficulty"] = diff
        return None

    def draw(self, surf):
        draw_bg(surf)
        W, H = self.W, self.H
        draw_title(surf, "Settings", 80, self.font_title)

        # Sound
        lbl = self.font.render("Sound:", True, WHITE)
        surf.blit(lbl, (W // 2 - 160, 188))
        on_col  = GREEN if self.settings["sound"] else GRAY
        off_col = RED   if not self.settings["sound"] else GRAY
        pygame.draw.rect(surf, on_col,  (W // 2 + 20,  180, 45, 36), border_radius=6)
        pygame.draw.rect(surf, off_col, (W // 2 + 70,  180, 45, 36), border_radius=6)
        pygame.draw.rect(surf, WHITE,   (W // 2 + 20,  180, 45, 36), 2, border_radius=6)
        pygame.draw.rect(surf, WHITE,   (W // 2 + 70,  180, 45, 36), 2, border_radius=6)
        on_t  = self.font.render("ON",  True, WHITE)
        off_t = self.font.render("OFF", True, WHITE)
        surf.blit(on_t,  on_t.get_rect(center=(W // 2 + 42, 198)))
        surf.blit(off_t, off_t.get_rect(center=(W // 2 + 92, 198)))

        # Car color
        lbl2 = self.font.render("Car Color:", True, WHITE)
        surf.blit(lbl2, (W // 2 - 160, 268))
        for i, col in enumerate(CAR_COLOR_OPTIONS):
            cx = W // 2 - 130 + i * 70
            cr = pygame.Rect(cx, 260, 52, 36)
            pygame.draw.rect(surf, CAR_DISPLAY_COLS[col], cr, border_radius=6)
            if self.settings["car_color"] == col:
                pygame.draw.rect(surf, WHITE, cr, 3, border_radius=6)

        # Difficulty
        lbl3 = self.font.render("Difficulty:", True, WHITE)
        surf.blit(lbl3, (W // 2 - 160, 348))
        diff_cols = {"easy": GREEN, "medium": YELLOW, "hard": RED}
        for i, diff in enumerate(DIFFICULTY_OPTIONS):
            dx = W // 2 - 130 + i * 95
            dr = pygame.Rect(dx, 340, 85, 36)
            col = diff_cols[diff]
            if self.settings["difficulty"] == diff:
                pygame.draw.rect(surf, col, dr, border_radius=6)
            else:
                pygame.draw.rect(surf, DKGRAY, dr, border_radius=6)
            pygame.draw.rect(surf, col, dr, 2, border_radius=6)
            dt = self.font.render(diff.capitalize(), True, WHITE)
            surf.blit(dt, dt.get_rect(center=dr.center))

        mouse = pygame.mouse.get_pos()
        self.btn_back.update(mouse)
        self.btn_back.draw(surf)


# ── Game Over ─────────────────────────────────────────────────────────────────

class GameOverScreen:
    def __init__(self, width, height, score, distance, coins, finished=False):
        W, H = width, height
        self.font_title = pygame.font.SysFont("Arial", 44, bold=True)
        self.font       = pygame.font.SysFont("Arial", 22)
        self.score      = score
        self.distance   = distance
        self.coins      = coins
        self.finished   = finished
        self.W, self.H  = W, H
        cx = W // 2
        self.btn_retry = Button((cx - 100, H - 170, 200, 46), "RETRY", GREEN)
        self.btn_menu  = Button((cx - 100, H - 115, 200, 46), "MAIN MENU", GRAY)

    def handle(self, event):
        if self.btn_retry.clicked(event):
            return "retry"
        if self.btn_menu.clicked(event):
            return "menu"
        return None

    def draw(self, surf):
        draw_bg(surf)
        W, H = self.W, self.H
        title = "FINISH!" if self.finished else "GAME OVER"
        col   = GREEN    if self.finished else RED
        t = self.font_title.render(title, True, col)
        surf.blit(t, t.get_rect(centerx=W // 2, y=100))

        lines = [
            f"Score:    {self.score}",
            f"Distance: {int(self.distance)} / 3000 m",
        ]
        for i, ln in enumerate(lines):
            lbl = self.font.render(ln, True, WHITE)
            surf.blit(lbl, lbl.get_rect(centerx=W // 2, y=200 + i * 36))

        mouse = pygame.mouse.get_pos()
        for btn in (self.btn_retry, self.btn_menu):
            btn.update(mouse)
            btn.draw(surf)


# ── Leaderboard ───────────────────────────────────────────────────────────────

class LeaderboardScreen:
    def __init__(self, width, height, entries):
        W, H = width, height
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font       = pygame.font.SysFont("Arial", 20)
        self.font_hdr   = pygame.font.SysFont("Arial", 18, bold=True)
        self.entries    = entries
        self.W, self.H  = W, H
        self.btn_back   = Button((W // 2 - 80, H - 70, 160, 44), "BACK", GRAY)

    def handle(self, event):
        if self.btn_back.clicked(event):
            return "back"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, surf):
        draw_bg(surf)
        W, H = self.W, self.H
        draw_title(surf, "TOP 10 LEADERBOARD", 60, self.font_title)

        # header
        hdr = self.font_hdr.render(
            f"{'#':<4} {'Name':<16} {'Score':>8} {'Dist':>7}", True, YELLOW)
        surf.blit(hdr, (W // 2 - hdr.get_width() // 2, 120))
        pygame.draw.line(surf, GRAY,
                         (W // 2 - 160, 144), (W // 2 + 160, 144), 1)

        row_cols = [WHITE, (200, 200, 200)]
        for i, entry in enumerate(self.entries[:10]):
            col = YELLOW if i == 0 else row_cols[i % 2]
            row = self.font.render(
                f"{i+1:<4} {entry['name']:<16} {entry['score']:>8} {entry['distance']:>6}m",
                True, col)
            surf.blit(row, (W // 2 - row.get_width() // 2, 152 + i * 28))

        if not self.entries:
            empty = self.font.render("No scores yet — play a game!", True, GRAY)
            surf.blit(empty, empty.get_rect(centerx=W // 2, y=200))

        mouse = pygame.mouse.get_pos()
        self.btn_back.update(mouse)
        self.btn_back.draw(surf)