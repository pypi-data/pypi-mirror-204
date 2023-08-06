import json
import logging
import os
import signal
import subprocess
import tempfile
import time
import zipfile
from typing import List, Optional

import requests
import typer

from launch import constants
from launch.auth import cache
from launch.auth import flow as auth_flow
from launch.config import LaunchFlowConfig
from launch.gen import gen
from launch.meta import actions

app = typer.Typer()
app.add_typer(gen.app, name='gen')
app.add_typer(actions.app, name='actions')


@app.command(help='Authenticate with launchflow.')
def auth(server_address: str = constants.SERVER_ADDRESS_OPTION):
    auth_flow.web_server_flow(server_address)

    config = LaunchFlowConfig.load()
    if config.default_organization:
        # Don't try to set the default organization if it is already set.
        return

    creds = cache.get_user_creds(server_address)
    response = requests.get(
        f'{server_address}/organization/list',
        headers={'Authorization': f'Bearer {creds.id_token}'})

    json_content = json.loads(response.content.decode())
    if response.status_code != 200:
        raise ValueError(
            f'Failed to list organizations : {json_content["detail"]}.')

    flow_creators: List[str] = json_content['flow_creators']
    if not flow_creators:
        print('Did not find any organizations you can create flows in. We will'
              ' not set a default organization.')
    elif len(flow_creators) > 1:
        print('Found multiple organizations you can create flows in: '
              f'{flow_creators}. We will not  set a default organization. You '
              'can either pass the organization to your deploy command, like: '
              '`launch deploy main.py --org=myorg`. Or you can set the default'
              ' with: `launch set-default-org myorg`')
    else:
        print('Found one organization you can create flows in: '
              f'{flow_creators[0]}. Setting as the default. You can change'
              ' this by running: `launch set-default-org myorg`')
        config.default_organization = flow_creators[0]
        config.write()


# @app.command(help='Set default organization for actions.')
# def set_default_org(name: str):
#     config = LaunchFlowConfig.load()
#     config.default_organization = name
#     config.write()

MODULE_HELP_TEXT = 'whether or not to run the python entry point as a module. e.g. python -m flow'  # noqa: E501
WORKING_DIR_HELP_TEXT = 'The working directory for your flow. Defaults to your current directory. This can be used if you need to include your working directory files with your executable.'  # noqa: E501
REQUIREMENTS_HELP_TEXT = 'The requirements.txt file containing requirements for your flow.'  # noqa: E501
MAX_RETRIES = 20


def get_job_status():
    response = requests.get('http://localhost:3569/get_job', )
    return response.json()['status']


def zipdir(path, ziph, requirements_path: str):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            full_file_path = os.path.join(root, file)
            if full_file_path == requirements_path:
                # No need to add requirements file we will do this below.
                continue
            ziph.write(
                full_file_path,
                os.path.relpath(full_file_path, os.path.join(path, '.')))


def send_deploy_request(
    server_address: str,
    zip_file: Optional[str],
    entrypoint: str,
    flow_id: str,
    has_requirements: bool,
):
    creds = cache.get_user_creds(server_address)
    if zip_file is not None:
        files = {
            'zip_file': ('working_dir.zip', open(zip_file,
                                                 'rb'), 'application/zip')
        }
    else:
        files = None
    data = {
        'flow_id': flow_id,
        'flow_entry_point': entrypoint,
    }
    if has_requirements:
        data['relative_requirements_file'] = './requirements.txt'
    response = requests.post(
        f'{server_address}/jobs/create',
        headers={'Authorization': f'Bearer {creds.id_token}'},
        files=files,
        data=data)
    if response.status_code != 200:
        json_content = json.loads(response.content.decode())
        raise ValueError(f'Remote run failed: {json_content["detail"]}.')


@app.command(help='Launch your BuildFlow pipeline.')
def run(
    module: bool = typer.Option(False, '-m', help=MODULE_HELP_TEXT),
    entrypoint: str = typer.Argument(
        ..., help='The python file or module for your BuildFlow pipeline.'),
    working_dir: str = typer.Option('', help=WORKING_DIR_HELP_TEXT),
    requirements_file: str = typer.Option('', help=REQUIREMENTS_HELP_TEXT),
    local: bool = typer.Option(default=False,
                               help='Whether or not to run in local mode.'),
    flow_id: Optional[int] = constants.FLOW_OPTION,
    team_id: Optional[int] = constants.TEAM_OPTION,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    if team_id is None:
        # list teams
        # prompt user if there is more than one team or if there are no teams
        pass

    if module:
        entrypoint = f'-m {entrypoint}'

    if working_dir:
        # Expand the full path so users can use relative paths.
        working_dir = os.path.abspath(working_dir)
    if requirements_file:
        requirements_file = os.path.abspath(requirements_file)
    if local:
        cli_working_dir = os.path.abspath(os.path.dirname(__file__))
        try:
            relay_proc = subprocess.Popen(
                [
                    'uvicorn', 'local_relay:app', '--host', 'localhost',
                    '--port', '3569', '--log-level', 'warning'
                ],
                cwd=cli_working_dir,
            )
            command = f'python {entrypoint}'
            tries = 0
            while tries < MAX_RETRIES:
                tries += 1
                try:
                    response = requests.post(
                        'http://localhost:3569/submit_job',
                        data=json.dumps({
                            'entrypoint': command,
                            'working_dir': working_dir,
                            'requirements_file': requirements_file
                        }))
                    if response.status_code != 200:
                        raise ValueError(
                            'failed to launch job. View logs for a more '
                            'detailed error.')
                    break
                except requests.exceptions.ConnectionError as e:
                    if tries >= MAX_RETRIES:
                        raise ValueError(
                            'failed to start launchflow runtime') from e
                    # this can happen if the server isn't up and running. Try
                    # again in one second
                    time.sleep(1)
                    continue
            job_status = None
            print('Flow starting...')
            while (job_status is None
                   or job_status not in ['STOPPED', 'SUCCEEDED', 'FAILED']):
                response = requests.get('http://localhost:3569/get_job_logs', )
                # remove the enclosing quotes.
                logs = response.json()
                if logs:
                    print(logs)
                time.sleep(2)
                # TODO: maybe we should print the logs while it is running
                job_status = get_job_status()
        finally:
            relay_proc.send_signal(signal.SIGINT)
            relay_proc.wait()
    else:
        if not flow_id:
            # TODO: implement ad hoc flow creation on the server side
            raise NotImplementedError('TODO: implement ad hoc Flow creation.')

        if working_dir or requirements_file:
            try:
                _, tf = tempfile.mkstemp(suffix='.zip')
                with zipfile.ZipFile(tf, mode='w') as zf:
                    if working_dir:
                        zipdir(working_dir, zf, requirements_file)
                    if requirements_file:
                        zf.write(requirements_file, 'requirements.txt')
                send_deploy_request(server_address=server_address,
                                    zip_file=tf,
                                    entrypoint=entrypoint,
                                    flow_id=flow_id,
                                    has_requirements=True)
            finally:
                os.remove(tf)
        else:
            send_deploy_request(server_address=server_address,
                                zip_file=None,
                                entrypoint=entrypoint,
                                flow_id=flow_id,
                                has_requirements=False)


def main():
    app()


if __name__ == "__main__":
    main()
