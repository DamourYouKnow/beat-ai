import sys
import math
import statistics
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

POLLING_INTERVAL = 10


class Song:
    def __init__(self, name, audio):
        self.name = name
        self.audio = audio
        self.low_pass = self.audio.low_pass_filter(120.0)
        self.loudness = abs(self.low_pass.dBFS)
        self.segments = segments(self.low_pass, POLLING_INTERVAL)
        self.peaks = peaks(self.segments, self.loudness)

    def splice(self):
        result = self.audio[0:1]
        for s in self.peaks:
            result += self.audio[s.time-50:s.time+50]
        return result



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
    for i in range(1, len(segments)-1):
        cur, prv, nxt = segments[i], segments[i-1], segments[i+1]
        if cur.amplitude > prv.amplitude and cur.amplitude > nxt.amplitude:
            if cur.amplitude >= loudness + (loudness / 1.5):
                result.append(cur)
    return result


def chunks(arr, size):
    return [arr[x:x+size] for x in range(0, len(arr), size)]


def change(arr):
    return [arr[i] - arr[i-1] for i in range(1, len(arr))]


if __name__ == '__main__':
    filename = sys.argv[1]
    audio = AudioSegment.from_mp3(filename)
    song = Song(filename.split('.')[0], audio[0:20000])

    changes = sorted(change([p.time for p in song.peaks]))
    print(changes)
    median = changes[len(changes) // 2]
    print(60000 / median)
    print(len(song.peaks))
    print(song.loudness)

    song.splice().export('output.wav', format='wav')