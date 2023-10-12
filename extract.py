#!/usr/bin/env python
"""
Script to generate/analyze/plot ONCVPSP pseudopotentials.
"""
from __future__ import annotations

import sys
import os
import argparse
import shutil
import abipy.tools.cli_parsers as cli

from pprint import pformat
from monty.termcolor import cprint
from abipy.flowtk.pseudos import Pseudo
from abipy.ppcodes.ppgen import OncvGenerator
from abipy.ppcodes.oncv_parser import OncvParser
from abipy.ppcodes.oncv_plotter import OncvPlotter, oncv_make_open_notebook, MultiOncvPlotter


def extract(out_path):
    # Parse the output file
    onc_parser = OncvParser(out_path).scan()
    if not onc_parser.run_completed:
        raise RuntimeError("oncvpsp output is not completed. Exiting")

    # Build names of output files.
    psp8_path = out_path.replace(".out", ".psp8")
    #djrepo_path = root + ".djrepo"
    #out_path = root + ".out"

    # Extract psp8 files from the oncvpsp output and write it to file.
    with open(psp8_path, "wt") as fh:
        fh.write(onc_parser.get_psp8_str())

    # Write UPF2 file if available.
    upf_str = onc_parser.get_upf_str()
    if upf_str is not None:
        #print("UPF ok")
        with open(psp8_path.replace(".psp8", ".upf"), "wt") as fh:
            fh.write(upf_str)
    else:
        raise RuntimeError("UPF2 file has not been produced. Use `both` in input file!")


def main():
    top = sys.argv[1]
    for root, dirs, files in os.walk(top):
        for name in files:
            if not name.endswith(".in"): continue
            out_path = os.path.join(root, name.replace(".in", ".out"))
            print(out_path)
            extract(out_path)


if __name__ == "__main__":
    main()
