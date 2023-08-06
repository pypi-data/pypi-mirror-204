from launch import constants
from launch.auth import cache
import requests
from websocket import create_connection

import typer

app = typer.Typer()


@app.command()
def upgrade(server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    response = requests.get(
        f'{server_address}/billing/checkout',
        headers={'Authorization': f'Bearer {creds.id_token}'})
    response_json = response.json()
    return f'Sign up for a premium account at {response_json["url"]}'


@app.command()
def stream_job_info(job_id: int,
                    server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    ws = create_connection(
        f'{server_address}/jobs/info?job_id={job_id}',
        header={'Authorization': f'Bearer {creds.id_token}'})
    while True:
        print(ws.recv())


if __name__ == "__main__":
    app()
