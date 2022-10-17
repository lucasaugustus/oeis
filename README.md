# oeis
Code for my contributions to the OEIS.
Many of these files import from the package ``labmath``.  This can be downloaded from <https://pypi.org/project/labmath> and nstalled via pip.

Most files are named according to the A-numbers that they compute.  For example, ``A350953+4+A356865.py`` computes A356953, A350954, and A356865.
As of 2022-10-16, there are two exceptions:
* ``semiprimemods.py`` computes A106125-A106136, A357741, A357781, A356755, A357807, A357808, A357023, A356135, A356357, A356764, and four other sequences that were rejected from the Encyclopedia.
* ``stormer.py`` computes several sequences related to [Størmer's theorem](https://en.wikipedia.org/wiki/St%C3%B8rmer%27s_theorem), namely A002071, A002072, A117581 - 1, A117582, A117583, A145604, A145606, A175607 - 1, A181471, and several sequences not currently listed in the Encyclopedia.
