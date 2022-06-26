import sys
from pathlib import Path
from typing import Iterator, Iterable, Sequence

import typer

from df_gettext_toolkit.common import TranslationItem
from df_gettext_toolkit.parse_po import save_pot


def extract_translatables(files: Iterable[Path]) -> Iterator[TranslationItem]:
    for file_path in files:
        if file_path.is_file():
            print("File:", file_path.name, file=sys.stderr)
            with open(file_path) as file:
                for i, line in enumerate(file, 1):
                    text = line.rstrip("\n")
                    if text:
                        yield TranslationItem(text=text, source_file=file_path.name, line_number=i)


def create_pot_file(pot_file: typer.FileTextWrite, files: Sequence[Path]):
    save_pot(
        pot_file,
        extract_translatables(files),
    )


def main(
    path: Path,
    pot_file: typer.FileTextWrite = typer.Option(..., encoding="utf-8"),
):
    files = (file for file in path.glob("*.txt") if file.is_file())
    create_pot_file(pot_file, sorted(files))


if __name__ == "__main__":
    typer.run(main)
