import sys
import mido
import fluidsynth

# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start(driver='alsa')

# Load a SoundFont (replace 'soundfont.sf2' with your actual SoundFont file)
sfid = fs.sfload('/usr/share/sounds/sf2/default-GM.sf2')
fs.program_select(0, sfid, 0, 0)  
fs.program_select(9, sfid, 128, 0)  

class PortSynth:
    def __init__(self):
        self.min_velocity = 0

    # Function to handle MIDI messages
    def handle_message(self, msg):
        if msg.type == 'control_change' and msg.channel == 0:
            if msg.control == 70: # K1 = instrument
                new_program = msg.value
                fs.program_change(0, new_program)
            elif msg.control == 71: # K2 = volume
                fs.cc(0, 7, msg.value)
            elif msg.control == 72: # K3 = vibrato
                fs.cc(0, 1, msg.value)
            elif msg.control == 73: # K4 = expression
                fs.cc(0, 11, msg.value)
            elif msg.control == 74: # K5 = minimum velocity
                self.min_velocity = msg.value
            elif msg.control == 75: # K6 = reverb
                fs.cc(0, 91, msg.value)
            elif msg.control == 76: # K7 = chorus
                fs.cc(0, 93, msg.value)
        elif msg.type == 'note_on':
            fs.noteon(msg.channel, msg.note, min(msg.velocity + self.min_velocity, 127))
        elif msg.type == 'note_off':
            fs.noteoff(msg.channel, msg.note)

synth = PortSynth()

# Open MIDI input port
with mido.open_input() as inport:
    for msg in inport:
        synth.handle_message(msg)
