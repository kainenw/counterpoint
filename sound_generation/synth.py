from synthesizer import Player, Synthesizer, Waveform

from TET import getFreq

player = Player()
player.open_stream()

synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)

# You can also specify frequencies to play just intonation

def play2(item):
  print(item)
  freq1 = getFreq(57 + item[0])
  freq2 = getFreq(57 + item[1])
  player.play_wave(synth.generate_chord([freq1, freq2], 0.2))


def playFirstSpecies(line):
  for pair in line:
    freq1 = getFreq(57 + pair[0])
    freq2 = getFreq(57 + pair[1])
    player.play_wave(synth.generate_chord([freq1, freq2], 0.2))