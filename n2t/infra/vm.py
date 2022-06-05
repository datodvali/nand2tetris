from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from n2t.core import VMTranslator as DefaultVMTranslator


@dataclass
class VmProgram:  # TODO: your work for Projects 7 and 8 starts here
    path: Path
    translator: VMTranslator = field(default_factory=DefaultVMTranslator.create)

    @classmethod
    def load_from(cls, file_or_directory_name: str) -> VmProgram:
        return cls(Path(file_or_directory_name))

    def translate(self) -> None:
        file_path = str(self.path)
        self.translator.translate(file_path)


class VMTranslator(Protocol):  # pragma: no cover
    def translate(self, file_path: str) -> None:
        pass
