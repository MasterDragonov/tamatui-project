import curses
import time
import random
from characters import Mage
from mob import monster_pool

def draw_borders(win):
    win.attron(curses.A_BOLD)
    win.box()
    win.attroff(curses.A_BOLD)

def render_screen(stdscr, player, monster, menu_opt, menu_select, log_text):
    stdscr.erase()
    sh, sw = stdscr.getmaxyx()

    if sh < 24 or sw < 70:
        stdscr.addstr(0, 0, "Terminal too small! Please resize to at least 70x24.")
        stdscr.refresh()
        return

    stdscr.noutrefresh()

    # 1. PLAYER STATUS BOX
    status_win = curses.newwin(6, 22, 1, 2)
    draw_borders(status_win)
    status_win.addstr(1, 2, f"{player.name.upper()[:10]}", curses.A_BOLD)
    status_win.addstr(2, 2, f"LV: {player.level:2d} {getattr(player, 'job', 'HERO')}")
    status_win.addstr(3, 2, f"HP: {player.hp:3d}/{player.max_hp:3d}")
    status_win.addstr(4, 2, f"MP: {player.mp:3d}/{player.max_mp:3d}")
    status_win.noutrefresh()

    # 2. ENEMY ARENA (Reading the imported ASCII property dynamically)
    arena_win = curses.newwin(11, sw - 4, 7, 2)
    draw_borders(arena_win)
    
    if monster.is_alive():
        art = monster.ascii_art
        art_width = max(len(line) for line in art) if art else 0
        center_x = (sw - 4) // 2 - (art_width // 2)
        
        for row_idx, line in enumerate(art):
            if row_idx + 1 < 9:
                arena_win.addstr(1 + row_idx, center_x, line)
                
        monster_title = f"{monster.name.upper()} (LV {monster.level})"
        name_x = (sw - 4) // 2 - (len(monster_title) // 2)
        arena_win.addstr(9, name_x, monster_title, curses.A_BOLD)

        # Render Dynamic Health Bar Element (Row 10)
        bar_length = 20  # Total character width of the health bar
        # Calculate filled segments safely, ensuring it drops to 0 when appropriate
        filled_segments = round((monster.hp / monster.max_hp) * bar_length) if monster.hp > 0 else 0
        if filled_segments == 0 and monster.hp > 0:
            filled_segments = 1  # Show at least 1 tick if barely alive

        health_bar = f"HP: [{'■' * filled_segments}{'-' * (bar_length - filled_segments)}]"
        bar_x = (sw - 4) // 2 - (len(health_bar) // 2)
        
        # Give the text color logic or classic bold styling
        arena_win.addstr(10, bar_x, health_bar)
    else:
        arena_win.addstr(5, (sw - 4) // 2 - 10, "* MONSTER DEFEATED *", curses.A_REVERSE)

    arena_win.noutrefresh()

    # 3. TEXT & LOG PANEL
    log_win = curses.newwin(3, sw - 4, 18, 2)
    draw_borders(log_win)
    log_win.addstr(1, 2, log_text[:sw-10])
    log_win.noutrefresh()

    # 4. COMMAND MENU
    menu_win = curses.newwin(3, sw - 4, 21, 2)
    draw_borders(menu_win)
    menu_col_width = (sw - 8) // len(menu_opt)
    for idx, opt in enumerate(menu_opt):
        mx = 3 + (idx * menu_col_width)
        if idx == menu_select:
            menu_win.addstr(1, mx, f"> {opt}", curses.A_REVERSE | curses.A_BOLD)
        else:
            menu_win.addstr(1, mx, f"  {opt}")
            
    menu_win.noutrefresh()
    curses.doupdate()

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    # Dynamic class loading setup
    player = Mage("Lucas")
    
    # Grab a random class-instantiated monster from the imported pool function
    monster = random.choice(monster_pool())
    
    special_move = "FIREBALL" if isinstance(player, Mage) else "ATTACK"
    menu_options = ["ATTACK", special_move, "RUN"]
    selected_idx = 0
    log_text = f"A wild {monster.name} draws near! Command?"
    
    while player.is_alive() and monster.is_alive():
        render_screen(stdscr, player, monster, menu_options, selected_idx, log_text)
        key = stdscr.getch()
        
        if key in (curses.KEY_LEFT, ord('a')):
            selected_idx = (selected_idx - 1) % len(menu_options)
        elif key in (curses.KEY_RIGHT, ord('d')):
            selected_idx = (selected_idx + 1) % len(menu_options)
            
        elif key in (10, 13, ord(' ')):
            action = menu_options[selected_idx]
            player_turn_done = False
            
            if action == "ATTACK":
                dmg = player.attack_target(monster)
                log_text = f"{player.name} attacks! Dealt {dmg} damage to {monster.name}."
                player_turn_done = True
                
            elif action == "FIREBALL":
                dmg = player.fireball(monster)
                if dmg is None:
                    log_text = f"Not enough MP! {player.name} fails to cast Fireball."
                else:
                    log_text = f"{player.name} casts Fireball! Burned {monster.name} for {dmg} magic damage."
                    player_turn_done = True
                
            elif action == "RUN":
                level_diff = player.level - monster.level
                escape_chance = 0.5 + (level_diff * 0.05)
                escape_chance = max(0.10, min(0.90, escape_chance))

                if random.random() < escape_chance:
                    log_text = f"{player.name} fled the battlefield..."
                    render_screen(stdscr, player, monster, menu_options, selected_idx, log_text)
                    time.sleep(1.2)
                    break
                else:
                    log_text = f"{player.name} tried to run, but the path was blocked!"
                    player_turn_done = True

            if player_turn_done:
                render_screen(stdscr, player, monster, menu_options, selected_idx, log_text)
                time.sleep(1.2)
                
                if monster.is_alive():
                    monster_dmg = monster.attack_target(player)
                    log_text = f"{monster.name} retaliates! Strikes {player.name} for {monster_dmg} damage."
                else:
                    log_text = f"The {monster.name} disintegrates! You win!"
                    
        elif key == 27:
            break

    if not player.is_alive():
        log_text = f"{player.name} has fallen in battle... Game Over."
    render_screen(stdscr, player, monster, menu_options, selected_idx, log_text)
    time.sleep(2.0)

if __name__ == "__main__":
    curses.wrapper(main)

