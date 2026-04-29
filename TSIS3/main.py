"""
TSIS3 – Racer Arcade
Run:  python main.py
"""

import pygame
import sys

from persistence import load_settings, save_settings, load_leaderboard, add_score
from racer import RacerGame, WIDTH, HEIGHT
from ui import (
    MainMenu,
    UsernameScreen,
    SettingsScreen,
    GameOverScreen,
    LeaderboardScreen,
)

FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer Arcade – TSIS3")
    clock = pygame.time.Clock()

    settings = load_settings()

    # ── state machine ──────────────────────────────────────────────────────
    # States: "menu" | "username" | "game" | "gameover" | "leaderboard" | "settings"
    state    = "menu"
    username = "Player"
    game     = None
    go_screen  = None

    screens = {}

    def make_menu():
        screens["menu"]     = MainMenu(WIDTH, HEIGHT)
        screens["username"] = UsernameScreen(WIDTH, HEIGHT)

    def make_settings():
        screens["settings"] = SettingsScreen(WIDTH, HEIGHT, settings)

    def make_leaderboard():
        screens["leaderboard"] = LeaderboardScreen(WIDTH, HEIGHT, load_leaderboard())

    make_menu()
    make_settings()
    make_leaderboard()

    while True:
        dt = clock.tick(FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ── MENU ────────────────────────────────────────────────────
            if state == "menu":
                result = screens["menu"].handle(event)
                if result == "play":
                    screens["username"] = UsernameScreen(WIDTH, HEIGHT)
                    state = "username"
                elif result == "leaderboard":
                    make_leaderboard()
                    state = "leaderboard"
                elif result == "settings":
                    make_settings()
                    state = "settings"
                elif result == "quit":
                    pygame.quit()
                    sys.exit()

            # ── USERNAME ────────────────────────────────────────────────
            elif state == "username":
                result = screens["username"].handle(event)
                if result is not None:
                    action, val = result
                    if action == "start":
                        username = val
                        game     = RacerGame(settings, username)
                        state    = "game"
                    elif action == "back":
                        state = "menu"

            # ── GAME ────────────────────────────────────────────────────
            elif state == "game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # quit to menu mid-game
                    state = "menu"
                else:
                    game.handle_event(event)

            # ── GAME OVER ───────────────────────────────────────────────
            elif state == "gameover":
                result = go_screen.handle(event)
                if result == "retry":
                    game  = RacerGame(settings, username)
                    state = "game"
                elif result == "menu":
                    make_menu()
                    state = "menu"

            # ── LEADERBOARD ─────────────────────────────────────────────
            elif state == "leaderboard":
                result = screens["leaderboard"].handle(event)
                if result == "back":
                    state = "menu"

            # ── SETTINGS ────────────────────────────────────────────────
            elif state == "settings":
                result = screens["settings"].handle(event)
                if result is not None:
                    action, new_settings = result
                    if action == "save":
                        settings.update(new_settings)
                        save_settings(settings)
                    state = "menu"

        # ── update & draw ──────────────────────────────────────────────────
        if state == "menu":
            screens["menu"].draw(screen)

        elif state == "username":
            screens["username"].draw(screen)

        elif state == "game":
            game.update()
            game.draw(screen)

            # transition to game-over
            if not game.alive and game.crash_timer == 0:
                add_score(username, game.score, game.distance)
                go_screen = GameOverScreen(
                    WIDTH, HEIGHT,
                    game.score, game.distance, game.coins,
                    finished=game.finished,
                )
                state = "gameover"
            elif game.finished:
                add_score(username, game.score, game.distance)
                go_screen = GameOverScreen(
                    WIDTH, HEIGHT,
                    game.score, game.distance, game.coins,
                    finished=True,
                )
                state = "gameover"

        elif state == "gameover":
            go_screen.draw(screen)

        elif state == "leaderboard":
            screens["leaderboard"].draw(screen)

        elif state == "settings":
            screens["settings"].draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()