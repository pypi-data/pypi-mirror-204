from pathlib import Path

from typer import echo
from typer import Exit
from typer import getchar

from visual_novel_toolkit.speller.mistakes import load_mistakes
from visual_novel_toolkit.speller.words import FileWords


def review_mistakes() -> None:
    for mistake in load_mistakes():
        echo("")
        echo(mistake)
        echo("")
        echo("[I] Insert   [S] Skip   [Q] Quit")
        match getchar():
            case "q":
                raise Exit(code=0)
            case "s":
                continue
            case "i":
                file_words = FileWords(Path("personal.json"))
                dictionary = file_words.loads()
                dictionary.append(mistake)
                dictionary.sort()
                file_words.dumps(dictionary)
