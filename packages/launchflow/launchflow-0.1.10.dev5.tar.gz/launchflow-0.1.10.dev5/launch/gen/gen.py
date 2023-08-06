import json

import typer

from launch.gen import utils
import os

app = typer.Typer()

_SESSION_STATE_FILE = os.path.join(os.path.expanduser('~'), '.config',
                                   'launchflow', 'session_state.json')


@app.command()
def inspect(buildflow_file_path: str):
    result = utils.inspect(buildflow_file_path)
    typer.echo(
        json.dumps({
            'source': result.source,
            'sink': result.sink,
        }, indent=4))
    with open(_SESSION_STATE_FILE, 'w') as f:
        json.dump({
            'source': result.source,
            'sink': result.sink,
        },
                  f,
                  indent=4)


@app.command()
def schemas(buildflow_file_path: str):
    raise NotImplementedError


@app.command()
def tests(buildflow_file_path: str):
    raise NotImplementedError


if __name__ == "__main__":
    app()
