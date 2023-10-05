#!/usr/bin/env python3
"""returns a multiplier function"""

import typing


def make_multiplier(multiplier: float) -> typing.Callable[[float], float]:
