import os
import math
import json
import random
from shutil import rmtree
from data import Note, NoteType, CutDirection, directions


POLLING_INTERVAL = 10
LENIENCY = 6


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

        # Function inputs note, delta, outputs valid notes

        


        level = []
        for i in range(len(self.peaks)):
            peak = self.peaks[i]

            row, col = random.randint(0, 2), random.randint(0, 3)
            time = self.adjusted_time(peak.time)
            note_type = random.choice([NoteType.blue, NoteType.red])
            direction = CutDirection(random.randint(0, 7))
            if i-1 >= 0:
                last_note = level[len(level)-1]
                direction = random.choice(
                    directions[last_note.direction]
                )

            note = Note(note_type, time, row, col, direction)
            note.raw_time = peak.time
            level.append(note)

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
        if not delta >= 100:
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


def count(arr, predicate):
    return sum(predicate(x) for x in arr)