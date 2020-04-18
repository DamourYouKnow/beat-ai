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
        self.raw_time = None

    def json(self):
        return {
            '_time': self.time,
            '_lineIndex': self.column,
            '_lineLayer': self.row,
            '_type': int(self.type),
            '_cutDirection': int(self.direction)
        }


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


patterns = [
    # Dance notes
    [
        [
            Note(NoteType.red, 0.0, 1, 0, CutDirection.down),
            Note(NoteType.blue, 0.0, 1, 3, CutDirection.up)
        ],
        [
            Note(NoteType.red, 1.0, 1, 0, CutDirection.up),
            Note(NoteType.blue, 1.0, 1, 3, CutDirection.down)
        ]
    ],
    # Cross
    [
        [
            Note(NoteType.red, 0.0, 0, 3, CutDirection.right),
            Note(NoteType.blue, 0.0, 1, 0, CutDirection.left)
        ],
        [
            Note(NoteType.red, 1.0, 0, 0, CutDirection.left),
            Note(NoteType.blue, 1.0, 1, 3, CutDirection.right)
        ]
    ],
    # Drum roll
    [
        [
            Note(NoteType.red, 0.0, 0, 1, CutDirection.down)
        ],
        [
            Note(NoteType.blue, 0.25, 0, 2, CutDirection.none)
        ],
        [
            Note(NoteType.red, 0.50, 0, 1, CutDirection.none)
        ],
        [
            Note(NoteType.blue, 0.75, 0, 2, CutDirection.none)
        ]
    ],
    # Roller left to right
    [
        [
            Note(NoteType.red, 0.0, 0, 0, CutDirection.down),
        ],
        [
            Note(NoteType.blue, 0.25, 0, 1, CutDirection.up),
        ],
        [
            Note(NoteType.red, 0.50, 0, 2, CutDirection.up),
        ],
        [
            Note(NoteType.blue, 0.75, 0, 3, CutDirection.down),
        ]
    ],
    # Roller right to left
    [
        [
            Note(NoteType.blue, 0.0, 0, 3, CutDirection.down),
        ],
        [
            Note(NoteType.red, 0.25, 0, 2, CutDirection.up),
        ],
        [
            Note(NoteType.blue, 0.50, 0, 1, CutDirection.up),
        ],
        [
            Note(NoteType.red, 0.75, 0, 0, CutDirection.down),
        ]
    ],
]