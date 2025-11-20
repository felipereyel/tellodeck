from typing import Dict


JOYSTICK_8BITDO_BUTTONS_MAP = {
    0: "B",
    1: "A",
    2: "Y",
    3: "X",
    9: "L1",
    10: "R1",
    11: "UP",
    12: "DOWN",
    13: "LEFT",
    14: "RIGHT",
    6: "START",
    4: "SELECT",
}


JOYSTICK_BUTTON_MAP = {
    0: "A / Cross",
    1: "B / Circle",
    2: "X / Square",
    3: "Y / Triangle",
    4: "Left Bumper",
    5: "Right Bumper",
    6: "Back / Select",
    7: "Start",
    8: "Guide / Home",
    9: "Left Stick Click",
    10: "Right Stick Click",
}

BUTTON_MAPS = {
    "8bitdo": JOYSTICK_8BITDO_BUTTONS_MAP,
    "default": JOYSTICK_BUTTON_MAP,
}


def get_button_name(
    button_number: int, mapping: Dict[int, str] = JOYSTICK_BUTTON_MAP
) -> str:
    return mapping.get(button_number, str(button_number))
