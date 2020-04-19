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
                PNote(NoteType.red, 1, 0, CutDirection.down),
                PNote(NoteType.blue, 2, 2, CutDirection.up)
            ],
            [
                PNote(NoteType.red, 2, 0, CutDirection.up),
                PNote(NoteType.blue, 1, 2, CutDirection.down)
            ]
        ]
    ),
    PatternType.cross: Pattern(
        [[0.0, 1.0]],
        [
            [
                PNote(NoteType.red, 1, 2, CutDirection.right),
                PNote(NoteType.blue, 2, 0, CutDirection.left)
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.left),
                PNote(NoteType.blue, 2, 2, CutDirection.right)
            ]
        ]
    ),
    PatternType.drumroll: Pattern(
        [[0.0, 0.25, 0.50, 0.75]],
        [
            [
                PNote(NoteType.red, 1, 1, CutDirection.down)
            ],
            [
                PNote(NoteType.blue, 1, 2, CutDirection.none)
            ],
            [
                PNote(NoteType.red, 1, 1, CutDirection.none)
            ],
            [
                PNote(NoteType.blue, 1, 2, CutDirection.none)
            ]
        ]
    ),
    PatternType.roll_lr: Pattern(
        [[0.0, 0.25, 0.50, 0.75]],
        [
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 1, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 1, 2, CutDirection.up),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ]
        ]
    ),
    PatternType.roll_rl: Pattern(
        [[0.0, 0.25, 0.50, 0.75]],
        [
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 2, CutDirection.up),
            ],
            [
                PNote(NoteType.blue, 1, 1, CutDirection.up),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_red: Pattern(
        [[0.0, 1.0, 2.0, 3.0], [0.0, 0.5, 1.0, 1.5]],
        [
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_blue: Pattern(
        [[0.0, 1.0, 2.0, 3.0], [0.0, 0.5, 1.0, 1.5]],
        [
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_red_half: Pattern(
        [[0.0, 1.0], [0.0, 0.5]],
        [
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ],
            [
                PNote(NoteType.red, 1, 0, CutDirection.down),
            ]
        ]
    ),
    PatternType.tap_blue_half: Pattern(
        [[0.0, 1.0], [0.0, 0.5]],
        [
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ],
            [
                PNote(NoteType.blue, 1, 3, CutDirection.down),
            ],
        ]
    )
}