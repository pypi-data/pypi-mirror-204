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
    print("hallo")
    return 0


if __name__ == "__main__":
    main()
