# POCKETROCKIT - A rocket in your pocket that rocks!

[Project page](https://projects.om-office.de/frans/pocketrockit.git)

Write a music track and play it while you write it. As you might know it from Sonic Pi, but in
Python (`sonic.py` was not available on PyPi, though).


## Usage

Workflow is not quite mature yet, so here is the short version for now.

Create and enter a development folder and provide required SoundFont files (configurable later,
hard-coded for now)

```sh
mkdir mytracks
cd mytracks
cp /usr/share/soundfonts/FluidR3_GM.sf2 .
```

Download [Roland JV-1080 Drums](https://musical-artifacts.com/artifacts/2744) (`JV_1080_Drums.sf2`)
to that directory.

Create a file `myfirsttrack.py` with the following content:

```python
#!/usr/bin/env python3

from pocketrockit.decorated import Env, midiseq, player, track

@track
def po20(env: Env):
    """A Pocket Operator PO-20 Arcade (well, not yet)"""

    env.bpm = 60
    key = "C3"

    @player
    def melody():
        yield from midiseq(
            " t6  t5  t6  t3 "
            " t1  t3  t0  .  "
            " .   .   .   .  "
            " .   .   .   .  ",
            key=key,
            channel=25,
        )

    @player
    def drums1():
        yield from midiseq(
            "x .  x  . "
            "x .  .  . "
            "x .  x  . "
            "x .  x  x ",
            channel=128,
            note=33,
        )
```

Now - keeping the editor open for later use - execute this file. You can either make it executable
and run it directly or you run `python3` instead:

```sh
chmod +x myfirsttrack.py
./myfirsttrack.py

# or

python3 myfirsttrack.py
```


## Installation

```sh
[<PYTHON> -m] pip[3] install [-U] pocketrockit
```


## Development & Contribution

```sh
pip3 install -U poetry pre-commit
git clone --recurse-submodules https://projects.om-office.de/frans/pocketrockit.git
cd pocketrockit
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.10.4/bin/python3
poetry install
```


## Stuff to read / Sources

### SoundFonts

* https://musescore.org/en/handbook/3/soundfonts-and-sfz-files
* https://www.producersbuzz.com/category/downloads/download-free-soundfonts-sf2/
* https://archive.org/details/500-soundfonts-full-gm-sets
* https://ia802502.us.archive.org/view_archive.php?archive=/27/items/500-soundfonts-full-gm-sets/500_Soundfonts_Full_GM_Sets.zip
* https://musical-artifacts.com/artifacts?formats=sf2&tags=soundfont


### Music theory

* https://pianoscales.org/major.html
* https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
