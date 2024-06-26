import sys
import mido
import fluidsynth

fs = fluidsynth.Synth()
fs.start(driver='alsa')

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
            elif msg.control == 72: # K3 = expression
                fs.cc(0, 11, msg.value)
            elif msg.control == 73: # K4 = minimum velocity
                self.min_velocity = msg.value
            elif msg.control == 74: # K5 = reverb
                fs.cc(0, 91, msg.value)
            elif msg.control == 75: # K6 = chorus
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
