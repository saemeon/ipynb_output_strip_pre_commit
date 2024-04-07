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


def smudge(filename):
    logger.warning(f"in ipynb filter smudge for {filename}")
    nb_incoming = json.loads(sys.stdin.read())
    logger.warning(nb_incoming)
    for cell_incoming in nb_incoming["cells"]:
        cell_incoming["outputs"] = [
            {"name": "stdout", "output_type": "stream", "text": ["blablablab\n"]}
        ]
    logger.warning(nb_incoming)
    sys.stdout.write(json.dumps(nb_incoming))


# def smudge(filename):
#     # filename = "test.ipynb"
#     # with open(filename, "r") as file:
#     #     nb_local = json.loads(file.read())
#     nb_incoming = json.loads(sys.stdin.read())

#     # nb_incoming = json.loads(git.Repo().git.show(f":{filename}"))
#     # print(nb_local)
#     print(nb_incoming)
#     # for cell_local, cell_incoming in zip(nb_local["cells"], nb_incoming["cells"]):
#     for cell_incoming in nb_incoming["cells"]:
#         # tbd: check which cells to insert output
#         # if cell_incoming["source"] == cell_local["source"]:
#         #     cell_incoming["outputs"] = cell_local["outputs"]

#         # cell_incoming["outputs"] = cell_local["outputs"]
#         cell_incoming["outputs"] = [
#             {"name": "stdout", "output_type": "stream", "text": ["blablablab\n"]}
#         ]

# # print(nb_local)
# print(nb_incoming)
# sys.stdout.write(json.dumps(nb_incoming))


def clean():
    logger.warning("in ipynb filter clean")
    logger.warning(sys.stdin.read())
    sys.stdout.write(sys.stdin.read())


if __name__ == "__main__":
    print(sys.argv)
    logger.warning(sys.argv)
    if sys.argv[1] == "--smudge":
        filename = sys.argv[2]
        smudge(filename)
    elif sys.argv[1] == "--clean":
        filename = sys.argv[2]
        clean()
    else:
        usage()
    # except Exception as e:
    #     print(e)
    #     usage()
