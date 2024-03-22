"""Pre-commit hook to check if a committed notebook only has empty metadata and output cells.."""

from __future__ import annotations

import argparse
import git
import json
import logging
from typing import Sequence

logger = logging.getLogger(__name__)


repo = git.Repo()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    args = parser.parse_args(argv)
    retval = 0
    for filename in args.filenames:
        try:
            notebook = json.loads(repo.git.show(f":{filename}"))
            for cell in notebook["cells"]:
                try:
                    if cell["metadata"] != {}:
                        retval += 1
                        logger.warning("found cell with nonempty metadata.")
                    if cell["outputs"] != []:
                        retval += 1
                        logger.warning("found cell with nonempty output.")
                except KeyError:
                    pass

        except ValueError as exc:
            print(f"{filename}: Failed to json decode ({exc})")
            retval = 1
    return retval


if __name__ == "__main__":
    raise SystemExit(main())
