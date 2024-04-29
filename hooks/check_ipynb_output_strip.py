#!/usr/bin/env python
"""Pre-commit hook to check if a committed notebook only has empty metadata and output cells."""

from __future__ import annotations

import argparse
import json
import logging
from typing import Sequence

import git

logger = logging.getLogger(__name__)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    args = parser.parse_args(argv)
    retval = 0
    for filename in args.filenames:
        try:
            notebook = json.loads(git.Repo().git.show(f":{filename}"))
            for cell in notebook["cells"]:
                try:
                    if cell["metadata"] != {}:
                        retval += 1
                        logger.warning(
                            f"found cell with nonempty metadata in {filename}."
                        )
                    if cell["outputs"] != []:
                        retval += 1
                        logger.warning(
                            f"found cell with nonempty output in {filename}."
                        )
                except KeyError:
                    pass

        except ValueError as exc:
            logger.exception(f"{filename}: Failed to json decode ({exc})")
            retval = 1
    return retval


if __name__ == "__main__":
    exit(main())
