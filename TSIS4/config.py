"""
config.py — database connection settings and global constants.
Edit DB_CONFIG to match your PostgreSQL setup.
"""

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "snake_game",
    "user":     "postgres",
    "password": "postgres",
}

# Grid / window
CELL         = 20          # pixels per grid cell
COLS         = 30          # grid columns
ROWS         = 28          # grid rows
PANEL_H      = 60          # top HUD height (pixels)
WIDTH        = CELL * COLS
HEIGHT       = CELL * ROWS + PANEL_H

FPS          = 10          # base snake ticks per second

# Levels
LEVEL_SCORE_STEP = 5       # score points to advance a level
MAX_OBSTACLES    = 12      # max obstacle cells on screen