from typing import Dict


CONTROLLER_8BITDO_BUTTONS_MAP = {
    0: "B",
    1: "A",
    2: "Y",
    3: "X",
    7: "L3",
    8: "R3",
    9: "L1",
    10: "R1",
    11: "UP",
    12: "DOWN",
    13: "LEFT",
    14: "RIGHT",
    6: "START",
    4: "SELECT",
    15: "SHARE",
}

CONTROLLER_8BITDO_AXIS_MAP = {
    0: "LX",
    1: "LY",
    2: "RX",
    3: "RY",
    4: "L2",
    5: "R2",
}


CONTROLLER_BUTTON_MAP = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "L1",
    5: "R1",
    6: "SELECT",
    7: "START",
    9: "Left Stick Click",
    10: "Right Stick Click",
}

CONTROLLER_AXIS_MAP = {
    0: "LX",
    1: "LY",
    2: "RX",
    3: "RY",
    4: "L2",
    5: "R2",
}

BUTTON_MAPS = {
    "8bitdo": CONTROLLER_8BITDO_BUTTONS_MAP,
    "default": CONTROLLER_BUTTON_MAP,
}

AXIS_MAPS = {
    "8bitdo": CONTROLLER_8BITDO_AXIS_MAP,
    "default": CONTROLLER_AXIS_MAP,
}


def get_button_name(
    button_number: int, mapping: Dict[int, str] = CONTROLLER_BUTTON_MAP
) -> str:
    return mapping.get(button_number, str(button_number))


def get_axis_name(
    axis_number: int, mapping: Dict[int, str] = CONTROLLER_AXIS_MAP
) -> str:
    return mapping.get(axis_number, str(axis_number))
