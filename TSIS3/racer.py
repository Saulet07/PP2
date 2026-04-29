import pygame
import random
import math

# ── colours ───────────────────────────────────────────────────────────────────
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
GRAY    = (100, 100, 100)
DKGRAY  = ( 50,  50,  50)
RED     = (220,  30,  30)
BLUE    = ( 30, 100, 220)
GREEN   = ( 30, 200,  80)
YELLOW  = (255, 220,   0)
ORANGE  = (255, 140,   0)
CYAN    = (  0, 220, 220)
PURPLE  = (160,  32, 240)
BROWN   = (139,  69,  19)
ROAD_C  = ( 70,  70,  70)
LANE_C  = (200, 200,   0)
GRASS_C = ( 34, 139,  34)
SKY_C   = ( 30,  30,  60)

CAR_COLORS = {
    "red":    RED,
    "blue":   BLUE,
    "green":  GREEN,
    "yellow": YELLOW,
}

# ── layout ────────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 480, 700
ROAD_LEFT   = 80
ROAD_RIGHT  = 400
ROAD_W      = ROAD_RIGHT - ROAD_LEFT          # 320
NUM_LANES   = 4
LANE_W      = ROAD_W // NUM_LANES             # 80

PLAYER_W, PLAYER_H = 36, 60
ENEMY_W,  ENEMY_H  = 36, 56
OBS_W,    OBS_H    = 38, 38
PU_SIZE             = 32

SCROLL_SPEED_BASE = 5
FINISH_DISTANCE   = 3000          # pixels of distance to finish

# ── helpers ───────────────────────────────────────────────────────────────────

def lane_x(lane):
    """Centre x of lane 0-3."""
    return ROAD_LEFT + lane * LANE_W + LANE_W // 2


def rand_lane():
    return random.randint(0, NUM_LANES - 1)


def difficulty_multipliers(diff):
    return {"easy": 0.7, "medium": 1.0, "hard": 1.5}.get(diff, 1.0)


# ── Road markings ─────────────────────────────────────────────────────────────

class RoadStripe:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, speed):
        self.y += speed
        if self.y > HEIGHT + 20:
            self.y -= HEIGHT + 40

    def draw(self, surf):
        pygame.draw.rect(surf, LANE_C, (self.x - 2, self.y, 4, 30))


# ── Player ────────────────────────────────────────────────────────────────────

class Player:
    def __init__(self, car_color="red"):
        self.lane   = 1
        self.x      = float(lane_x(self.lane))
        self.y      = float(HEIGHT - 120)
        self.w      = PLAYER_W
        self.h      = PLAYER_H
        self.color  = CAR_COLORS.get(car_color, RED)
        self.shield = False
        self.nitro  = False
        self.nitro_timer  = 0
        self.shield_active = False
        self.move_anim = 0      # smooth lane switch

    def move(self, direction):
        new_lane = self.lane + direction
        if 0 <= new_lane < NUM_LANES:
            self.lane = new_lane

    def update(self):
        target_x = float(lane_x(self.lane))
        self.x += (target_x - self.x) * 0.25   # smooth slide
        if self.nitro_timer > 0:
            self.nitro_timer -= 1
            if self.nitro_timer == 0:
                self.nitro = False

    def activate_nitro(self, duration):
        self.nitro = True
        self.nitro_timer = duration

    def rect(self):
        return pygame.Rect(int(self.x) - self.w // 2, int(self.y) - self.h // 2,
                           self.w, self.h)

    def draw(self, surf):
        r = self.rect()
        # body
        pygame.draw.rect(surf, self.color, r, border_radius=6)
        # windshield
        ws = pygame.Rect(r.x + 5, r.y + 8, r.w - 10, 14)
        pygame.draw.rect(surf, (180, 230, 255), ws, border_radius=3)
        # wheels
        for wx, wy in [(r.x - 4, r.y + 8), (r.right, r.y + 8),
                       (r.x - 4, r.bottom - 20), (r.right, r.bottom - 20)]:
            pygame.draw.rect(surf, BLACK, (wx, wy, 6, 12), border_radius=2)
        # shield glow
        if self.shield_active:
            pygame.draw.ellipse(surf, CYAN,
                                r.inflate(12, 12), 3)
        # nitro flame
        if self.nitro:
            for i in range(3):
                fx = r.centerx + random.randint(-8, 8)
                fy = r.bottom + random.randint(4, 16)
                pygame.draw.circle(surf, ORANGE, (fx, fy), random.randint(4, 8))


# ── Enemy car ─────────────────────────────────────────────────────────────────

ENEMY_COLORS = [BLUE, PURPLE, ORANGE, (180, 0, 0), (0, 150, 150)]

class Enemy:
    def __init__(self, speed_mult=1.0):
        self.lane  = rand_lane()
        self.x     = float(lane_x(self.lane))
        self.y     = float(-ENEMY_H)
        self.w     = ENEMY_W
        self.h     = ENEMY_H
        self.color = random.choice(ENEMY_COLORS)
        self.speed_extra = random.uniform(0.5, 2.0) * speed_mult

    def update(self, scroll_speed):
        self.y += scroll_speed + self.speed_extra

    def rect(self):
        return pygame.Rect(int(self.x) - self.w // 2, int(self.y) - self.h // 2,
                           self.w, self.h)

    def draw(self, surf):
        r = self.rect()
        pygame.draw.rect(surf, self.color, r, border_radius=5)
        ws = pygame.Rect(r.x + 5, r.y + 10, r.w - 10, 12)
        pygame.draw.rect(surf, (180, 230, 255), ws, border_radius=3)
        for wx, wy in [(r.x - 4, r.y + 6), (r.right, r.y + 6),
                       (r.x - 4, r.bottom - 18), (r.right, r.bottom - 18)]:
            pygame.draw.rect(surf, BLACK, (wx, wy, 6, 10), border_radius=2)


# ── Road obstacle (oil spill / pothole / barrier) ─────────────────────────────

OBS_TYPES = ["oil", "pothole", "barrier"]

class Obstacle:
    def __init__(self):
        self.type  = random.choice(OBS_TYPES)
        self.lane  = rand_lane()
        self.x     = float(lane_x(self.lane))
        self.y     = float(-OBS_H)
        self.w     = OBS_W
        self.h     = OBS_H

    def update(self, scroll_speed):
        self.y += scroll_speed

    def rect(self):
        return pygame.Rect(int(self.x) - self.w // 2, int(self.y) - self.h // 2,
                           self.w, self.h)

    def draw(self, surf):
        r = self.rect()
        if self.type == "oil":
            pygame.draw.ellipse(surf, (30, 30, 80), r)
            pygame.draw.ellipse(surf, (60, 60, 160), r.inflate(-8, -8))
        elif self.type == "pothole":
            pygame.draw.ellipse(surf, DKGRAY, r)
            pygame.draw.ellipse(surf, BLACK, r.inflate(-10, -10))
        else:   # barrier
            pygame.draw.rect(surf, ORANGE, r, border_radius=4)
            pygame.draw.rect(surf, BLACK, r, 2, border_radius=4)
            pygame.draw.line(surf, BLACK, (r.x, r.centery), (r.right, r.centery), 3)


# ── Power-up ──────────────────────────────────────────────────────────────────

PU_TYPES = ["nitro", "shield", "repair"]
PU_COLORS = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
PU_ICONS  = {"nitro": "N", "shield": "S", "repair": "R"}

class PowerUp:
    TIMEOUT = 300   # frames before it disappears

    def __init__(self):
        self.type  = random.choice(PU_TYPES)
        self.lane  = rand_lane()
        self.x     = float(lane_x(self.lane))
        self.y     = float(-PU_SIZE)
        self.size  = PU_SIZE
        self.timer = self.TIMEOUT
        self.pulse = 0

    def update(self, scroll_speed):
        self.y    += scroll_speed
        self.timer -= 1
        self.pulse  = (self.pulse + 5) % 360

    def expired(self):
        return self.timer <= 0

    def rect(self):
        return pygame.Rect(int(self.x) - self.size // 2,
                           int(self.y) - self.size // 2,
                           self.size, self.size)

    def draw(self, surf, font):
        r   = self.rect()
        col = PU_COLORS[self.type]
        alpha = int(180 + 75 * math.sin(math.radians(self.pulse)))
        pygame.draw.rect(surf, col, r, border_radius=8)
        pygame.draw.rect(surf, WHITE, r, 2, border_radius=8)
        lbl = font.render(PU_ICONS[self.type], True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=r.center))
        # remaining-time bar
        pct = self.timer / self.TIMEOUT
        bar_w = int(self.size * pct)
        pygame.draw.rect(surf, WHITE, (r.x, r.bottom + 2, bar_w, 3))


# ── Road event (moving barrier / speed bump / nitro strip) ────────────────────

class RoadEvent:
    DURATION = 180

    def __init__(self):
        choices = ["moving_barrier", "speed_bump", "nitro_strip"]
        self.kind   = random.choice(choices)
        self.lane   = rand_lane()
        self.x      = float(lane_x(self.lane))
        self.y      = float(-40)
        self.timer  = self.DURATION
        self.dir    = 1 if random.random() > 0.5 else -1
        self.w      = LANE_W - 8
        self.h      = 20

    def update(self, scroll_speed):
        self.y    += scroll_speed
        self.timer -= 1
        if self.kind == "moving_barrier":
            self.x += self.dir * 2
            if self.x < ROAD_LEFT + self.w // 2 or self.x > ROAD_RIGHT - self.w // 2:
                self.dir *= -1

    def rect(self):
        return pygame.Rect(int(self.x) - self.w // 2,
                           int(self.y) - self.h // 2,
                           self.w, self.h)

    def draw(self, surf):
        r = self.rect()
        if self.kind == "moving_barrier":
            pygame.draw.rect(surf, RED, r, border_radius=4)
            for i in range(0, r.w, 16):
                pygame.draw.rect(surf, WHITE, (r.x + i, r.y, 8, r.h))
        elif self.kind == "speed_bump":
            pygame.draw.rect(surf, BROWN, r, border_radius=6)
            pygame.draw.rect(surf, DKGRAY, r, 2, border_radius=6)
        else:   # nitro_strip
            pygame.draw.rect(surf, YELLOW, r, border_radius=4)
            pygame.draw.rect(surf, ORANGE, r, 2, border_radius=4)


# ── Lane hazard (slow zone) ───────────────────────────────────────────────────

class LaneHazard:
    def __init__(self):
        self.lane  = rand_lane()
        self.x     = ROAD_LEFT + self.lane * LANE_W
        self.y     = float(-120)
        self.h     = 80
        self.w     = LANE_W
        self.timer = 200

    def update(self, scroll_speed):
        self.y    += scroll_speed
        self.timer -= 1

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surf):
        s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        s.fill((255, 50, 50, 70))
        surf.blit(s, (int(self.x), int(self.y)))
        # warning stripes
        for i in range(0, self.h, 16):
            pygame.draw.line(surf, (255, 100, 0),
                             (int(self.x), int(self.y) + i),
                             (int(self.x) + self.w, int(self.y) + i), 2)


# ── Main Game ─────────────────────────────────────────────────────────────────

class RacerGame:
    def __init__(self, settings, username="Player"):
        self.settings  = settings
        self.username  = username
        self.diff_mult = difficulty_multipliers(settings.get("difficulty", "medium"))

        self.player    = Player(settings.get("car_color", "red"))
        self.scroll    = SCROLL_SPEED_BASE * self.diff_mult
        self.distance  = 0.0
        self.score     = 0
        self.coins     = 0       # carried from P10/P11 — tracked as score bonus
        self.alive     = True
        self.finished  = False
        self.crash_timer = 0

        # HUD font
        self.font_sm  = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_med = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_pu  = pygame.font.SysFont("Arial", 20, bold=True)

        # Road stripes
        self.stripes = []
        for lane in range(1, NUM_LANES):
            sx = ROAD_LEFT + lane * LANE_W
            for y in range(-30, HEIGHT, 80):
                self.stripes.append(RoadStripe(sx, y))

        # Spawn counters
        self.enemy_timer   = 0
        self.obs_timer     = 0
        self.pu_timer      = 0
        self.event_timer   = 0
        self.hazard_timer  = 0

        self.enemies   = []
        self.obstacles = []
        self.powerups  = []
        self.events    = []
        self.hazards   = []

        # Active power-up
        self.active_pu       = None
        self.active_pu_timer = 0

        # Key state for smooth input
        self._left_held  = False
        self._right_held = False
        self._move_cd    = 0

    # ── input ──────────────────────────────────────────────────────────────

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.player.move(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.player.move(1)

    # ── update ─────────────────────────────────────────────────────────────

    def update(self):
        if not self.alive or self.finished:
            if self.crash_timer > 0:
                self.crash_timer -= 1
            return

        speed = self.scroll * (1.5 if self.player.nitro else 1.0)
        self.distance += speed / 10.0
        self.score     = int(self.distance) + self.coins * 10

        # difficulty ramp
        ramp = 1.0 + self.distance / 5000.0
        self.scroll = SCROLL_SPEED_BASE * self.diff_mult * ramp

        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            return

        # stripes
        for s in self.stripes:
            s.update(speed)

        # spawn enemies
        self.enemy_timer -= 1
        base_interval = max(30, int(90 / ramp))
        if self.enemy_timer <= 0:
            self.enemy_timer = random.randint(base_interval, base_interval * 2)
            e = Enemy(self.diff_mult * ramp)
            # safe spawn — not on player lane
            while e.lane == self.player.lane:
                e.lane = rand_lane()
                e.x = float(lane_x(e.lane))
            self.enemies.append(e)

        # spawn obstacles
        self.obs_timer -= 1
        if self.obs_timer <= 0:
            self.obs_timer = random.randint(60, 150)
            o = Obstacle()
            while o.lane == self.player.lane and random.random() > 0.3:
                o.lane = rand_lane()
                o.x = float(lane_x(o.lane))
            self.obstacles.append(o)

        # spawn power-ups (only one on screen)
        self.pu_timer -= 1
        if self.pu_timer <= 0 and len(self.powerups) == 0:
            self.pu_timer = random.randint(200, 400)
            self.powerups.append(PowerUp())

        # spawn road events
        self.event_timer -= 1
        if self.event_timer <= 0:
            self.event_timer = random.randint(150, 300)
            self.events.append(RoadEvent())

        # spawn lane hazards
        self.hazard_timer -= 1
        if self.hazard_timer <= 0:
            self.hazard_timer = random.randint(120, 250)
            self.hazards.append(LaneHazard())

        # update everything
        for e in self.enemies:
            e.update(speed)
        for o in self.obstacles:
            o.update(speed)
        for p in self.powerups:
            p.update(speed)
        for ev in self.events:
            ev.update(speed)
        for hz in self.hazards:
            hz.update(speed)

        self.player.update()

        # collisions
        pr = self.player.rect()

        # enemy collision
        for e in self.enemies[:]:
            if pr.colliderect(e.rect()):
                if self.player.shield_active:
                    self.player.shield_active = False
                    self.active_pu = None
                    self.enemies.remove(e)
                else:
                    self._crash()
                    return

        # obstacle collision
        for o in self.obstacles[:]:
            if pr.colliderect(o.rect()):
                if self.player.shield_active:
                    self.player.shield_active = False
                    self.active_pu = None
                    self.obstacles.remove(o)
                elif o.type == "oil":
                    # slow effect — handled by lane hazard logic; just remove
                    self.obstacles.remove(o)
                else:
                    self._crash()
                    return

        # lane hazard (slow zone)
        for hz in self.hazards:
            if pr.colliderect(hz.rect()):
                speed_penalty = speed * 0.4
                self.scroll = max(SCROLL_SPEED_BASE * 0.5,
                                  self.scroll - speed_penalty * 0.05)

        # road event collision
        for ev in self.events[:]:
            if pr.colliderect(ev.rect()):
                if ev.kind == "moving_barrier":
                    if not self.player.shield_active:
                        self._crash()
                        return
                    else:
                        self.player.shield_active = False
                        self.active_pu = None
                elif ev.kind == "speed_bump":
                    self.scroll = max(2.0, self.scroll - 1.0)
                elif ev.kind == "nitro_strip":
                    self.player.activate_nitro(60)

        # power-up collection
        for p in self.powerups[:]:
            if pr.colliderect(p.rect()):
                self._apply_powerup(p.type)
                self.powerups.remove(p)

        # active power-up countdown
        if self.active_pu in ("nitro",):
            pass   # managed by player nitro_timer
        if self.active_pu == "shield" and self.player.shield_active:
            pass   # until hit

        # cull off-screen
        self.enemies   = [e for e in self.enemies   if e.y < HEIGHT + 100]
        self.obstacles = [o for o in self.obstacles if o.y < HEIGHT + 100]
        self.powerups  = [p for p in self.powerups  if not p.expired() and p.y < HEIGHT + 100]
        self.events    = [ev for ev in self.events  if ev.timer > 0 and ev.y < HEIGHT + 100]
        self.hazards   = [hz for hz in self.hazards if hz.timer > 0 and hz.y < HEIGHT + 100]

    def _apply_powerup(self, kind):
        self.active_pu = kind
        if kind == "nitro":
            self.player.activate_nitro(180)   # 3 sec @ 60fps
        elif kind == "shield":
            self.player.shield_active = True
        elif kind == "repair":
            # clears one obstacle ahead — just cosmetic here
            if self.obstacles:
                self.obstacles.pop(0)

    def _crash(self):
        self.alive = False
        self.crash_timer = 120

    # ── draw ───────────────────────────────────────────────────────────────

    def draw(self, surf):
        # sky
        surf.fill(SKY_C)

        # grass sides
        pygame.draw.rect(surf, GRASS_C, (0, 0, ROAD_LEFT, HEIGHT))
        pygame.draw.rect(surf, GRASS_C, (ROAD_RIGHT, 0, WIDTH - ROAD_RIGHT, HEIGHT))

        # road
        pygame.draw.rect(surf, ROAD_C, (ROAD_LEFT, 0, ROAD_W, HEIGHT))

        # stripes
        for s in self.stripes:
            s.draw(surf)

        # road edges
        pygame.draw.rect(surf, WHITE, (ROAD_LEFT - 3, 0, 6, HEIGHT))
        pygame.draw.rect(surf, WHITE, (ROAD_RIGHT - 3, 0, 6, HEIGHT))

        # hazards
        for hz in self.hazards:
            hz.draw(surf)

        # events
        for ev in self.events:
            ev.draw(surf)

        # obstacles
        for o in self.obstacles:
            o.draw(surf)

        # power-ups
        for p in self.powerups:
            p.draw(surf, self.font_pu)

        # enemies
        for e in self.enemies:
            e.draw(surf)

        # player
        self.player.draw(surf)

        # crash effect
        if not self.alive:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = min(180, (120 - self.crash_timer) * 3)
            s.fill((255, 0, 0, alpha))
            surf.blit(s, (0, 0))

        # finish line
        finish_y = HEIGHT - int(self.distance / FINISH_DISTANCE * HEIGHT * 10) % (HEIGHT * 2)
        if 0 <= finish_y <= HEIGHT:
            for x in range(ROAD_LEFT, ROAD_RIGHT, 20):
                color = WHITE if (x // 20) % 2 == 0 else BLACK
                pygame.draw.rect(surf, color, (x, finish_y, 20, 10))

        self._draw_hud(surf)

    def _draw_hud(self, surf):
        # top bar background
        pygame.draw.rect(surf, (0, 0, 0, 180), (0, 0, WIDTH, 50))

        # score
        sc = self.font_med.render(f"Score: {self.score}", True, WHITE)
        surf.blit(sc, (10, 10))

        # distance
        dist_pct = min(1.0, self.distance / FINISH_DISTANCE)
        dist_txt = self.font_sm.render(
            f"Dist: {int(self.distance)}/{FINISH_DISTANCE}", True, YELLOW)
        surf.blit(dist_txt, (WIDTH // 2 - dist_txt.get_width() // 2, 6))

        # distance bar
        bar_x, bar_y, bar_w, bar_h = WIDTH // 2 - 80, 26, 160, 10
        pygame.draw.rect(surf, DKGRAY, (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surf, GREEN,
                         (bar_x, bar_y, int(bar_w * dist_pct), bar_h), border_radius=4)

        # speed indicator
        spd_txt = self.font_sm.render(f"{int(self.scroll * 20)} km/h", True, ORANGE)
        surf.blit(spd_txt, (WIDTH - spd_txt.get_width() - 10, 10))

        # active power-up
        if self.active_pu:
            pu_col = PU_COLORS.get(self.active_pu, WHITE)
            label  = f"[{self.active_pu.upper()}]"
            if self.active_pu == "nitro" and self.player.nitro_timer > 0:
                label += f" {self.player.nitro_timer // 60 + 1}s"
            pu_surf = self.font_sm.render(label, True, pu_col)
            surf.blit(pu_surf, (WIDTH - pu_surf.get_width() - 8, HEIGHT - 30))

        # username
        name_surf = self.font_sm.render(self.username, True, (200, 200, 200))
        surf.blit(name_surf, (10, HEIGHT - 28))

        # controls hint (fades after a bit)
        if self.distance < 200:
            hint = self.font_sm.render("← → to steer", True, (180, 180, 180))
            surf.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))