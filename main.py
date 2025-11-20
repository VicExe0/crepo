from consts import MONSTER_LEVELS, EXTRACTION_AMOUNT, MONEY_MULTIPLIERS, ORB_VALUE
from viewport import Viewport, Flags

import dearpygui.dearpygui as dpg

def update( ) -> None:
    level = dpg.get_value("level")
    money = dpg.get_value("money")

    total_money = round(money * MONEY_MULTIPLIERS[level - 1])
    monsters = MONSTER_LEVELS[level - 1]
    extracts = EXTRACTION_AMOUNT[level - 1]

    min_value = 0
    max_value = 0

    for i in range(3):
        min_value += monsters[i] * ORB_VALUE[i][0]
        max_value += monsters[i] * ORB_VALUE[i][1]

    dpg.set_value("money_text", f"Total money: ${total_money}")
    dpg.set_value("monster_text", f"Monsters Tiers: {monsters[0]}, {monsters[1]}, {monsters[2]}")
    dpg.set_value("extract_text", f"Extracts: {extracts}")
    dpg.set_value("orb_text", f"Total orb value*: ${min_value} - ${max_value}")


def layout() -> None:
    dpg.add_input_int(label="Level", width=150, default_value=1, min_value=1, max_value=1000000, tag="level")
    dpg.add_input_int(label="Money", width=150, default_value=1000, min_value=1, max_value=1000000, tag="money")

    with dpg.drawlist(width=300, height=10):
        dpg.draw_line((0, 5), (280, 5), color=(150, 150, 150, 255), thickness=2)

    dpg.add_text("Total money: N/A", tag="money_text")
    dpg.add_text("Monsters Tiers: X, X, X", tag="monster_text")
    dpg.add_text("Extracts: N/A", tag="extract_text")
    dpg.add_text("Total orb value*: X - X", tag="orb_text")

    dpg.add_button(label="Calculate", width=283, callback=update)

def main() -> None:
    viewport = Viewport("CREPO by VicExe", ( 300, 265 ), layout, Flags.CENTERED | Flags.DRAG_ONLY_TITLEBAR | Flags.ALWAYS_ON_TOP | Flags.NO_SCROLLBAR)
    viewport.setFont("Poppins-Regular.ttf")

    viewport.start(180)


if __name__ == "__main__":
    try:
        main()
    
    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e)