use log::{error, info};
use regex::Regex;
use simple_logger::SimpleLogger;
use std::{
    process::{Command, Stdio},
    thread,
    time::Duration,
};

fn start_fluidsynth() {
    let _ = Command::new("sudo")
        .args([
            "fluidsynth",
            "-v",
            "-a",
            "alsa",
            "-m",
            "alsa_seq",
            "-l",
            "-i",
            "/usr/share/sounds/sf2/FluidR3_GM.sf2",
            "-s",
            "-o",
            "audio.alsa.device=hw:0",
        ])
        .spawn()
        .unwrap_or_else(|_| panic!("Failed to start fluidsynth"));
}

fn connect_midi() {
    let re = Regex::new(r"client (\d+):.*?[^Midi Through|System]").unwrap();
    let mut connected = false;
    loop {
        let output = Command::new("aconnect")
            .arg("-i")
            .output()
            .expect("Couldn't execute aconnect");

        if let Ok(s) = String::from_utf8(output.stdout) {
            for cap in re.captures_iter(&s) {
                let port = &cap[1];
                info!("Found midi device with port {port}");
                match Command::new("aconnect")
                    .arg(format!("{}:0", port))
                    .arg("128:0")
                    .stderr(Stdio::piped())
                    .output()
                {
                    Ok(output) => {
                        if output.status.success() {
                            info!("Successfully connected {} to FluidSynth", port);
                            connected = true;
                        } else {
                            error!("Failed to connect {} to FluidSynth", port);
                        }
                    }
                    Err(e) => error!("Error connecting {} to FluidSynth: {}", port, e),
                }
            }
        }

        thread::sleep(Duration::from_secs_f32(if connected { 10.0 } else { 0.5 }));
    }
}

fn main() {
    SimpleLogger::new().init().unwrap();
    start_fluidsynth();
    connect_midi();
}
