import os
import sys
import math
import json
import statistics
from enum import Enum
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

POLLING_INTERVAL = 20


class Song:
    def __init__(self, name, audio):
        self.name = name
        self.audio = audio
        self.low_pass = self.audio.low_pass_filter(120.0)
        self.loudness = abs(self.low_pass.dBFS)
        self.segments = segments(self.low_pass, POLLING_INTERVAL)
        self.peaks = peaks(self.segments, self.loudness)
        self.bpm = self._calculate_bpm()
        self.chart = self.create_level()

    def splice(self):
        result = self.audio[0:1]
        for s in self.peaks:
            result += self.audio[s.time-50:s.time+50]
        return result

    def create_level(self):
        level = []
        for peak in self.peaks:
            note = Note(
                NoteType.blue,
                self.adjusted_time(peak.time),
                0, 0,
                CutDirection.none
            )
            level.append(note)
        return level

    def adjusted_time(self, time):
        beat_time = (1 / self.bpm) * 60 * 1000
        return time / beat_time

    def export(self):
        if not os.path.exists('output'):
            os.mkdir('output')
        with open('./output/info.data', 'w') as fr:
            fr.write(json.dumps(self.metadata_json()))
            fr.close()
        with open('./output/AI.dat', 'w') as fr:
            fr.write(json.dumps(self.level_json()))
            fr.close()

    def level_json(self):
        return {
            '_events': [], # Cool light stuff goes here but is not a priority.
            '_notes': [note.json() for note in self.chart],
            '_obstacles': [] # We won't worry about walls for now.
        }

    def metadata_json(self):
        return {
            '_version': '2.0.0',
            '_songName': self.name,
            '_songSubName': 'TODO',
            '_songAuthorName': 'TODO',
            '_levelAuthorName': 'Beat A.I.',
            '_beatsPerMinute': self.bpm,
            '_shuffle': 0,
            '_shufflePeriod': 0.5, # WTF is this?
            '_previewStartTime': 0,
            '_previewDuration': 15,
            '_songFilename': f'{self.name}.ogg',
            '_environmentNane': 'BigMirrorEnvironment',
            '_songTimeOffset': 0,
            '_difficultyBeatmapSets': [
                {
                    '_beatmapCharacteristicName': 'Standard',
                    '_difficultyBeatmaps': [
                        {
                            '_difficulty': 'AI',
                            '_difficultyRank': 7,
                            '_beatmapFilename': 'AI.dat',
                            '_noteJumpMovementSpeed': 12,
                            '_noteJumpStartBeatOffset': 0
                        }
                    ]
                }
            ]
        }   

    def _calculate_bpm(self):
        changes = sorted(change([peak.time for peak in self.peaks]))
        median = changes[len(changes) // 2]
        bpm = (60 * 1000) / median
        # A wacky BPM calculate shouldn't really matter to us, I think...
        if bpm > 200:
            return 200
        if bpm < 50:
            return 50
        return bpm




'''
Data file format:

notes - array of notes
type - color of note (0, 1) or bomb (3)
lineIndex - column
lineLayer - row
cutDirection - direction of note (0-7) or dot (8)
'''
class NoteType(Enum):
    red = 0
    blue = 1
    bomb = 3

class CutDirection(Enum):
    up = 0
    up_right = 1
    right = 2
    down_right = 3
    down = 4
    down_left = 5
    left = 6
    up_left = 7
    none = 8


class Note:
    def __init__(self, note_type, time, row, column, direction):
        self.type = note_type
        self.time = time
        self.row, self.column = row, column
        self.direction = direction

    def json(self):
        return {
            '_time': self.time,
            '_lineIndex': self.column,
            '_lineLayer': self.row,
            '_type': self.type,
            '_cutDirection': self.direction
        }


class Segment:
    def __init__(self, time, amplitude):
        self.time = time
        self.amplitude = amplitude

    def __repr__(self):
        return f'{self.time}: {self.amplitude}'


def segments(audio, interval):
    intervals = chunks(audio, interval)
    offset = interval / 2
    return [
        Segment((i * interval) + offset, abs(intervals[i].dBFS))
        for i in range(len(intervals))
    ]


def peaks(segments, loudness):
    result = []
    last_peak = 0
    for i in range(1, len(segments)-1):
        cur, prv, nxt = segments[i], segments[i-1], segments[i+1]
        delta = cur.time - last_peak
        if cur.amplitude > prv.amplitude and cur.amplitude > nxt.amplitude:
            if cur.amplitude >= loudness + (loudness / 2) and delta >= 100:
                result.append(cur)
                last_peak = cur.time
    return result


def chunks(arr, size):
    return [arr[x:x+size] for x in range(0, len(arr), size)]


def change(arr):
    return [arr[i] - arr[i-1] for i in range(1, len(arr))]


if __name__ == '__main__':
    filename = sys.argv[1]
    audio = AudioSegment.from_mp3(filename)
    song = Song(filename.split('.')[0], audio[0:20000])

    print('\n'.join([str(s) for s in song.segments]))
    print(f'bpm={song.bpm}')
    print(song.loudness)

    song.splice().export('output.wav', format='wav')

# Shoutout to Daniwell