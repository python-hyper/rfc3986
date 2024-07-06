"""This script is a shim around `pyright --verifytypes` to determine if the
current typing coverage meets the expected coverage. The previous command by
itself won't suffice, since its expected coverage can't be modified from 100%.
Useful while still adding annotations to the library.
"""

import argparse
import json
import subprocess
from decimal import Decimal

PYRIGHT_CMD = ("pyright", "--verifytypes", "rfc3986", "--outputjson")


def validate_coverage(inp: str) -> Decimal:
    """Ensure the given coverage score is between 0 and 100 (inclusive)."""

    coverage = Decimal(inp)
    if not (0 <= coverage <= 100):
        raise ValueError
    return coverage


def main() -> int:
    """Determine if rfc3986's typing coverage meets our expected coverage."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fail-under",
        default=Decimal("75"),
        type=validate_coverage,
        help="The target typing coverage to not fall below (default: 75).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Whether to hide the full output from `pyright --verifytypes`.",
    )

    args = parser.parse_args()

    expected_coverage: Decimal = args.fail_under / 100
    quiet: bool = args.quiet

    try:
        output = subprocess.check_output(
            PYRIGHT_CMD,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        output = exc.output

    verifytypes_output = json.loads(output)
    raw_score = verifytypes_output["typeCompleteness"]["completenessScore"]
    actual_coverage = Decimal(raw_score)

    if not quiet:
        # Switch back to normal output instead of json, for readability.
        subprocess.run(PYRIGHT_CMD[:-1])

    if actual_coverage >= expected_coverage:
        print(
            f"OK - Required typing coverage of {expected_coverage:.2%} "
            f"reached. Total typing coverage: {actual_coverage:.2%}."
        )
        return 0
    else:
        print(
            f"FAIL - Required typing coverage of {expected_coverage:.2%} not "
            f"reached. Total typing coverage: {actual_coverage:.2%}."
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
