# No Name Yet

Uses `strace` to trace a program call and displays what's going on in a human
friendly manner.

[Project page](https://projects.om-office.de/frans/einefreude)

## Usage

Run a song-file (which has to implement `main()` or run the engine providing the song file:

```
./mysong.py

./enging_dev mysong.py
```


### ToDo for MLP (minimal lovable product)


### Other ideas

## Installation

```
git clone https://projects.om-office.de/frans/einefreude
```

## Development & Contribution

```
pip3 install -U poetry pre-commit
git clone --recurse-submodules https://projects.om-office.de/frans/einefreude.git
cd einefreude
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use /home/frafue/.pyenv/versions/3.10.4/bin/python3
poetry install
```
