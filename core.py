import os
import math
import json
import random
from shutil import rmtree
from data import Note, NoteType, CutDirection, directions, patterns


POLLING_INTERVAL = 10
LENIENCY = 8


class Segment:
    def __init__(self, time, amplitude):
        self.time = time
        self.amplitude = amplitude

    def __repr__(self):
        return f'{self.time}: {self.amplitude}'


class Song:
    def __init__(self, name, audio):
        self.name = name
        self.audio = audio
        self.low_pass = self.audio.low_pass_filter(120.0)
        self.loudness = abs(self.low_pass.dBFS)
        self.segments = segments(self.low_pass, POLLING_INTERVAL)
        self.peaks = peaks(self.low_pass, self.segments)
        self.bpm = self._calculate_bpm()
        self.chart = self.create_level()

    def splice(self):
        result = self.audio[0:1]
        for s in self.peaks:
            result += self.audio[s.time-50:s.time+50]
        return result

    def create_level(self):
        random.seed(1)
        max_pattern_length = max(len(p.timings) for p in patterns.values())

        level = []
        i = 0
        last_note = None
        while i < len(self.peaks):
            options = []
            nxt = []
            peak = self.peaks[i]

            # Try to find pattern.
            for length in range(1, max_pattern_length + 1):
                # Make sure we don't go out of bounds.
                if i + length >= len(self.peaks):
                    continue
    
                matching = [
                    p for p in patterns.values() if len(p.timings[0]) == length
                ]
                for match in matching:
                    times = [p.time for p in self.peaks[i:i+length]]
                    r = [0.0] + [get_range(t) for t in change(times)]
                    ranges = [sum(r[:k]) + r[k] for k in range(len(r))]

                    # Make sure the intervals match
                    if count(match.timings, lambda x: ranges == x) == 0:
                        continue

                    # Make sure we don't change directions abruptly
                    first = match.notes[0][0]
                    if last_note and \
                        not first.direction in directions[last_note.direction]:
                        continue

                    options.append(match.notes)
      
            # Do we have options
            if options:
                choice = random.choice(options)
                for c in range(len(choice)):
                    for note in choice[c]:
                        nxt.append(Note(
                            note.type,
                            self.adjusted_time(self.peaks[i+c].time),
                            note.row, note.col,
                            note.direction
                        ))
                i += len(choice)

            if not nxt:
                # Resort to randomness if we can't find a matching pattern.
                row, col = random.randint(0, 2), random.randint(0, 3)
                time = self.adjusted_time(peak.time)
                note_type = random.choice([NoteType.blue, NoteType.red])
                direction = CutDirection(random.randint(0, 7))

                if i-1 >= 0:
                    last_note = level[len(level)-1]
                    direction = random.choice(
                        directions[last_note.direction]
                    )

                print('hai')
                nxt = [Note(note_type, time, row, col, direction)]
                i += 1

            level += nxt
            last_note = level[len(level)-1]

        print('\n'.join([str(n) for n in level]))
        return level

    def adjusted_time(self, time):
        beat_time = (1 / self.bpm) * 60 * 1000
        return time / beat_time

    def export(self):
        outdir, songdir = './output', f'./output/{self.name}'
        infopath, datapath = f'{songdir}/info.dat', f'{songdir}/AI.dat'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        if os.path.exists(songdir):
            rmtree(songdir)
        os.mkdir(songdir)
        with open(infopath, 'w') as fr:
            fr.write(json.dumps(self.metadata_json()))
            fr.close()
        with open(datapath, 'w') as fr:
            fr.write(json.dumps(self.level_json()))
            fr.close()
        self.audio.export(f'{songdir}/{self.name}.ogg', format='ogg')

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


def segments(audio, interval):
    intervals = chunks(audio, interval)
    offset = interval / 2
    return [
        Segment((i * interval) + offset, abs(intervals[i].dBFS))
        for i in range(len(intervals))
    ]


def peaks(audio, segments):
    result = []
    last_peak = 0
    for i in range(1, len(segments)-1):
        cur, prv, nxt = segments[i], segments[i-1], segments[i+1]
        delta = cur.time - last_peak
        left = [s for s in segments[i-LENIENCY:i]]
        right = [s for s in segments[i+1:i+LENIENCY+1]]
        sides = left + right

        # Check if segment louder than all adjacent segments. 
        if not all(sides, lambda s: cur.amplitude > s.amplitude):
            continue

        # Check if there is distinction between current segment and adjacent
        # segments.
        distinct = lambda s: s.amplitude < cur.amplitude * 0.75
        if not (count(left, distinct) >= 1 and count(right, distinct) >= 1):
            continue 

        # Check if all near segments are above loudness threshold for the frame.
        loudness = abs(audio[cur.time-3000:cur.time+5000].dBFS)       
        if not all(sides, lambda s: s.amplitude > loudness * 0.5):
            continue
        
        # Sanity check for placing notes too close to each other.
        if not delta >= 10:
            continue

        result.append(cur)
        last_peak = cur.time

    # TODO: Weave merge close notes.
    return result


def chunks(arr, size):
    return [arr[x:x+size] for x in range(0, len(arr), size)]


def change(arr):
    return [arr[i] - arr[i-1] for i in range(1, len(arr))]


def all(arr, predicate):
    for x in arr:
        if not predicate(x):
            return False
    return True


def in_range(value, range):
    return range[0] <= value < range[1]


def get_range(value):
    value = value / 1000
    time_ranges = {
        # (100bpm, 200bpm)
        (0.075, 0.15): 0.25,
        (0.15, 0.30): 0.50,
        (0.30, 0.60): 1.0
    }
    for r in time_ranges:
        if in_range(value, r):
            return time_ranges[r]
    return -1


def flatten(arr):
    [item for sublist in arr for item in sublist]


def count(arr, predicate):
    return sum(predicate(x) for x in arr)