# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocketrockit']

package_data = \
{'': ['*']}

install_requires = \
['asyncinotify>=4.0.1,<5.0.0',
 'pyfluidsynth>=1.3.1,<2.0.0',
 'pygame>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['pocketrockit = pocketrockit.cli:main',
                     'pri = pocketrockit.cli:main']}

setup_kwargs = {
    'name': 'pocketrockit',
    'version': '0.0.6',
    'description': 'pocketrockit',
    'long_description': '# POCKETROCKIT - A rocket in your pocket that rocks!\n\n[Project page](https://projects.om-office.de/frans/pocketrockit.git)\n\nWrite a music track and play it while you write it. As you might know it from Sonic Pi, but in\nPython (`sonic.py` was not available on PyPi, though).\n\n\n## Usage\n\nWorkflow is not quite mature yet, so here is the short version for now.\n\nCreate and enter a development folder and provide required SoundFont files (configurable later,\nhard-coded for now)\n\n```sh\nmkdir mytracks\ncd mytracks\ncp /usr/share/soundfonts/FluidR3_GM.sf2 .\n```\n\nDownload [Roland JV-1080 Drums](https://musical-artifacts.com/artifacts/2744) (`JV_1080_Drums.sf2`)\nto that directory.\n\nCreate a file `myfirsttrack.py` with the following content:\n\n```python\n#!/usr/bin/env python3\n\nfrom pocketrockit.decorated import Env, midiseq, player, track\n\n@track\ndef po20(env: Env):\n    """A Pocket Operator PO-20 Arcade (well, not yet)"""\n\n    env.bpm = 60\n    key = "C3"\n\n    @player\n    def melody():\n        yield from midiseq(\n            " t6  t5  t6  t3 "\n            " t1  t3  t0  .  "\n            " .   .   .   .  "\n            " .   .   .   .  ",\n            key=key,\n            channel=25,\n        )\n\n    @player\n    def drums1():\n        yield from midiseq(\n            "x .  x  . "\n            "x .  .  . "\n            "x .  x  . "\n            "x .  x  x ",\n            channel=128,\n            note=33,\n        )\n```\n\nNow - keeping the editor open for later use - execute this file. You can either make it executable\nand run it directly or you run `python3` instead:\n\n```sh\nchmod +x myfirsttrack.py\n./myfirsttrack.py\n\n# or\n\npython3 myfirsttrack.py\n```\n\n\n## Installation\n\n```sh\n[<PYTHON> -m] pip[3] install [-U] pocketrockit\n```\n\n\n## Development & Contribution\n\n```sh\npip3 install -U poetry pre-commit\ngit clone --recurse-submodules https://projects.om-office.de/frans/pocketrockit.git\ncd pocketrockit\npre-commit install\n# if you need a specific version of Python inside your dev environment\npoetry env use ~/.pyenv/versions/3.10.4/bin/python3\npoetry install\n```\n\n\n## Stuff to read / Sources\n\n### SoundFonts\n\n* https://musescore.org/en/handbook/3/soundfonts-and-sfz-files\n* https://www.producersbuzz.com/category/downloads/download-free-soundfonts-sf2/\n* https://archive.org/details/500-soundfonts-full-gm-sets\n* https://ia802502.us.archive.org/view_archive.php?archive=/27/items/500-soundfonts-full-gm-sets/500_Soundfonts_Full_GM_Sets.zip\n* https://musical-artifacts.com/artifacts?formats=sf2&tags=soundfont\n\n\n### Music theory\n\n* https://pianoscales.org/major.html\n* https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies\n',
    'author': 'Frans Fürst',
    'author_email': 'frans.fuerst+gitlab@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://projects.om-office.de/frans/pocketrockit.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
