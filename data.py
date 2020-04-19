from enum import Enum


class NoteType(Enum):
    red = 0
    blue = 1
    bomb = 3

    def __int__(self):
        return self.value


class CutDirection(Enum):
    up = 0
    up_right = 5
    right = 3
    down_right = 7
    down = 1
    down_left = 6
    left = 2
    up_left = 4
    none = 8

    def __int__(self):
        return self.value


class Note:
    def __init__(self, note_type, time, row, column, direction):
        self.type = note_type
        self.time = time
        self.row, self.column = row, column
        self.direction = direction
        self.classified = False

    def json(self):
        return {
            '_time': self.time,
            '_lineIndex': self.column,
            '_lineLayer': self.row,
            '_type': int(self.type),
            '_cutDirection': int(self.direction)
        }

    def __repr__(self):
        s = f'[time={self.time}, type={int(self.type)}, '
        s += f'pos=({self.row}, {self.column})]'
        return s


# [Easy, Medium, Medium, Hard, Hard]
directions = {
    CutDirection.up: [
        CutDirection.down,
        CutDirection.down_left,
        CutDirection.down_right,
        CutDirection.left,
        CutDirection.right
    ],
    CutDirection.down: [
        CutDirection.up,
        CutDirection.up_left,
        CutDirection.up_right,
        CutDirection.left,
        CutDirection.right
    ],
    CutDirection.left: [
        CutDirection.right,
        CutDirection.up_right,
        CutDirection.down_right,
        CutDirection.up,
        CutDirection.down
    ],
    CutDirection.right: [
        CutDirection.left,
        CutDirection.up_left,
        CutDirection.down_left,
        CutDirection.up,
        CutDirection.down
    ],
    CutDirection.up_right: [
        CutDirection.down_left,
        CutDirection.left,
        CutDirection.down,
        CutDirection.up_left,
        CutDirection.down_right
    ],
    CutDirection.up_left: [
        CutDirection.down_right,
        CutDirection.right,
        CutDirection.down,
        CutDirection.down_left,
        CutDirection.up_right
    ],
    CutDirection.down_right: [
        CutDirection.up_left,
        CutDirection.up,
        CutDirection.left,
        CutDirection.up_right,
        CutDirection.down_left
    ],
    CutDirection.down_left: [
        CutDirection.up_right,
        CutDirection.up,
        CutDirection.right,
        CutDirection.up_left,
        CutDirection.down_right
    ]
}


class PatternType(Enum):
    dance = 0
    cross = 1
    drumroll = 2
    roll_lr = 3
    roll_rl = 4
    tap_red = 5
    tap_blue = 6
    tap_red_half = 5
    tap_blue_half = 6
    alt_narrow = 7
    alt_wide = 8
    sides = 9
    handle_right = 10
    handle_left = 11
    scoop_right = 12
    scoop_left = 13
    wave_right = 14
    wave_left = 14
    hop_wide_right = 15
    hop_wide_left = 16
    hop_narrow_right = 17
    hop_narrow_left = 18
    wheel_right = 19
    wheel_left = 20
    up_down = 21

    def __int__(self):
        return self.value


class PNote:
    def __init__(self, note_type, rows, cols, direction):
        self.type = note_type
        self.row = rows
        self.col = cols
        self.direction = direction


class Pattern:
    def __init__(self, timings, notes):
        self.timings = timings
        self.notes = notes


patterns = {
    PatternType.dance: Pattern(
        [[0.0, 1.0], [0.0, 0.5]], 
        [
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
                PNote(NoteType.blue, 1, 2, CutDirection.up)
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.up),
                PNote(NoteType.blue, 0, 2, CutDirection.down)
            ]
        ]
    ),
    PatternType.cross: Pattern(
        [[0.0, 1.0]],
        [
            [
                PNote(NoteType.red, 0, 2, CutDirection.right),
                PNote(NoteType.blue, 1, 0, CutDirection.left)
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.left),
                PNote(NoteType.blue, 1, 2, CutDirection.right)
            ]
        ]
    ),
    PatternType.drumroll: Pattern(
        [[0.0, 0.25, 0.5, 0.75]],
        [
            [
                PNote(NoteType.red, 0, 1, CutDirection.down)
            ],
            [
                PNote(NoteType.blue, 0, 2, CutDirection.none)
            ],
            [
                PNote(NoteType.red, 0, 1, CutDirection.none)
            ],
            [
                PNote(NoteType.blue, 0, 2, CutDirection.none)
            ]
        ]
    ),
    PatternType.roll_lr: Pattern(
        [[0.0, 0.25, 0.5, 0.75], [0.0, 0.5, 0.75, 1.0]],
        [
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 0, 1, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 0, 2, CutDirection.up),
            ],
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ]
        ]
    ),
    PatternType.roll_rl: Pattern(
        [[0.0, 0.25, 0.5, 0.75]],
        [
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 0, 2, CutDirection.up),
            ],
            [
                PNote(NoteType.blue, 0, 1, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_red: Pattern(
        [[0.0, 1.0, 2.0, 3.0], [0.0, 0.5, 1.0, 1.5]],
        [
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_blue: Pattern(
        [[0.0, 1.0, 2.0, 3.0], [0.0, 0.5, 1.0, 1.5]],
        [
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_red_half: Pattern(
        [[0.0, 1.0], [0.0, 0.5]],
        [
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_blue_half: Pattern(
        [[0.0, 1.0], [0.0, 0.5]],
        [
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
        ]
    ),
    PatternType.alt_narrow: Pattern(
        [[0.0, 0.25, 0.5, 0.75], [0.0, 0.5, 1.0, 1.5], [0.0, 1.0, 2.0, 3.0]],
        [
            [
                PNote(NoteType.blue, 0, 2, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 0, 2, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 0, 1, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 0, 1, CutDirection.up),
            ],
        ]
    ),
    PatternType.alt_wide: Pattern(
        [[0.0, 0.25, 0.5, 0.75], [0.0, 0.5, 1.0, 1.5], [0.0, 1.0, 2.0, 3.0]],
        [
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 0, 3, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 0, 0, CutDirection.up),
            ],
        ]
    ),
    PatternType.sides: Pattern(
        [[0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.blue, 1, 2, CutDirection.right),
                PNote(NoteType.red, 0, 2, CutDirection.right),
            ],
            [
                PNote(NoteType.blue, 1, 0, CutDirection.left),
                PNote(NoteType.red, 0, 0, CutDirection.left),
            ]
        ]
    ),
    PatternType.handle_right: Pattern(
        [[0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.blue, 0, 2, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.right),
            ]
        ]
    ),
    PatternType.handle_left: Pattern(
        [[0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.red, 0, 1, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.left),
            ]
        ]
    ),
    PatternType.scoop_right: Pattern(
        [[0.0, 0.25], [0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 2, CutDirection.up),
            ]
        ]
    ),
    PatternType.scoop_left: Pattern(
        [[0.0, 0.25], [0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 1, CutDirection.up),
            ]
        ]
    ),
    PatternType.wave_right: Pattern(
        [[0.0, 0.25], [0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.blue, 1, 3, CutDirection.right),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.left),
            ]
        ]
    ),
    PatternType.wave_left: Pattern(
        [[0.0, 0.25], [0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.red, 1, 0, CutDirection.left),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.right),
            ]
        ]
    ),
    PatternType.hop_wide_right: Pattern(
        [[0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.blue, 1, 0, CutDirection.up),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ]
        ]
    ),
    PatternType.hop_wide_left: Pattern(
        [[0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.red, 1, 3, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ]
        ]
    ),
    PatternType.hop_narrow_right: Pattern(
        [[0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.blue, 1, 3, CutDirection.up),
            ],
            [
                PNote(NoteType.blue, 1, 1, CutDirection.down),
            ]
        ]
    ),
    PatternType.hop_narrow_left: Pattern(
        [[0.0, 0.5], [0.0, 1.0]],
        [
            [
                PNote(NoteType.red, 1, 0, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 1, 2, CutDirection.down),
            ]
        ]
    ),
    PatternType.wheel_right: Pattern(
        [[0.0, 0.25, 0.75], [0.0, 0.5, 1.0], [0.0, 1.0, 2.0]],
        [
            [
                PNote(NoteType.blue, 0, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 2, CutDirection.up),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ]
        ]
    ),
    PatternType.wheel_left: Pattern(
        [[0.0, 0.25, 0.75], [0.0, 0.5, 1.0], [0.0, 1.0, 2.0]],
        [
            [
                PNote(NoteType.red, 0, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 1, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ]
        ]
    )
}