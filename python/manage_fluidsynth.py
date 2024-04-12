import mido
import fluidsynth

# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start(driver='alsa')

# Load a SoundFont (replace 'soundfont.sf2' with your actual SoundFont file)
sfid = fs.sfload('/usr/share/sounds/sf2/default-GM.sf2')
fs.program_select(0, sfid, 0, 0)  # Initial program select

# Function to handle MIDI messages
def handle_message(msg):
    if msg.type == 'control_change':
        if msg.control == 70: # K1 = instrument
            new_program = msg.value  
            fs.program_change(0, new_program)
        if msg.control == 71: # K2 = volume 
            fs.cc(0, 7, msg.value) 
        if msg.control == 72: # K3 = vibrato
            fs.cc(0, 1, msg.value)
        if msg.control == 73: # K4 = expression 
            fs.cc(0, 11, msg.value) 
        if msg.control == 74: # K5 = sustain 
            fs.cc(0, 64, msg.value)
        if msg.control == 75: # K6 = reverb
            fs.cc(0, 91, msg.value)
        if msg.control == 76: # K7 = chorus
            fs.cc(0, 93, msg.value)

# Open MIDI input port
with mido.open_input() as inport:
    for msg in inport:
        handle_message(msg)
