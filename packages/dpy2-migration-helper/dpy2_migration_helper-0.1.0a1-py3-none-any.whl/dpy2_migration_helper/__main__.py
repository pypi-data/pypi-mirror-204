import argparse
from pathlib import Path

from .dataclasses import CogModule, PythonFile, Result
from .visitor import visit


def check_file(result: Result, file: PythonFile) -> None:
    result.current_file = file
    visit(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src",
        nargs="+",
        type=Path,
        help="Path to cog's module file or package directory.",
    )
    ns = parser.parse_args()

    result = Result()
    for module_path in ns.src:
        module = CogModule(is_pkg=module_path.is_dir(), base_path=module_path)
        if module.is_pkg:
            for path in module.base_path.rglob("*.py"):
                check_file(result, PythonFile(top_package=module, path=path))
        else:
            check_file(result, PythonFile(top_package=module, path=module.base_path))

    result.print()

    return 0


def entrypoint() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
