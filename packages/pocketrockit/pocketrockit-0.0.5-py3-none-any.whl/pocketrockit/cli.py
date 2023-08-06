#!/usr/bin/env python3

"""POCKETROCKIT
"""

from argparse import ArgumentParser
from argparse import Namespace as Args
from pathlib import Path


def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")

    parser.add_argument("path", type=Path)

    return parser.parse_args()


def main() -> int:
    """Entry point for everything else"""
    print(
        """
    This executable does not do anything yet. Later in time it can be used to run one or multiple
    pocketrockit tracks simultaneously and to configure run time behavior.
    
    For now, please follow the steps described on https://projects.om-office.de/frans/pocketrockit

    In short:
    * create a working folder and provide FluidR3_GM.sf2 and JV_1080_Drums.sf2
    * create an executable track script, e.g. mytrack.py
    * directly run this track script
    """
    )
    return 0


if __name__ == "__main__":
    main()
