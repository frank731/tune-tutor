import librosa
import pyaudio
from time import sleep
import numpy as np
from math import isnan
import matplotlib.pyplot as plt
from collections import Counter, deque

class AudioHandler:
    def __init__(self, chord_display_func):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 22050
        self.CHUNK = 1024 * 2
        self.WINDOW = int(self.RATE * 0.3)
        self.AUDIO_THRESH = 0.2
        self.p = None
        self.stream = None
        self.rec = np.array([])
        self.chord_display_func = chord_display_func

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  stream_callback=self.callback,
                                  frames_per_buffer=self.CHUNK)
        print("Listening")

    def stop(self):
        self.stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        #take 0.3 sec windows
        self.rec = np.append(self.rec, audio_data)
        if len(self.rec) > self.WINDOW:
            self.rec = self.rec[len(self.rec) - self.WINDOW:]

        m = np.max(self.rec)
        if(m > self.AUDIO_THRESH): #possibly do rolling max
            self.calc_chord()
        return None, pyaudio.paContinue
    
    def calc_chord(self):
        chromagram = librosa.feature.chroma_cens(y=self.rec, sr=self.RATE, win_len_smooth=60)
        mean_chroma = np.mean(chromagram, axis=1)

        estimated_chord = self.identify_chord(mean_chroma) # check if estimated chord is the same for a while

        if estimated_chord:
            self.chord_display_func(estimated_chord)

    def identify_chord(self, chromagram): # takes in mean chromagram
        patterns = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'diminished': [0, 3, 6],
            
        }
        note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        """
        Tests
        Working: Cmaj, C#maj, C#min, Dmaj, Dmin, D#maj, D#min, Emaj, Emin, Fmaj, Fmin, F#maj, F#min, Gmaj, Gmin, G#maj, G#min, Amaj, Amin, A#maj, A#min, Bmaj, Bmin
        Not working: Cmin sometimes shows as F# minor 
        """
        
        threshold = 0.4 * max(chromagram)
        significant_notes = [i for i, x in enumerate(chromagram) if x > threshold]
        chord_scores = {}

        for root in significant_notes:
            for chord_type, pattern in patterns.items():
                if all((root + interval) % 12 in significant_notes for interval in pattern):
                    # Calculate weighted score for the chord
                    score = sum(chromagram[(root + interval) % 12] for interval in pattern)
                    chord_name = note_name[root] + ' ' + chord_type
                    chord_scores[chord_name] = max(chord_scores.get(chord_name, 0), score)

        # Return the chord with the highest score or a message if no chord was recognized
        if chord_scores:
            return max(chord_scores, key=chord_scores.get)
        else:
            return None
    
    def mainloop(self):
        while (self.stream.is_active()): # if using button you can set self.stream to 0 (self.stream = 0), otherwise you can use a stop condition
            sleep(0.1)

if __name__ == "__main__":
    def display_chord(chord):
        print(f"Detected chord: {chord}")

    audio = AudioHandler(display_chord)
    audio.start()
    audio.mainloop()
    audio.stop()