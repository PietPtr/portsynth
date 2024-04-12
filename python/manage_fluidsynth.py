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
    if msg.type == 'control_change' and msg.control == 70:
        # Change instrument based on the value received from CC #070
        new_program = msg.value  # Assuming CC #070 directly maps to the program number
        fs.program_change(0, new_program)

# Open MIDI input port
with mido.open_input() as inport:
    for msg in inport:
        handle_message(msg)
