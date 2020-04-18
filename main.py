import sys
import os
from pydub import AudioSegment
from core import Song


if __name__ == '__main__':
    filename = sys.argv[1]
    audio = AudioSegment.from_mp3(filename)
    song = Song(os.path.basename(filename).split('.')[0], audio[0:30000])
    song.export()

# Shoutout to Daniwell