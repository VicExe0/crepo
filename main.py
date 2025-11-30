from consts import MONSTER_LEVELS, EXTRACTION_AMOUNT, MONEY_MULTIPLIERS, ORB_VALUE, IDLE_TIME
from viewport import Viewport, Flags

import dearpygui.dearpygui as dpg
import webbrowser
import os

current_view = -1
always_on_top = True
save_on_close = False
auto_calc = False

level = 1
money = 1000

GITHUB = "https://github.com/VicExe0/crepo"
VIEWS = [
    [
        "level",
        "money",
        "line2",
        "money_text",
        "monster_text",
        "extract_text",
        "orb_text",
        "calc_button"
    ],
    [
        "always_on_top",
        "auto_calc",
        "save_on_close",
        "line3",
        "github",
        "version",
    ]
]

def toggleAOT() -> None:
    global always_on_top

    always_on_top = not always_on_top
    dpg.set_viewport_always_top(always_on_top)

def toggleAutoCalc() -> None:
    global auto_calc

    auto_calc = not auto_calc

def toggleSaveOnClose() -> None:
    global save_on_close

    save_on_close = not save_on_close

def update( auto: bool = False ) -> None:
    global level, money

    if auto and not auto_calc:
        return

    level = dpg.get_value("level")
    money = dpg.get_value("money")

    total_money = round(money * MONEY_MULTIPLIERS[level - 1])
    monsters = MONSTER_LEVELS[level - 1]
    extracts = EXTRACTION_AMOUNT[level - 1]
    idle_time = IDLE_TIME[level - 1]

    min_value = 0
    max_value = 0

    for i in range(3):
        min_value += monsters[i] * ORB_VALUE[i][0]
        max_value += monsters[i] * ORB_VALUE[i][1]

    dpg.set_value("money_text", f"Total money: ${total_money}")
    dpg.set_value("monster_text", f"Monsters Tiers: {monsters[0]}, {monsters[1]}, {monsters[2]}")
    dpg.set_value("extract_text", f"Extracts: {extracts} | MEM: {money * extracts}")
    dpg.set_value("idle_time", f"Idle Time: {idle_time[0]}s - {idle_time[1]}s")
    dpg.set_value("orb_text", f"Total orb value*: ${min_value} - ${max_value}")

def swapView( id: int, setup: bool = False ) -> None:
    global current_view

    if setup:
        for lst in [ v for i, v in enumerate(VIEWS) if i != id ]:
            for item in lst:
                dpg.hide_item(item)

        current_view = id
        return

    if current_view == id:
        return
    
    for item in VIEWS[current_view]:
        dpg.hide_item(item)

    for item in VIEWS[id]:
        dpg.show_item(item)

    current_view = id

def saveData() -> None:
    data = f"{int(save_on_close)};{int(always_on_top)};{int(auto_calc)};{level};{money}"

    with open("save", "w", encoding="utf8") as file:
        file.write(data)

def loadData() -> None:
    global save_on_close, always_on_top, auto_calc

    if not os.path.exists("save"):
        return

    with open("save", "r", encoding="utf8") as file:
        data = file.read()

    parts = data.split(";")
    save_on_close = bool(parts[0])
    always_on_top = bool(parts[1])
    auto_calc = bool(parts[2])
    level = int(parts[3])
    money = int(parts[4])

    dpg.set_value("always_on_top", always_on_top)
    dpg.set_value("auto_calc", auto_calc)
    dpg.set_value("save_on_close", save_on_close)
    dpg.set_value("level", level)
    dpg.set_value("money", money)

    update(True)

def layout() -> None:
    # Tab bar
    with dpg.group(horizontal=True, horizontal_spacing=4):
        dpg.add_button(label="Level", width=140, callback=lambda: swapView(0))
        dpg.add_button(label="Settings", width=140, callback=lambda: swapView(1))

    with dpg.drawlist(width=300, height=10, tag="line1"):
        dpg.draw_line(( 0,  5), ( 284, 5 ), color=( 80, 80, 80, 255 ), thickness=1)

    # Tab "Level"
    dpg.add_input_int(label="Level", width=200, default_value=1, min_value=1, max_value=1000000, tag="level", callback=lambda: update(True))
    dpg.add_input_int(label="Money", width=200, default_value=1000, min_value=1, max_value=1000000, tag="money", callback=lambda: update(True))
    
    with dpg.drawlist(width=300, height=10, tag="line2"):
        dpg.draw_line(( 0,  5), ( 284, 5 ), color=( 80, 80, 80, 255 ), thickness=1)
    
    dpg.add_text("Total money: X", tag="money_text")
    dpg.add_text("Monsters Tiers: X, X, X", tag="monster_text")
    dpg.add_text("Extracts: X | MEM: X", tag="extract_text")
    dpg.add_text("Idle Time: Xs - Xs", tag="idle_time")
    dpg.add_text("Total orb value*: X - X", tag="orb_text")
    
    dpg.add_button(label="Calculate", width=284, callback=lambda: update(False), tag="calc_button")

    # Tab "Settings"
    dpg.add_checkbox(label="Always on top", tag="always_on_top", default_value=True, callback=toggleAOT)
    dpg.add_checkbox(label="Auto calculate", tag="auto_calc", default_value=False, callback=toggleAutoCalc)
    dpg.add_checkbox(label="Save on quit", tag="save_on_close", default_value=False, callback=toggleSaveOnClose)

    with dpg.drawlist(width=300, height=10, tag="line3"):
        dpg.draw_line(( 0,  5), ( 284, 5 ), color=( 80, 80, 80, 255 ), thickness=1)
    
    dpg.add_button(label="Open github page", width=284, callback=lambda: webbrowser.open(GITHUB), tag="github")

    dpg.add_text("Version: 1.2", tag="version")

    swapView(0, True)

    loadData()

def main() -> None:
    viewport = Viewport("CREPO by VicExe0", ( 300, 335 ), layout, Flags.CENTERED | Flags.DRAG_ONLY_TITLEBAR | Flags.ALWAYS_ON_TOP | Flags.NO_SCROLLBAR)
    viewport.setFont("Poppins-Regular.ttf")

    viewport.start(180)


if __name__ == "__main__":
    try:
        main()
    
    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e)

    finally:
        if save_on_close:
            saveData()

        elif os.path.exists("save"):
            os.remove("save")