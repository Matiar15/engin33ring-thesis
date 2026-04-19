"""
Label mapping for GTSDB fine-grained class IDs (43 traffic sign classes).
Copied from ml/src/label_mapping.py to avoid cross-project imports.
"""

# fmt: off
GTSDB_FINE_NAMES: dict[int, str] = {
    0: "speed_limit_20",
    1: "speed_limit_30",
    2: "speed_limit_50",
    3: "speed_limit_60",
    4: "speed_limit_70",
    5: "speed_limit_80",
    6: "end_speed_limit_80",
    7: "speed_limit_100",
    8: "speed_limit_120",
    9: "no_overtaking",
    10: "no_overtaking_trucks",
    11: "right_of_way",
    12: "priority_road",
    13: "yield",
    14: "stop",
    15: "no_vehicles",
    16: "no_trucks",
    17: "no_entry",
    18: "general_caution",
    19: "dangerous_curve_left",
    20: "dangerous_curve_right",
    21: "double_curve",
    22: "bumpy_road",
    23: "slippery_road",
    24: "road_narrows_right",
    25: "road_work",
    26: "traffic_signals",
    27: "pedestrians",
    28: "children_crossing",
    29: "bicycles_crossing",
    30: "ice_snow",
    31: "wild_animals",
    32: "end_all_limits",
    33: "turn_right_ahead",
    34: "turn_left_ahead",
    35: "ahead_only",
    36: "straight_or_right",
    37: "straight_or_left",
    38: "keep_right",
    39: "keep_left",
    40: "roundabout",
    41: "end_no_overtaking",
    42: "end_no_overtaking_trucks",
}
# fmt: on

