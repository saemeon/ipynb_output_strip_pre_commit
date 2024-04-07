"""Pre-commit hook to check if a committed notebook only has empty metadata and output cells.."""

from __future__ import annotations
import tempfile
from functools import reduce
import sys
import git
import json
import logging

logger = logging.getLogger(__name__)


repo = git.Repo()


def usage():
    print(
        """usage:
        1. for git smudge
            python keyfilter.py --smudge
        2. for git clean
            python keyfilter.py --clean
        """
    )


# def smudge():


def smudge(filename):
    # notebook_staged = json.loads(sys.stdin.read())
    # filename = "test.ipynb"
    with open(filename, "r") as file:
        nb_local = json.loads(file.read())
    nb_incoming = json.loads(git.Repo().git.show(f":{filename}"))
    print(nb_local)
    print(nb_incoming)
    for cell_local, cell_incoming in zip(nb_local["cells"], nb_incoming["cells"]):
        # tbd: check which cells to insert output
        # if cell_incoming["source"] == cell_local["source"]:
        #     cell_incoming["outputs"] = cell_local["outputs"]

        cell_incoming["outputs"] = cell_local["outputs"]

    print(nb_local)
    print(nb_incoming)
    sys.stdout.write(json.dumps(nb_incoming))


def clean():
    pass


if __name__ == "__main__":
    print(sys.argv)
    if sys.argv[1] == "--smudge":
        filename = sys.argv[2]
        print(filename)
        smudge(filename)
    elif sys.argv[1] == "--clean":
        clean()
    else:
        usage()
    # except Exception as e:
    #     print(e)
    #     usage()
