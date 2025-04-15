import curses
import random
import time
import os

HIGH_SCORE_FILE = "highscore.txt"

# Load high scores as a dictionary {name: score}
def load_high_scores():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            scores = {}
            for line in f:
                if ":" in line:
                    name, score = line.strip().split(":")
                    scores[name] = int(score)
            return scores
    return {}

def save_high_scores(high_scores):
    with open(HIGH_SCORE_FILE, "w") as f:
        for name, score in high_scores.items():
            f.write(f"{name}:{score}\n")

def show_menu(stdscr):
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()

    title = "🚗 TERMINAL TRAFFIC RACER 🚗"
    prompt = "Press '1' for Solo or '2' for Multiplayer"
    stdscr.addstr(sh//2 - 2, sw//2 - len(title)//2, title)
    stdscr.addstr(sh//2, sw//2 - len(prompt)//2, prompt)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('1'):
            return 1
        elif key == ord('2'):
            return 2

def get_player_names(stdscr, num_players):
    curses.echo()
    sh, sw = stdscr.getmaxyx()
    names = []
    for i in range(num_players):
        stdscr.clear()
        prompt = f"Enter name for Player {i+1}: "
        stdscr.addstr(sh//2, sw//2 - len(prompt)//2, prompt)
        stdscr.refresh()
        name = stdscr.getstr().decode("utf-8")
        names.append(name)
    curses.noecho()
    return names

def game(stdscr, mode):
    curses.curs_set(0)
    stdscr.nodelay(True)

    sh, sw = stdscr.getmaxyx()
    total_lanes = 4
    lane_width = sw // total_lanes
    lanes = [i * lane_width + lane_width // 2 for i in range(total_lanes)]

    names = get_player_names(stdscr, 2 if mode == 2 else 1)
    high_scores = load_high_scores()

    players = [
        {
            "name": names[0],
            "lane": 1,
            "y": sh - 4,
            "char": "[1]",
            "controls": {"left": ord('a'), "right": ord('d'), "up": ord('w'), "down": ord('s'), "jump": ord(' ')},
            "score": 0,
            "jump": False,
            "jump_frames": 0,
            "alive": True
        }
    ]

    if mode == 2:
        players.append({
            "name": names[1],
            "lane": 2,
            "y": sh - 4,
            "char": "[2]",
            "controls": {"left": ord('j'), "right": ord('l'), "up": ord('i'), "down": ord('k'), "jump": ord('m')},
            "score": 0,
            "jump": False,
            "jump_frames": 0,
            "alive": True
        })

    obstacles = []
    frame_delay = 0.2
    last_frame_time = time.time()
    last_obstacle_time = time.time()

    while True:
        now = time.time()
        elapsed = now - last_frame_time
        if elapsed < frame_delay:
            time.sleep(0.01)
            continue
        last_frame_time = now

        stdscr.erase()
        key = stdscr.getch()

        for p in players:
            if not p["alive"]:
                continue

            if key == p["controls"]["left"] and p["lane"] > 0:
                p["lane"] -= 1
            elif key == p["controls"]["right"] and p["lane"] < total_lanes - 1:
                p["lane"] += 1
            elif key == p["controls"]["up"]:
                frame_delay = max(0.05, frame_delay - 0.02)
            elif key == p["controls"]["down"]:
                frame_delay = min(0.5, frame_delay + 0.02)
            elif key == p["controls"]["jump"] and not p["jump"]:
                p["jump"] = True
                p["jump_frames"] = 2

        if key in [ord('q'), ord('Q')]:
            break

        if now - last_obstacle_time > 0.6:
            obstacles.append([1, random.randint(0, total_lanes - 1)])
            last_obstacle_time = now

        new_obstacles = []
        for oy, olane in obstacles:
            if oy < sh - 3:
                new_obstacles.append([oy + 1, olane])
        obstacles = new_obstacles

        for oy, olane in obstacles:
            ox = lanes[olane] - 2
            stdscr.addstr(oy, ox, "[V]")

        for p in players:
            if not p["alive"]:
                continue

            draw_y = p["y"]
            if p["jump"]:
                draw_y -= 1
                p["jump_frames"] -= 1
                if p["jump_frames"] <= 0:
                    p["jump"] = False

            car_x = lanes[p["lane"]] - len(p["char"]) // 2
            stdscr.addstr(draw_y, car_x, p["char"])

        for i in range(1, total_lanes):
            divider_x = i * lane_width
            for y in range(1, sh - 2, 2):
                stdscr.addch(y, divider_x, '|')

        for p in players:
            if not p["alive"]:
                continue
            for oy, olane in obstacles:
                if oy == p["y"] and olane == p["lane"] and not p["jump"]:
                    p["alive"] = False
                    stdscr.addstr(sh//2, 2, f"{p['name']} 💀 CRASHED! Press R to restart or Q to quit")

        all_dead = all(not p["alive"] for p in players)

        for p in players:
            if p["alive"]:
                p["score"] += 1

        stdscr.hline(0, 0, '-', sw)
        stdscr.hline(sh - 2, 0, '-', sw)

        for idx, p in enumerate(players):
            hiscore = high_scores.get(p["name"], 0)
            stdscr.addstr(sh - 1 - idx, 0, f"{p['name']} Score: {p['score']} | High Score: {hiscore}")

        stdscr.refresh()

        if all_dead:
            for p in players:
                if p["score"] > high_scores.get(p["name"], 0):
                    high_scores[p["name"]] = p["score"]
            save_high_scores(high_scores)

            stdscr.nodelay(False)
            while True:
                key = stdscr.getch()
                if key in [ord('r'), ord('R')]:
                    return game(stdscr, mode)
                elif key in [ord('q'), ord('Q')]:
                    return

def main(stdscr):
    mode = show_menu(stdscr)
    game(stdscr, mode)

if __name__ == "__main__":
    curses.wrapper(main)
