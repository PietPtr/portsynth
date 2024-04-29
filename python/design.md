# Web server

To control various modes of the portsynth and to see current settings.

## Main page

### Current settings quick view

Shows the eight knobs and their current configuration:

* Program: translates to the instrument name
* Volume / expression / minimum velocity / reverb / chorus: naked value
* Tempo: scaled tempo from 45 to 180.

### Mode selector

Selects which mode the portsynth will be configured as. Each mode should have a start and stop function which configures processes as the mode requires.

1. Instrument Mode: simply play whatever midi notes the portsynth receives without anything else.

2. Drums Mode: select from some builtin drum midi tracks. Once enabled the drum track will be played on repeat at the currently set master tempo.

3. Practice Mode: show a selection of tracks, select a loop start and end point in bars / beats. Portsynth should start playing that on repeat, optionally with a metronome, and play whatever midi notes it gets.

4. Looper Mode: looping-pedal like functionality.