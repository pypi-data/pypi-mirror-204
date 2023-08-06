#!/usr/bin/env python

from __future__ import annotations

import fire

from .cli.cli import CLI
from .client import Client
from .encoder import Encoder


def main() -> None:
    fire.Fire(CLI, name="anomalo")


if __name__ == "__main__":
    main()
