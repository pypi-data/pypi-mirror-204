import json

import typer

from launch.gen import utils
from launch.session_state import LaunchFlowSession

app = typer.Typer()


@app.command()
def inspect(buildflow_file_path: str):
    result = utils.inspect(buildflow_file_path)
    state = LaunchFlowSession.load()
    state.sink = result.sink
    state.source = result.source
    typer.echo(
        json.dumps({
            'source': result.source,
            'sink': result.sink,
        }, indent=4))
    state.write()


@app.command()
def schemas(buildflow_file_path: str):
    raise NotImplementedError


@app.command()
def tests(buildflow_file_path: str):
    raise NotImplementedError


if __name__ == "__main__":
    app()
