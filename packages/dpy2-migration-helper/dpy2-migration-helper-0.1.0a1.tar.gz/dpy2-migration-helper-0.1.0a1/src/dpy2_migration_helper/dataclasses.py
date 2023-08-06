import ast
import dataclasses
import socket
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclasses.dataclass()
class CogModule:
    is_pkg: bool
    base_path: Path


@dataclasses.dataclass()
class PythonFile:
    top_package: CogModule
    path: Path


class Result:
    current_file: PythonFile

    def __init__(self) -> None:
        self.messages: Dict[str, List[Tuple[Path, int, int]]] = {}

    def print(self) -> None:
        for error_msg, locations in self.messages.items():
            print(error_msg)
            for path, line, column in locations:
                uri = path.resolve().as_uri()
                if uri.startswith("file:///"):
                    uri = uri[len("file://") :]
                    uri = f"file://{socket.gethostname()}{uri}"
                print(
                    f"  - \033]8;;{uri}#{line}:{column}"
                    f"\033\\{path}:{line}:{column}\033]8;;\033\\"
                )

    def add(self, node: ast.AST, error: str, *, file: Optional[Path] = None) -> None:
        file = file or self.current_file.path
        self.messages.setdefault(error, []).append((file, node.lineno, node.col_offset))
