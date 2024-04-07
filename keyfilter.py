from functools import reduce
import sys
import logging

logger = logging.getLogger()
REPLACE_CONTENT = [("USERNAME", "github"), ("PASSWORD", "123456")]


def usage():
    print(
        """usage:
        1. for git smudge
            python keyfilter.py --smudge
        2. for git clean
            python keyfilter.py --clean
        """
    )


def smudge():
    logger.warning("smudge in")
    for line in sys.stdin:
        """
        replace keyword list in line
        https://stackoverflow.com/questions/2484156/is-str-replace-replace-ad-nauseam-a-standard-idiom-in-python
        """
        logger.warning(line)
        line = reduce(lambda s, r: s.replace(*r), REPLACE_CONTENT, line)
        logger.warning(line)
        sys.stdout.write(line)


def clean():
    logger.warning("clan in")
    for line in sys.stdin:
        line = reduce(lambda s, r: s.replace(*r[::-1]), REPLACE_CONTENT, line)
        sys.stdout.write(line)


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--smudge":
            smudge()
        elif sys.argv[1] == "--clean":
            clean()
        else:
            usage()
    except Exception as e:
        print(e)
        usage()
