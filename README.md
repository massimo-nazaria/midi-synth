
# MIDI-SYNTH -- A MINIMALIST MIDI SYNTHESIZER

Can either play the sound through the speakers or store it to a Wave file.

More info: [A Minimalist MIDI Synth with Sine Waves](https://massimo-nazaria.github.io/midi-synth.html).

## Sample Usage

```sh
cd midi-synth/

python3 synth.py elise.mid
```

_Output_:

<audio controls>
	<source src="demo.ogg" type="audio/ogg">
	<a href="https://massimo-nazaria.github.io/assets/midi-synth/demo.ogg">Click here to listen (demo.ogg)</a>
</audio>

## Dependencies

Needed software packages:

* [Python 3](https://www.python.org/)
* [NumPy](https://numpy.org/)
* [MIDO](https://mido.readthedocs.io)
* [PyAudio (>=0.2.13)](https://people.csail.mit.edu/hubert/pyaudio/)
* [SciPy](https://scipy.org/)

_Use the following commands on Ubuntu Linux 22.04 or other recent Debian-based distros:_

```sh
$ sudo apt install python3
$ sudo apt install python3-numpy
$ sudo apt install python3-mido
$ sudo apt install python3-pip	
$ sudo apt install portaudio19-dev
$ python3 -m pip install pyaudio
$ sudo apt install python3-scipy
```
