"""
main.py — TSIS4 Snake Arcade
Run:  python main.py
Requires: pygame, psycopg2, PostgreSQL running (see config.py)
"""
import pygame
import sys

from config import WIDTH, HEIGHT, FPS
from settings_io import load_settings, save_settings
from game import SnakeGame, BG_COL, DKGRAY

WHITE  = (255, 255, 255)
GRAY   = ( 80,  80,  80)
YELLOW = (255, 220,   0)
RED    = (220,  40,  40)
CYAN   = (  0, 210, 210)
GREEN  = ( 30, 200,  80)
BLUE   = ( 50, 120, 220)
ORANGE = (255, 140,   0)
PURPLE = (160,  32, 240)

try:
    import db as _db
    _db.init_db()
    DB_AVAILABLE = True
except Exception as _e:
    print(f"[WARN] DB unavailable: {_e}. Scores will not be saved.")
    DB_AVAILABLE = False

# ── Palette ───────────────────────────────────────────────────────────────────
BLACK   = (  0,   0,   0)
ACCENT  = ( 80, 160, 255)

# ── Button widget ─────────────────────────────────────────────────────────────

class Button:
    def __init__(self, rect, text, color=ACCENT, text_color=WHITE, fsize=22):
        self.rect  = pygame.Rect(rect)
        self.text  = text
        self.color = color
        self.tcol  = text_color
        self.font  = pygame.font.SysFont("Arial", fsize, bold=True)

    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        col = tuple(min(255, c + 25) for c in self.color) \
              if self.rect.collidepoint(mx, my) else self.color
        pygame.draw.rect(surf, col, self.rect, border_radius=8)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=8)
        lbl = self.font.render(self.text, True, self.tcol)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def clicked(self, ev):
        return (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1
                and self.rect.collidepoint(ev.pos))


def draw_bg(surf):
    surf.fill(BG_COL)
    W, H = surf.get_size()
    for y in range(0, H, 30):
        pygame.draw.line(surf, (30, 30, 30), (0, y), (W, y))


def centre_text(surf, text, y, font, color=WHITE):
    lbl = font.render(text, True, color)
    surf.blit(lbl, lbl.get_rect(centerx=surf.get_width() // 2, y=y))


# ── Screens ───────────────────────────────────────────────────────────────────

class MainMenuScreen:
    def __init__(self):
        cx = WIDTH // 2
        self.font_title = pygame.font.SysFont("Arial", 54, bold=True)
        self.font_sub   = pygame.font.SysFont("Arial", 18)
        self.buttons = {
            "play":        Button((cx-100, 280, 200, 46), "PLAY"),
            "leaderboard": Button((cx-100, 338, 200, 46), "LEADERBOARD", GRAY),
            "settings":    Button((cx-100, 396, 200, 46), "SETTINGS", GRAY),
            "quit":        Button((cx-100, 454, 200, 46), "QUIT", RED),
        }

    def handle(self, ev):
        for k, b in self.buttons.items():
            if b.clicked(ev): return k
        return None

    def draw(self, surf):
        draw_bg(surf)
        centre_text(surf, "🐍 SNAKE", 100, self.font_title, YELLOW)
        centre_text(surf, "ARCADE — TSIS4", 165, self.font_sub, GRAY)
        for b in self.buttons.values(): b.draw(surf)


class UsernameScreen:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 34, bold=True)
        self.font_input = pygame.font.SysFont("Arial", 26)
        self.font_hint  = pygame.font.SysFont("Arial", 15)
        self.name  = ""
        self.rect  = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 - 20, 280, 44)
        self.btn_ok   = Button((WIDTH//2-90, HEIGHT//2+50,  180, 44), "START", (30, 160, 80))
        self.btn_back = Button((WIDTH//2-90, HEIGHT//2+105, 180, 44), "BACK",  GRAY)

    def handle(self, ev):
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN and self.name.strip():
                return ("start", self.name.strip())
            elif ev.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif ev.key == pygame.K_ESCAPE:
                return ("back", None)
            elif len(self.name) < 16 and ev.unicode.isprintable():
                self.name += ev.unicode
        if self.btn_ok.clicked(ev) and self.name.strip():
            return ("start", self.name.strip())
        if self.btn_back.clicked(ev):
            return ("back", None)
        return None

    def draw(self, surf):
        draw_bg(surf)
        centre_text(surf, "Enter Username", HEIGHT // 2 - 100,
                    self.font_title, YELLOW)
        pygame.draw.rect(surf, DKGRAY, self.rect, border_radius=6)
        pygame.draw.rect(surf, ACCENT,  self.rect, 2, border_radius=6)
        n = self.font_input.render(self.name + "|", True, WHITE)
        surf.blit(n, (self.rect.x + 8, self.rect.y + 8))
        h = self.font_hint.render("Type name then press ENTER or START", True, GRAY)
        surf.blit(h, h.get_rect(centerx=WIDTH // 2, y=HEIGHT // 2 + 22))
        self.btn_ok.draw(surf)
        self.btn_back.draw(surf)


class GameOverScreen:
    def __init__(self, score, level, personal_best):
        self.font_title = pygame.font.SysFont("Arial", 46, bold=True)
        self.font       = pygame.font.SysFont("Arial", 22)
        self.score  = score
        self.level  = level
        self.pb     = personal_best
        cx = WIDTH // 2
        self.btn_retry = Button((cx-100, HEIGHT-160, 200, 46), "RETRY",     (30,160,80))
        self.btn_menu  = Button((cx-100, HEIGHT-105, 200, 46), "MAIN MENU", GRAY)

    def handle(self, ev):
        if self.btn_retry.clicked(ev): return "retry"
        if self.btn_menu.clicked(ev):  return "menu"
        return None

    def draw(self, surf):
        draw_bg(surf)
        centre_text(surf, "GAME OVER", 90, self.font_title, RED)
        lines = [
            f"Score:        {self.score}",
            f"Level:        {self.level}",
            f"Personal Best: {self.pb or self.score}",
        ]
        for i, ln in enumerate(lines):
            lbl = self.font.render(ln, True, WHITE)
            surf.blit(lbl, lbl.get_rect(centerx=WIDTH//2, y=200+i*38))
        self.btn_retry.draw(surf)
        self.btn_menu.draw(surf)


class LeaderboardScreen:
    def __init__(self, rows):
        self.font_title = pygame.font.SysFont("Arial", 34, bold=True)
        self.font       = pygame.font.SysFont("Arial", 17)
        self.font_hdr   = pygame.font.SysFont("Arial", 15, bold=True)
        self.rows  = rows
        self.btn   = Button((WIDTH//2-80, HEIGHT-70, 160, 44), "BACK", GRAY)

    def handle(self, ev):
        if self.btn.clicked(ev): return "back"
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return "back"
        return None

    def draw(self, surf):
        draw_bg(surf)
        centre_text(surf, "TOP 10 LEADERBOARD", 55, self.font_title, YELLOW)
        hdr = self.font_hdr.render(
            f"{'#':<4}{'Username':<18}{'Score':>7}{'Level':>7}{'Date'}", True, YELLOW)
        surf.blit(hdr, hdr.get_rect(centerx=WIDTH//2, y=108))
        pygame.draw.line(surf, GRAY, (40, 128), (WIDTH-40, 128))
        for rank, name, score, level, played_at in self.rows:
            col = YELLOW if rank == 1 else WHITE
            date_str = played_at.strftime("%d/%m %H:%M") if played_at else ""
            row = self.font.render(
                f"{rank:<4}{name:<18}{score:>7}{level:>7}  {date_str}", True, col)
            surf.blit(row, row.get_rect(centerx=WIDTH//2, y=136+rank*26))
        if not self.rows:
            lbl = self.font.render("No scores yet — play a game!", True, GRAY)
            surf.blit(lbl, lbl.get_rect(centerx=WIDTH//2, y=200))
        self.btn.draw(surf)


COLOR_PRESETS = [
    ("Green",  [  0, 200,  80]),
    ("Blue",   [ 50, 120, 220]),
    ("Orange", [255, 140,   0]),
    ("Purple", [160,  32, 240]),
    ("White",  [220, 220, 220]),
]

class SettingsScreen:
    def __init__(self, settings):
        self.font_title = pygame.font.SysFont("Arial", 34, bold=True)
        self.font       = pygame.font.SysFont("Arial", 20, bold=True)
        self.settings   = dict(settings)
        self.btn_save   = Button((WIDTH//2-90, HEIGHT-80, 180, 44), "SAVE & BACK", (30,160,80))

    def handle(self, ev):
        if self.btn_save.clicked(ev):
            return ("save", self.settings)
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            return ("save", self.settings)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos
            cx = WIDTH // 2
            # grid toggle
            gr = pygame.Rect(cx+20, 178, 90, 34)
            if gr.collidepoint(mx, my):
                self.settings["grid_overlay"] = not self.settings["grid_overlay"]
            # sound toggle
            sr = pygame.Rect(cx+20, 230, 90, 34)
            if sr.collidepoint(mx, my):
                self.settings["sound"] = not self.settings["sound"]
            # colour presets
            for i, (_, rgb) in enumerate(COLOR_PRESETS):
                cr = pygame.Rect(cx - 120 + i * 52, 305, 44, 34)
                if cr.collidepoint(mx, my):
                    self.settings["snake_color"] = rgb
        return None

    def draw(self, surf):
        draw_bg(surf)
        centre_text(surf, "Settings", 70, self.font_title, YELLOW)

        def row(label, y, value, on_col, off_col):
            lbl = self.font.render(label, True, WHITE)
            surf.blit(lbl, (WIDTH//2 - 160, y + 6))
            cx = WIDTH // 2
            col = on_col if value else off_col
            r = pygame.Rect(cx+20, y, 90, 34)
            pygame.draw.rect(surf, col, r, border_radius=6)
            pygame.draw.rect(surf, WHITE, r, 2, border_radius=6)
            t = self.font.render("ON" if value else "OFF", True, WHITE)
            surf.blit(t, t.get_rect(center=r.center))

        row("Grid Overlay:", 178, self.settings.get("grid_overlay", True),
            (30,160,80), (120,30,30))
        row("Sound:",        230, self.settings.get("sound", True),
            (30,160,80), (120,30,30))

        lbl = self.font.render("Snake Color:", True, WHITE)
        surf.blit(lbl, (WIDTH//2 - 160, 312))
        cur_col = tuple(self.settings.get("snake_color", [0,200,80]))
        for i, (name, rgb) in enumerate(COLOR_PRESETS):
            cx = WIDTH // 2
            cr = pygame.Rect(cx - 120 + i * 52, 305, 44, 34)
            pygame.draw.rect(surf, tuple(rgb), cr, border_radius=6)
            if list(rgb) == self.settings.get("snake_color"):
                pygame.draw.rect(surf, WHITE, cr, 3, border_radius=6)

        self.btn_save.draw(surf)


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Arcade – TSIS4")
    clock  = pygame.time.Clock()

    settings = load_settings()
    state    = "menu"
    username = "Player"
    game     = None
    pb       = None

    screens = {
        "menu":     MainMenuScreen(),
        "username": UsernameScreen(),
        "settings": SettingsScreen(settings),
    }
    go_screen = None
    lb_screen = None

    while True:
        clock.tick(60)
        events = pygame.event.get()

        for ev in events:
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if state == "menu":
                res = screens["menu"].handle(ev)
                if res == "play":
                    screens["username"] = UsernameScreen()
                    state = "username"
                elif res == "leaderboard":
                    rows = _db.get_top10() if DB_AVAILABLE else []
                    lb_screen = LeaderboardScreen(rows)
                    state = "leaderboard"
                elif res == "settings":
                    screens["settings"] = SettingsScreen(settings)
                    state = "settings"
                elif res == "quit":
                    pygame.quit(); sys.exit()

            elif state == "username":
                res = screens["username"].handle(ev)
                if res:
                    action, val = res
                    if action == "start":
                        username = val
                        pb = _db.get_personal_best(username) if DB_AVAILABLE else None
                        game  = SnakeGame(settings, pb)
                        state = "game"
                    elif action == "back":
                        state = "menu"

            elif state == "game":
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    state = "menu"
                else:
                    game.handle_event(ev)

            elif state == "gameover":
                res = go_screen.handle(ev)
                if res == "retry":
                    pb   = _db.get_personal_best(username) if DB_AVAILABLE else None
                    game = SnakeGame(settings, pb)
                    state = "game"
                elif res == "menu":
                    state = "menu"

            elif state == "leaderboard":
                if lb_screen.handle(ev) == "back":
                    state = "menu"

            elif state == "settings":
                res = screens["settings"].handle(ev)
                if res:
                    _, new_s = res
                    settings.update(new_s)
                    save_settings(settings)
                    state = "menu"

        # ── draw ──────────────────────────────────────────────────────────
        if state == "menu":
            screens["menu"].draw(screen)

        elif state == "username":
            screens["username"].draw(screen)

        elif state == "game":
            game.update()
            game.draw(screen)
            if not game.alive:
                # auto-save to DB
                if DB_AVAILABLE:
                    try:
                        _db.save_result(username, game.score, game.level)
                        pb = _db.get_personal_best(username)
                    except Exception as e:
                        print(f"[DB] save failed: {e}")
                go_screen = GameOverScreen(game.score, game.level, pb)
                state = "gameover"

        elif state == "gameover":
            go_screen.draw(screen)

        elif state == "leaderboard":
            lb_screen.draw(screen)

        elif state == "settings":
            screens["settings"].draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()