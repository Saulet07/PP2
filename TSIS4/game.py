"""
game.py — Snake game logic for TSIS4.
Handles: snake movement, food (normal + poison), power-ups,
         obstacles (from level 3), collision, scoring, levelling.
"""
import pygame
import random
import math
from config import CELL, COLS, ROWS, PANEL_H, LEVEL_SCORE_STEP, MAX_OBSTACLES

# ── colours ───────────────────────────────────────────────────────────────────
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
GRAY     = ( 80,  80,  80)
DKGRAY   = ( 30,  30,  30)
BG_COL   = ( 18,  18,  18)
GRID_COL = ( 35,  35,  35)
RED      = (220,  40,  40)
ORANGE   = (255, 140,   0)
YELLOW   = (255, 220,   0)
CYAN     = (  0, 210, 210)
BLUE     = ( 50, 120, 220)
PURPLE   = (160,  32, 240)
POISON_COL   = (140,   0,   0)   # dark red
OBSTACLE_COL = ( 90,  80,  60)

# Power-up visual colours
PU_COLS = {
    "speed":  ORANGE,
    "slow":   CYAN,
    "shield": PURPLE,
}
PU_ICONS = {"speed": "⚡", "slow": "🐢", "shield": "🛡"}   # fallback text below

# Directions
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)
OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def rand_cell(blocked: set) -> tuple[int, int]:
    """Return a random grid cell not in blocked."""
    while True:
        c = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if c not in blocked:
            return c


class PowerUpItem:
    FIELD_TIMEOUT_MS = 8000   # 8 s on-field timeout

    def __init__(self, kind: str, pos: tuple):
        self.kind     = kind
        self.pos      = pos
        self.spawned  = pygame.time.get_ticks()

    def expired(self) -> bool:
        return pygame.time.get_ticks() - self.spawned > self.FIELD_TIMEOUT_MS


class SnakeGame:
    def __init__(self, settings: dict, personal_best: int | None = None):
        self.settings      = settings
        self.personal_best = personal_best

        # Snake
        start_x = COLS // 2
        start_y = ROWS // 2
        self.snake   = [(start_x, start_y),
                        (start_x - 1, start_y),
                        (start_x - 2, start_y)]
        self.direction  = RIGHT
        self.next_dir   = RIGHT
        self.alive      = True
        self.score      = 0
        self.level      = 1

        # Active power-up state
        self.active_pu        = None   # "speed" | "slow" | "shield"
        self.active_pu_end_ms = 0

        # Shield triggers once then disappears
        self.shield_ready = False

        # Items on field
        self.food        = None
        self.poison      = None
        self.powerup     = None   # PowerUpItem | None
        self.obstacles   = set()

        # Fonts
        self.font_sm  = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_med = pygame.font.SysFont("Arial", 18, bold=True)

        # Tick timing
        self.last_tick = pygame.time.get_ticks()
        self._place_obstacles()
        self._spawn_food()
        self._spawn_poison()

    # ── helpers ────────────────────────────────────────────────────────────

    def _occupied(self) -> set:
        s = set(self.snake) | self.obstacles
        if self.food:    s.add(self.food)
        if self.poison:  s.add(self.poison)
        if self.powerup: s.add(self.powerup.pos)
        return s

    def _spawn_food(self):
        self.food = rand_cell(self._occupied())

    def _spawn_poison(self):
        # 30 % chance to have poison on field
        if random.random() < 0.3:
            self.poison = rand_cell(self._occupied())
        else:
            self.poison = None

    def _place_obstacles(self):
        """Randomly place obstacle blocks from level 3, never trapping the snake."""
        self.obstacles = set()
        if self.level < 3:
            return
        count = min(MAX_OBSTACLES, (self.level - 2) * 3)
        head  = self.snake[0]
        for _ in range(count * 10):   # attempts
            if len(self.obstacles) >= count:
                break
            c = rand_cell(set(self.snake) | self.obstacles)
            # keep a clear 2-cell radius around head to avoid instant trap
            if abs(c[0] - head[0]) <= 2 and abs(c[1] - head[1]) <= 2:
                continue
            self.obstacles.add(c)

    def _maybe_spawn_powerup(self):
        """Spawn a power-up with 15% chance if none is currently on field."""
        if self.powerup is None and random.random() < 0.15:
            kind = random.choice(["speed", "slow", "shield"])
            pos  = rand_cell(self._occupied())
            self.powerup = PowerUpItem(kind, pos)

    def _tick_speed(self) -> int:
        """Return ms per tick based on level and active power-up."""
        base = max(60, 200 - (self.level - 1) * 15)
        if self.active_pu == "speed":
            base = max(40, base // 2)
        elif self.active_pu == "slow":
            base = int(base * 1.8)
        return base

    # ── input ──────────────────────────────────────────────────────────────

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            mapping = {
                pygame.K_UP:    UP,
                pygame.K_w:     UP,
                pygame.K_DOWN:  DOWN,
                pygame.K_s:     DOWN,
                pygame.K_LEFT:  LEFT,
                pygame.K_a:     LEFT,
                pygame.K_RIGHT: RIGHT,
                pygame.K_d:     RIGHT,
            }
            if event.key in mapping:
                new = mapping[event.key]
                if new != OPPOSITES.get(self.direction):
                    self.next_dir = new

    # ── update ─────────────────────────────────────────────────────────────

    def update(self):
        if not self.alive:
            return

        now = pygame.time.get_ticks()

        # expire active power-up
        if self.active_pu in ("speed", "slow"):
            if now >= self.active_pu_end_ms:
                self.active_pu = None

        # expire field power-up
        if self.powerup and self.powerup.expired():
            self.powerup = None

        # tick?
        if now - self.last_tick < self._tick_speed():
            return
        self.last_tick = now

        self.direction = self.next_dir
        hx, hy = self.snake[0]
        dx, dy  = self.direction
        new_head = ((hx + dx) % COLS, (hy + dy) % ROWS)

        # wall / self collision
        if new_head in set(self.snake[:-1]) or new_head in self.obstacles:
            if self.shield_ready:
                self.shield_ready = False
                self.active_pu    = None
                # teleport snake head past obstacle — skip the move
                return
            else:
                self.alive = False
                return

        self.snake.insert(0, new_head)

        ate = False

        if new_head == self.food:
            ate = True
            self.score += 1
            self._spawn_food()
            self._spawn_poison()
            self._maybe_spawn_powerup()
            # level up?
            new_level = self.score // LEVEL_SCORE_STEP + 1
            if new_level > self.level:
                self.level = new_level
                self._place_obstacles()

        elif new_head == self.poison:
            # shorten by 2 segments (remove tail twice)
            self.poison = None
            self.snake.pop()   # normal tail removal already done below
            if len(self.snake) <= 1:
                self.alive = False
                return
            self.snake.pop()   # second removal
            # re-spawn poison chance
            self._spawn_poison()

        elif self.powerup and new_head == self.powerup.pos:
            kind = self.powerup.kind
            self.powerup = None
            self.active_pu = kind
            if kind in ("speed", "slow"):
                self.active_pu_end_ms = pygame.time.get_ticks() + 5000
            elif kind == "shield":
                self.shield_ready = True
                self.active_pu_end_ms = 0  # until triggered

        if not ate:
            self.snake.pop()

    # ── draw ───────────────────────────────────────────────────────────────

    def draw(self, surf: pygame.Surface):
        W = surf.get_width()

        # background
        surf.fill(BG_COL)

        # grid overlay
        if self.settings.get("grid_overlay", True):
            for gx in range(0, COLS * CELL, CELL):
                pygame.draw.line(surf, GRID_COL,
                                 (gx, PANEL_H), (gx, surf.get_height()))
            for gy in range(PANEL_H, PANEL_H + ROWS * CELL, CELL):
                pygame.draw.line(surf, GRID_COL, (0, gy), (W, gy))

        # obstacles
        for ox, oy in self.obstacles:
            r = pygame.Rect(ox * CELL, PANEL_H + oy * CELL, CELL, CELL)
            pygame.draw.rect(surf, OBSTACLE_COL, r)
            pygame.draw.rect(surf, WHITE, r, 1)

        # food
        if self.food:
            fx, fy = self.food
            r = pygame.Rect(fx * CELL + 2, PANEL_H + fy * CELL + 2, CELL - 4, CELL - 4)
            pygame.draw.ellipse(surf, YELLOW, r)

        # poison food
        if self.poison:
            px, py = self.poison
            r = pygame.Rect(px * CELL + 2, PANEL_H + py * CELL + 2, CELL - 4, CELL - 4)
            pygame.draw.ellipse(surf, POISON_COL, r)
            pygame.draw.ellipse(surf, RED, r, 2)
            lbl = self.font_sm.render("☠", True, RED)
            surf.blit(lbl, lbl.get_rect(center=r.center))

        # power-up on field
        if self.powerup:
            pu = self.powerup
            px, py = pu.pos
            r = pygame.Rect(px * CELL + 1, PANEL_H + py * CELL + 1, CELL - 2, CELL - 2)
            # pulsing
            pulse = abs(math.sin(pygame.time.get_ticks() / 300)) * 40
            col   = tuple(min(255, c + int(pulse)) for c in PU_COLS[pu.kind])
            pygame.draw.rect(surf, col, r, border_radius=4)
            pygame.draw.rect(surf, WHITE, r, 1, border_radius=4)
            lbl = self.font_sm.render(pu.kind[0].upper(), True, WHITE)
            surf.blit(lbl, lbl.get_rect(center=r.center))
            # timeout bar
            elapsed = pygame.time.get_ticks() - pu.spawned
            pct     = max(0.0, 1.0 - elapsed / PowerUpItem.FIELD_TIMEOUT_MS)
            pygame.draw.rect(surf, WHITE,
                             (px * CELL, PANEL_H + py * CELL + CELL - 3,
                              int(CELL * pct), 3))

        # snake
        snake_col = tuple(self.settings.get("snake_color", [0, 200, 80]))
        for i, (sx, sy) in enumerate(self.snake):
            r = pygame.Rect(sx * CELL + 1, PANEL_H + sy * CELL + 1,
                            CELL - 2, CELL - 2)
            shade = max(60, 255 - i * 8)
            col   = tuple(int(c * shade / 255) for c in snake_col)
            pygame.draw.rect(surf, col, r, border_radius=3)
            if i == 0:   # eyes
                pygame.draw.circle(surf, WHITE,
                                   (r.x + 5,  r.y + 5), 3)
                pygame.draw.circle(surf, WHITE,
                                   (r.right - 5, r.y + 5), 3)
                pygame.draw.circle(surf, BLACK,
                                   (r.x + 5,  r.y + 5), 1)
                pygame.draw.circle(surf, BLACK,
                                   (r.right - 5, r.y + 5), 1)

        # shield glow around head
        if self.shield_ready:
            hx, hy = self.snake[0]
            cr = pygame.Rect(hx * CELL - 2, PANEL_H + hy * CELL - 2,
                             CELL + 4, CELL + 4)
            pygame.draw.rect(surf, PURPLE, cr, 2, border_radius=5)

        self._draw_hud(surf)

    def _draw_hud(self, surf):
        W = surf.get_width()
        pygame.draw.rect(surf, DKGRAY, (0, 0, W, PANEL_H))

        def txt(s, x, y, col=WHITE, font=None):
            f = font or self.font_med
            lbl = f.render(s, True, col)
            surf.blit(lbl, (x, y))

        txt(f"Score: {self.score}", 8, 8)
        txt(f"Level: {self.level}", 8, 30, YELLOW)

        # personal best
        pb = self.personal_best or 0
        best_col = CYAN if self.score > pb else GRAY
        pb_val   = max(self.score, pb)
        txt(f"Best: {pb_val}", W // 2 - 50, 8, best_col)

        # active power-up
        if self.active_pu:
            col = PU_COLS.get(self.active_pu, WHITE)
            label = self.active_pu.upper()
            if self.active_pu in ("speed", "slow"):
                remaining = max(0, self.active_pu_end_ms - pygame.time.get_ticks())
                label += f" {remaining // 1000 + 1}s"
            elif self.active_pu == "shield":
                label = "SHIELD ✓"
            txt(label, W // 2 - 50, 30, col, self.font_sm)

        txt(f"Len: {len(self.snake)}", W - 90, 8)
        txt(f"Lvl {self.level}", W - 90, 30, (180, 180, 180), self.font_sm)