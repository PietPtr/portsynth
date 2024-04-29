use std::cmp::min;

use fluidsynth::{settings::Settings, synth::Synth};
use log::{error, info};
use midir::{Ignore, MidiInput};
use wmidi::{Channel, ControlFunction, MidiMessage, U7};

struct PortSynth {
    synth: Synth,
    min_velocity: U7,
}

impl PortSynth {
    fn new() -> Self {
        let mut settings = Settings::new();
        settings.setstr("audio.driver", "alsa");
        let synth = Synth::new(&mut settings);
        let sfid = synth
            .sfload("/usr/share/sounds/sf2/default-GM.sf2", 1)
            .unwrap();
        synth.program_select(0, sfid, 0, 0);
        synth.program_select(9, sfid, 128, 0);
        PortSynth {
            synth,
            min_velocity: U7::MIN,
        }
    }
    fn handle_message(&self, bytes: &[u8]) {
        let message = MidiMessage::try_from(bytes);
        match message {
            Err(err) => error!("Failed to parse MIDI message: {}", err),
            Ok(message) => match message {
                MidiMessage::NoteOn(channel, note, velocity) => {
                    if channel == Channel::Ch1 {
                        // let adjusted_velocity = U7::try_from(velocity + self.min_velocity;
                        // self.synth.note_on(channel, note, adjusted_velocity);
                        self.synth.noteon(channel.index() as i32, note as i32, 127);
                    }
                }
                MidiMessage::NoteOff(channel, note, _) => {
                    if channel == Channel::Ch1 {
                        self.synth.noteoff(channel.index() as i32, note as i32);
                    }
                }
                MidiMessage::ControlChange(channel, controller, value) => {
                    let value = u8::from(value) as i32;
                    let to_i32 = |cf: ControlFunction| u8::from(cf.0) as i32;
                    if channel == Channel::Ch1 {
                        match controller {
                            ControlFunction::SOUND_CONTROLLER_1 => {
                                self.synth.program_change(channel.index() as i32, value);
                            }
                            ControlFunction::SOUND_CONTROLLER_2 => {
                                self.synth.cc(
                                    channel.index() as i32,
                                    to_i32(ControlFunction::CHANNEL_VOLUME),
                                    value,
                                );
                            }
                            ControlFunction::SOUND_CONTROLLER_3 => {}
                            ControlFunction::SOUND_CONTROLLER_4 => {}
                            ControlFunction::SOUND_CONTROLLER_5 => {}
                            ControlFunction::SOUND_CONTROLLER_6 => {}
                            ControlFunction::SOUND_CONTROLLER_7 => {}
                            ControlFunction::SOUND_CONTROLLER_8 => {}
                        }
                        // match controller {
                        //     70 => self.synth.program_change(0, value),
                        //     71 => self.synth.cc(0, 7, value),
                        //     72 => self.synth.cc(0, 11, value),
                        //     73 => min_velocity = value,
                        //     74 => self.synth.cc(0, 91, value),
                        //     75 => self.synth.cc(0, 93, value),
                        //     _ => {}
                        // }
                    }
                }
                _ => {}
            },
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut synth = PortSynth::new();
    let midi_in = MidiInput::new("Midi Input")?;
    midi_in.ignore(Ignore::None);
    let in_port = midi_in
        .ports()
        .into_iter()
        .next()
        .ok_or("No MIDI input port found.")?;

    let _conn_in = midi_in.connect(
        &in_port,
        "midir-read-input",
        move |_, message, _| {
            synth.handle_message(&message);
        },
        (),
    )?;

    info!("Press enter to exit...");
    let mut input = String::new();
    std::io::stdin().read_line(&mut input)?;
    Ok(())
}
