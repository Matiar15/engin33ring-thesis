"""
Mapping of GTSDB fine-grained class IDs for YOLO training.

GTSDB contains 43 classes of German traffic signs. We use all 43 classes
directly as YOLO class IDs (identity mapping: GTSDB ID == YOLO ID).

A super-category grouping (4 groups) is kept as a utility for visualisation
and analytics, but training uses fine-grained labels.
"""

# fmt: off

# ── Fine-grained class names (43 classes) ───────────────────────
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

# Set of all valid GTSDB class IDs (0–42)
VALID_GTSDB_IDS: set[int] = set(GTSDB_FINE_NAMES.keys())

# ── Super-category grouping (for analytics / dashboards) ────────
GTSDB_CLASS_TO_SUPERCATEGORY: dict[int, int] = {
    # ── prohibitory (0) ──────────────────────
    0: 0,   # speed limit 20
    1: 0,   # speed limit 30
    2: 0,   # speed limit 50
    3: 0,   # speed limit 60
    4: 0,   # speed limit 70
    5: 0,   # speed limit 80
    6: 0,   # end of speed limit 80
    7: 0,   # speed limit 100
    8: 0,   # speed limit 120
    9: 0,   # no overtaking
    10: 0,  # no overtaking for trucks
    13: 0,  # yield
    14: 0,  # stop
    15: 0,  # no vehicles
    16: 0,  # no trucks
    17: 0,  # no entry
    # ── mandatory (1) ────────────────────────
    33: 1,  # turn right ahead
    34: 1,  # turn left ahead
    35: 1,  # ahead only
    36: 1,  # go straight or right
    37: 1,  # go straight or left
    38: 1,  # keep right
    39: 1,  # keep left
    40: 1,  # roundabout mandatory
    41: 1,  # end of no overtaking
    42: 1,  # end of no overtaking for trucks
    # ── danger (2) ───────────────────────────
    11: 2,  # right-of-way at next intersection
    18: 2,  # general caution
    19: 2,  # dangerous curve left
    20: 2,  # dangerous curve right
    21: 2,  # double curve
    22: 2,  # bumpy road
    23: 2,  # slippery road
    24: 2,  # road narrows on the right
    25: 2,  # road work
    26: 2,  # traffic signals
    27: 2,  # pedestrians
    28: 2,  # children crossing
    29: 2,  # bicycles crossing
    30: 2,  # beware of ice/snow
    31: 2,  # wild animals crossing
    # ── other (3) ────────────────────────────
    12: 3,  # priority road
    32: 3,  # end of all speed and passing limits
}
# fmt: on

SUPERCATEGORY_NAMES: dict[int, str] = {
    0: "prohibitory",
    1: "mandatory",
    2: "danger",
    3: "other",
}


def fine_class_name(gtsdb_class_id: int) -> str:
    """Return the human-readable name for a GTSDB fine-grained class ID."""
    if gtsdb_class_id not in GTSDB_FINE_NAMES:
        raise ValueError(
            f"Unknown GTSDB class ID: {gtsdb_class_id}. Valid range: 0–42."
        )
    return GTSDB_FINE_NAMES[gtsdb_class_id]


def supercategory_id(gtsdb_class_id: int) -> int:
    """Map a GTSDB fine-grained class ID to a super-category ID."""
    if gtsdb_class_id not in GTSDB_CLASS_TO_SUPERCATEGORY:
        raise ValueError(
            f"Unknown GTSDB class ID: {gtsdb_class_id}. Valid range: 0–42."
        )
    return GTSDB_CLASS_TO_SUPERCATEGORY[gtsdb_class_id]


def supercategory_name(gtsdb_class_id: int) -> str:
    """Map a GTSDB fine-grained class ID to a super-category name."""
    return SUPERCATEGORY_NAMES[supercategory_id(gtsdb_class_id)]
