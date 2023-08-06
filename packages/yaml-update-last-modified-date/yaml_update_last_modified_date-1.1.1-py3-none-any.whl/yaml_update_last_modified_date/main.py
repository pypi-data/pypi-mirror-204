"""Set the last modified date in YAML front matter of edited markdown files.

Credit to Michael Rose (@mmistakes) for the basis of this script.
https://mademistakes.com/notes/adding-last-modified-timestamps-with-git/

Credit to ChatGPT for help converting it to python.
"""

import datetime as dt
import os
import tempfile

import git
import typer
from rich import print
from rich.progress import track


app = typer.Typer()


@app.command()
def main(
    *,
    field: str = 'last_modified_at',
    fmt: str = '%Y-%m-%d %H:%M:%S',
) -> None:
    """Set the last modified date in YAML front matter of edited markdown files."""
    # Use Git to get a list of modified Markdown files.
    repo = git.Repo(search_parent_directories=True)
    diff_index = repo.index.diff('HEAD')
    modified_files = [diff.a_path for diff in diff_index if diff.change_type != 'D']
    modified_files = [file for file in modified_files if file.endswith('.md')]

    # Update the last_modified_at field in each file.
    tmpfile = tempfile.mktemp()
    last_modified_at = dt.datetime.now(dt.timezone.utc).strftime(fmt)
    for file in modified_files:
        with open(file, 'r') as f:
            lines = f.readlines()
        with open(tmpfile, 'w') as f:
            for line in lines:
                if line.startswith(f'{field}:'):
                    f.write(f'{field}: {last_modified_at}\n')
                else:
                    f.write(line)
        os.replace(tmpfile, file)
        repo.git.add(file)
        typer.echo(f'Updated {field} for {file}.')


# FIXME: What to call this file?

# FIXME: Apply copier-python-project! - .pre-commit hooks

# FIXME: Convert to python script installable via pip(x) install using - update instructions
# FIXME: Ask ChatGPT?
# https://github.com/psf/black
# https://github.com/PyCQA/pydocstyle
# https://github.com/pylint-dev/pylint
# https://github.com/PyCQA/prospector
# https://github.com/PyCQA/isort
# https://github.com/PyCQA/docformatter
# https://github.com/PyCQA/autoflake

# use Github to test this with different versions of python.

# https://typer.tiangolo.com/tutorial/testing/#test-the-app

# FIXME: poetry publish

# FIXME: How will this change affect homebrew tap? - update instructions
# https://github.com/simonw/homebrew-datasette/blob/main/Formula/datasette.rb

# FIXME: Submit to pre-commit.com.

# FIXME: auto send to pypi.org upon release?

# FIXME: auto send to homebrew upon release?


if __name__ == "__main__":
    app()
