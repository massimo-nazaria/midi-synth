#!/usr/bin/python3
# MIDI-SYNTH -- minimalist MIDI software synthesizer
# More info: https://massimo-nazaria.github.io/midi-synth.html

import os
import sys
import mido
import pyaudio
import argparse
import numpy as np
from scipy.io import wavfile

# standard number of samples per second for audio
sample_rate = 44100

parser = argparse.ArgumentParser(description="minimalist MIDI software synthesizer")
# clearly a midi filename must be given as argument
parser.add_argument("midi", help="input MIDI file", type=str)
# if output file given it stores the final waveform in the given file
parser.add_argument("-o", "--output", help="output Wave file", type=str)
args = parser.parse_args()

# input midi filename
midi_name = args.midi

# provided input file does not exist, print error and terminate
if not os.path.exists(midi_name):
    sys.stderr.write("provided input file", midi_name, "does not exist.\n")
    sys.exit(-1)

# provided output file already exists, print error and terminate
if args.output and os.path.exists(args.output):
    sys.stderr.write("provided output Wave file", args.output, "already exists.\n")
    sys.exit(-1)

# temporary hash table with: note -> start-time (in secs)
note_start = {}
# temporary hash table with: note -> velocity (i.e. loudness in range 0-127)
note_velocity = {}
# sequence with played notes and info: [note, start-time, end-time, velocity]
note_start_end_vel = []

# init seconds of the midi tune
secs = 0
# iterate over midi messages
for msg in mido.MidiFile(midi_name):
    # we are only interested in note on/off messagges
    if not msg.is_meta and msg.type in ('note_on', 'note_off'):
        # increment tune seconds (msg time is relative to previous msg)
        secs += msg.time
        # midi note number (integer)
        note = msg.note
        # attention: if velocity == 0 then message is note_off
        if msg.type == 'note_on' and msg.velocity > 0:
            # save note start-time for later
            note_start[note] = secs
            # save note velocity for later
            note_velocity[note] = msg.velocity
        # handle note_off message
        else:
            # discard note_off events having no previous note_on
            if note in note_start:
                # get current note start (from previously seen note on msg)
                start = note_start.pop(note)
                # set current note end-time
                end = secs
                # set current note velocity (from previous note on msg)
                velocity = note_velocity.pop(note)
                # store collected data about the played note
                note_start_end_vel.append([note, start, end, velocity])

# the last assignment to secs should be the total nuumber of seconds
total_secs = secs
# integer of the total number of samples
total_samples = int(total_secs*sample_rate)

# array with time steps (from 0 to total_secs) of length total_samples
t = np.linspace(0, total_secs, total_samples, endpoint=False)
# waveform array initialized with zeros of same length as time array t
w = np.zeros(total_samples)

# for each [note, start, end, vel] in the collected list
for note, start, end, velocity in note_start_end_vel:
    # select range [s, e) of time steps the note must be played in
    s = int(start*sample_rate)
    e = int(end*sample_rate)
    # normalize velocity range [0,127] to amplitude range [0,1]
    amplitude = velocity/127.0
    # compute note frequency w.r.t. A4 (440 Hz), notice A4 note number is 69
    frequency = 440 * 2**((note-69)/12)
    # add to the waveform the sine wave of the played note
    w[s:e] += amplitude*np.sin(2 * np.pi * frequency * t[s:e])

# if output wave file name is provided then write output and exit
if args.output:
    wave_file = args.output
    # write the waveform in wave file
    wavfile.write(wave_file, sample_rate, w)
# play midi through the speakers (no output wave file provided)
else:
    # convert the waveform to the format used by pyaudio
    w_out = w.astype(np.float32).tobytes()

    # initialize an audio session and play the waveform through the speakers
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)
    stream.write(w_out)
    # stop and terminate the audio session
    stream.stop_stream()
    stream.close()
    p.terminate()

sys.exit(0)
