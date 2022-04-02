from pathlib import Path
from typing import List

from pytablewriter import MarkdownTableWriter as Table
from pytablewriter.style import Style
from typer import Argument, Typer

app = Typer()


@app.command()
def command(package: Path = Argument(..., exists=True)) -> None:
    files: List[Path] = []

    for file in package.glob("**/*.py"):
        if file.is_dir():
            continue

        files.append(str(file.relative_to(package)))

    files.sort()

    table = Table(
        table_name=f"Fully Type Annotation - {package.name.capitalize()}",
        headers=("Status", "Filename", "PR"),
        value_matrix=[(":x:", file.replace("_", "\\_"), "") for file in files],
        margin=2,
        column_styles=[
            Style(align="center"),
            Style(align="left", font_weight="bold"),
            Style(align="left"),
        ],
    )

    table.write_table()
    print()
    print(
        ":white_check_mark: (`:white_check_mark:`): Merged",
        ":x: (`:x:`)): Need work",
        ":speech_balloon: (`:speech_balloon:`): In review",
        sep="\n",
    )
