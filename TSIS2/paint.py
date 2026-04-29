"""
paint.py — TSIS2 Paint App
Run:  python paint.py

Features:
  • Pencil tool      – freehand drawing
  • Straight line    – click drag release with live preview
  • Rectangle        – click drag release with live preview
  • Circle           – click drag release with live preview
  • Flood fill       – BFS fill with current colour
  • Text tool        – click to place, type, Enter to commit, Esc to cancel
  • Eraser           – freehand white eraser
  • Brush sizes      – S(2px) M(5px) L(10px) via buttons or keys 1/2/3
  • Colour palette   – 20 preset colours + current colour swatch
  • Save canvas      – Ctrl+S → timestamped .png
"""

import pygame
import sys
import datetime
from tools import (
    flood_fill,
    TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_CIRCLE,
    TOOL_FILL, TOOL_TEXT, TOOL_ERASER,
    BRUSH_SIZES, BRUSH_LABELS, BRUSH_KEYS,
)

# ── Layout ────────────────────────────────────────────────────────────────────
TOOLBAR_W  = 130
WIDTH      = 900
HEIGHT     = 650
CANVAS_X   = TOOLBAR_W
CANVAS_W   = WIDTH - TOOLBAR_W
CANVAS_H   = HEIGHT

# ── Colours ───────────────────────────────────────────────────────────────────
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
LTGRAY  = (220, 220, 220)
GRAY    = (150, 150, 150)
DKGRAY  = ( 50,  50,  50)
TOOLBAR_BG = ( 40,  40,  50)
ACCENT  = ( 80, 140, 255)

PALETTE = [
    (  0,   0,   0), (255, 255, 255), (128, 128, 128), (192, 192, 192),
    (255,   0,   0), (128,   0,   0), (255, 128,   0), (128,  64,   0),
    (255, 255,   0), (128, 128,   0), (  0, 255,   0), (  0, 128,   0),
    (  0, 255, 255), (  0, 128, 128), (  0,   0, 255), (  0,   0, 128),
    (255,   0, 255), (128,   0, 128), (255, 128, 128), (128, 255, 128),
]


def draw_rounded(surf, col, rect, r=5):
    pygame.draw.rect(surf, col, rect, border_radius=r)


# ── Toolbar button ────────────────────────────────────────────────────────────

class ToolButton:
    def __init__(self, rect, label, tool_id, font):
        self.rect    = pygame.Rect(rect)
        self.label   = label
        self.tool_id = tool_id
        self.font    = font

    def draw(self, surf, active: bool):
        col = ACCENT if active else DKGRAY
        draw_rounded(surf, col, self.rect)
        pygame.draw.rect(surf, LTGRAY, self.rect, 1, border_radius=5)
        lbl = self.font.render(self.label, True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def clicked(self, ev):
        return (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1
                and self.rect.collidepoint(ev.pos))


# ── Main App ──────────────────────────────────────────────────────────────────

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Paint App – TSIS2")
        self.clock   = pygame.time.Clock()

        # Fonts
        self.font_sm  = pygame.font.SysFont("Arial", 13, bold=True)
        self.font_med = pygame.font.SysFont("Arial", 15, bold=True)
        self.font_txt = pygame.font.SysFont("Arial", 20)

        # Canvas surface (white)
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(WHITE)

        # Drawing state
        self.tool       = TOOL_PENCIL
        self.color      = BLACK
        self.brush_idx  = 1          # 0=small 1=medium 2=large
        self.drawing    = False
        self.last_pos   = None
        self.start_pos  = None       # for line/rect/circle preview

        # Text tool state
        self.text_active   = False
        self.text_pos      = None
        self.text_buffer   = ""

        # Preview overlay (for line/rect/circle)
        self.preview_canvas  = None
        self.preview_surface = None   # frame shown while dragging
        self.preview_end     = None

        # Build UI
        self._build_ui()

    # ── UI Construction ───────────────────────────────────────────────────

    def _build_ui(self):
        f = self.font_sm
        x0, bw, bh = 5, 120, 28
        tools = [
            ("✏ Pencil",   TOOL_PENCIL),
            ("╱ Line",     TOOL_LINE),
            ("▭ Rect",     TOOL_RECT),
            ("○ Circle",   TOOL_CIRCLE),
            ("⬛ Fill",    TOOL_FILL),
            ("T Text",     TOOL_TEXT),
            ("⌫ Eraser",   TOOL_ERASER),
        ]
        self.tool_buttons = []
        for i, (label, tid) in enumerate(tools):
            r = pygame.Rect(x0, 10 + i * (bh + 4), bw, bh)
            self.tool_buttons.append(ToolButton(r, label, tid, f))

        # Brush size buttons
        self.brush_buttons = []
        for i, lbl in enumerate(BRUSH_LABELS):
            r = pygame.Rect(x0 + i * 40, 10 + len(tools) * (bh + 4) + 10, 35, 28)
            self.brush_buttons.append(r)

        # Palette
        self.palette_rects = []
        sw = 24
        cols_per_row = 5
        py_start = 10 + len(tools) * (bh + 4) + 50
        for i, col in enumerate(PALETTE):
            row, col_idx = divmod(i, cols_per_row)
            r = pygame.Rect(x0 + col_idx * (sw + 2), py_start + row * (sw + 2), sw, sw)
            self.palette_rects.append((r, col))

        # Current colour swatch
        self.swatch_rect = pygame.Rect(x0, py_start + 5 * (sw + 2) + 8, bw, 28)

    # ── Coordinate helpers ────────────────────────────────────────────────

    def _canvas_pos(self, pos):
        """Convert screen pos to canvas-local pos."""
        return (pos[0] - CANVAS_X, pos[1])

    def _on_canvas(self, pos):
        return pos[0] >= CANVAS_X

    # ── Event handling ────────────────────────────────────────────────────

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # ── keyboard ─────────────────────────────────────────────────
            elif ev.type == pygame.KEYDOWN:
                # Ctrl+S save
                mods = pygame.key.get_mods()
                if ev.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    self._save_canvas()
                    continue

                # brush size hotkeys (only when not typing)
                if not self.text_active:
                    for i, k in enumerate(BRUSH_KEYS):
                        if ev.key == k:
                            self.brush_idx = i

                # text tool input
                if self.text_active:
                    if ev.key == pygame.K_RETURN:
                        self._commit_text()
                    elif ev.key == pygame.K_ESCAPE:
                        self.text_active  = False
                        self.text_buffer  = ""
                        self.text_pos     = None
                    elif ev.key == pygame.K_BACKSPACE:
                        self.text_buffer = self.text_buffer[:-1]
                    elif ev.unicode and ev.unicode.isprintable():
                        self.text_buffer += ev.unicode

            # ── mouse button down ─────────────────────────────────────────
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                pos = ev.pos

                # toolbar clicks
                for tb in self.tool_buttons:
                    if tb.clicked(ev):
                        self.tool = tb.tool_id
                        self.text_active = False
                        break

                for i, r in enumerate(self.brush_buttons):
                    if r.collidepoint(pos):
                        self.brush_idx = i
                        break

                for r, col in self.palette_rects:
                    if r.collidepoint(pos):
                        self.color = col
                        break

                # canvas clicks
                if self._on_canvas(pos):
                    cp = self._canvas_pos(pos)

                    if self.tool == TOOL_FILL:
                        flood_fill(self.canvas, *cp, self.color)

                    elif self.tool == TOOL_TEXT:
                        # commit any existing text first
                        if self.text_active:
                            self._commit_text()
                        self.text_active = True
                        self.text_pos    = cp
                        self.text_buffer = ""

                    elif self.tool in (TOOL_LINE, TOOL_RECT, TOOL_CIRCLE):
                        self.drawing         = True
                        self.start_pos       = cp
                        self.preview_canvas  = self.canvas.copy()   # frozen snapshot
                        self.preview_surface = self.canvas.copy()   # current preview frame
                        self.preview_end     = cp

                    elif self.tool in (TOOL_PENCIL, TOOL_ERASER):
                        self.drawing  = True
                        self.last_pos = cp

            # ── mouse move ────────────────────────────────────────────────
            elif ev.type == pygame.MOUSEMOTION:
                if self.drawing and self._on_canvas(ev.pos):
                    cp = self._canvas_pos(ev.pos)

                    if self.tool == TOOL_PENCIL:
                        if self.last_pos:
                            pygame.draw.line(self.canvas, self.color,
                                             self.last_pos, cp,
                                             BRUSH_SIZES[self.brush_idx])
                        self.last_pos = cp

                    elif self.tool == TOOL_ERASER:
                        if self.last_pos:
                            pygame.draw.line(self.canvas, WHITE,
                                             self.last_pos, cp,
                                             BRUSH_SIZES[self.brush_idx] * 3)
                        self.last_pos = cp

                    # preview for shape tools — draw onto a temp surface, NOT self.canvas
                    elif self.tool in (TOOL_LINE, TOOL_RECT, TOOL_CIRCLE):
                        self.preview_surface = self.preview_canvas.copy()
                        self._draw_shape(self.preview_surface, self.start_pos, cp)
                        self.preview_end = cp

            # ── mouse button up ───────────────────────────────────────────
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if self.drawing:
                    cp = self._canvas_pos(ev.pos)
                    if self.tool in (TOOL_LINE, TOOL_RECT, TOOL_CIRCLE):
                        # Commit: draw onto the frozen snapshot, make it the new canvas
                        committed = self.preview_canvas.copy()
                        self._draw_shape(committed, self.start_pos, cp)
                        self.canvas = committed
                        self.preview_surface = None
                    self.drawing        = False
                    self.last_pos       = None
                    self.start_pos      = None
                    self.preview_canvas = None
                    self.preview_end    = None

    # ── Shape drawing ─────────────────────────────────────────────────────

    def _draw_shape(self, surf, p1, p2, preview=False):
        col   = self.color
        thick = BRUSH_SIZES[self.brush_idx]
        if self.tool == TOOL_LINE:
            pygame.draw.line(surf, col, p1, p2, thick)
        elif self.tool == TOOL_RECT:
            x = min(p1[0], p2[0])
            y = min(p1[1], p2[1])
            w = abs(p2[0] - p1[0])
            h = abs(p2[1] - p1[1])
            pygame.draw.rect(surf, col, (x, y, w, h), thick)
        elif self.tool == TOOL_CIRCLE:
            cx = (p1[0] + p2[0]) // 2
            cy = (p1[1] + p2[1]) // 2
            rx = abs(p2[0] - p1[0]) // 2
            ry = abs(p2[1] - p1[1]) // 2
            r  = max(rx, ry)
            if r > 0:
                pygame.draw.circle(surf, col, (cx, cy), r, thick)

    # ── Text handling ─────────────────────────────────────────────────────

    def _commit_text(self):
        if self.text_buffer and self.text_pos:
            lbl = self.font_txt.render(self.text_buffer, True, self.color)
            self.canvas.blit(lbl, self.text_pos)
        self.text_active = False
        self.text_buffer = ""
        self.text_pos    = None

    # ── Save canvas ───────────────────────────────────────────────────────

    def _save_canvas(self):
        ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"canvas_{ts}.png"
        pygame.image.save(self.canvas, name)
        print(f"[Saved] {name}")
        # brief on-screen flash message
        self._flash_msg = (f"Saved: {name}", pygame.time.get_ticks())

    # ── Draw toolbar ──────────────────────────────────────────────────────

    def _draw_toolbar(self, surf):
        pygame.draw.rect(surf, TOOLBAR_BG, (0, 0, TOOLBAR_W, HEIGHT))

        # tool buttons
        for tb in self.tool_buttons:
            tb.draw(surf, self.tool == tb.tool_id)

        # brush size buttons
        y_off = self.brush_buttons[0].y - 16
        lbl = self.font_sm.render("Brush:", True, LTGRAY)
        surf.blit(lbl, (5, y_off))
        for i, r in enumerate(self.brush_buttons):
            active = (i == self.brush_idx)
            col    = ACCENT if active else DKGRAY
            draw_rounded(surf, col, r)
            pygame.draw.rect(surf, LTGRAY, r, 1, border_radius=4)
            t = self.font_sm.render(BRUSH_LABELS[i], True, WHITE)
            surf.blit(t, t.get_rect(center=r.center))

        # palette
        for r, col in self.palette_rects:
            pygame.draw.rect(surf, col, r)
            if col == self.color:
                pygame.draw.rect(surf, WHITE, r, 2)

        # current colour swatch
        pygame.draw.rect(surf, self.color, self.swatch_rect, border_radius=4)
        pygame.draw.rect(surf, WHITE,      self.swatch_rect, 2, border_radius=4)
        lbl2 = self.font_sm.render("Color", True, WHITE)
        surf.blit(lbl2, lbl2.get_rect(center=self.swatch_rect.center))

        # divider
        pygame.draw.line(surf, GRAY, (TOOLBAR_W - 1, 0), (TOOLBAR_W - 1, HEIGHT))

        # hotkey hint at bottom
        hints = ["1=S 2=M 3=L", "Ctrl+S = Save"]
        for i, h in enumerate(hints):
            hl = self.font_sm.render(h, True, GRAY)
            surf.blit(hl, (5, HEIGHT - 32 + i * 16))

    # ── Main loop ─────────────────────────────────────────────────────────

    def run(self):
        self._flash_msg = None

        while True:
            self.clock.tick(60)
            self.handle_events()

            # ── compose frame ──────────────────────────────────────────────
            self.screen.fill((30, 30, 30))

            # canvas (or preview surface during shape drag)
            display_canvas = (self.preview_surface
                              if self.preview_surface is not None
                              else self.canvas)
            self.screen.blit(display_canvas, (CANVAS_X, 0))

            # text cursor preview
            if self.text_active and self.text_pos:
                preview_lbl = self.font_txt.render(
                    self.text_buffer + "|", True, self.color)
                self.screen.blit(preview_lbl,
                                 (CANVAS_X + self.text_pos[0],
                                  self.text_pos[1]))

            # toolbar
            self._draw_toolbar(self.screen)

            # flash save message
            if self._flash_msg:
                msg, t0 = self._flash_msg
                if pygame.time.get_ticks() - t0 < 2500:
                    box = pygame.Surface((360, 30), pygame.SRCALPHA)
                    box.fill((0, 0, 0, 160))
                    self.screen.blit(box, (CANVAS_X + 10, HEIGHT - 38))
                    lbl = self.font_med.render(msg, True, (180, 255, 180))
                    self.screen.blit(lbl, (CANVAS_X + 14, HEIGHT - 34))
                else:
                    self._flash_msg = None

            # canvas border
            pygame.draw.rect(self.screen, GRAY,
                             (CANVAS_X, 0, CANVAS_W, HEIGHT), 1)

            pygame.display.flip()


if __name__ == "__main__":
    PaintApp().run()