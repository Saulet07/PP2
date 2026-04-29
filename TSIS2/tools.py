"""
tools.py — drawing tool implementations for TSIS2 Paint App.
"""
import pygame
from collections import deque


# ── Flood Fill ────────────────────────────────────────────────────────────────

def flood_fill(surface: pygame.Surface, x: int, y: int, fill_color: tuple):
    """BFS flood-fill on a pygame.Surface using get_at / set_at."""
    w, h       = surface.get_size()
    target_col = surface.get_at((x, y))[:3]   # ignore alpha
    fill_col3  = fill_color[:3]

    if target_col == fill_col3:
        return

    visited = set()
    queue   = deque()
    queue.append((x, y))
    visited.add((x, y))

    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), fill_color)

        for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
            if (nx, ny) not in visited and 0 <= nx < w and 0 <= ny < h:
                if surface.get_at((nx, ny))[:3] == target_col:
                    visited.add((nx, ny))
                    queue.append((nx, ny))


# ── Tool constants ────────────────────────────────────────────────────────────

TOOL_PENCIL   = "pencil"
TOOL_LINE     = "line"
TOOL_RECT     = "rect"
TOOL_CIRCLE   = "circle"
TOOL_FILL     = "fill"
TOOL_TEXT     = "text"
TOOL_ERASER   = "eraser"

BRUSH_SIZES   = [2, 5, 10]   # small, medium, large
BRUSH_LABELS  = ["S", "M", "L"]
BRUSH_KEYS    = [pygame.K_1, pygame.K_2, pygame.K_3]