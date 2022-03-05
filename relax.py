#!/usr/bin/env python

r"""
===============

"""

import sys
import os
import json
import numpy as np

import abipy.abilab as abilab
import abipy.flowtk as flowtk


def build_flow(options):
    extra = options.extra
    if extra is None:
        raise RuntimeError("This script requires `-e PSEUDO_PATH`")


    from tools import make_input, MyFlow
    #pseudo_path = os.path.abspath(extra)
    #relax_inp = make_input(pseudo_path, relax=True)

    flow = MyFlow.from_pseudo_path(extra)

    #root = os.path.dirname(pseudo_path)
    #workdir = os.path.join(root, "FCC_RELAX_" + os.path.basename(pseudo_path))

    ## Initialize the flow
    #flow = flowtk.Flow(workdir=workdir)
    #work = flowtk.Work()
    #work.register_relax_task(relax_inp)
    #flow.register_work(work)

    return flow


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    return build_flow(options)


if __name__ == "__main__":
    sys.exit(main())

