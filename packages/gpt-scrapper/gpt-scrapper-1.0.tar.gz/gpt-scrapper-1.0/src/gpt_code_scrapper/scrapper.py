import click
from pathlib import Path
import os


def read_contents(path):
    with open(path, 'r') as f:
        return f.read()


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--extensions', '-e', default=['hpp'], help='Extensions to search for', multiple=True)
def scrap_code(path, extensions):
    result = ""
    for extension in extensions:
        for p in Path(path).rglob(f"*.{extension}"):
            if p.is_file():
                result += f"{os.path.join(p.parent.name, p.name)}\n\n"
                result += read_contents(p)
                result += "******\n\n\n"

    output_path = Path("output.txt")
    with output_path.open("w") as f:
        f.write(result)


if __name__ == '__main__':
    scrap_code()
