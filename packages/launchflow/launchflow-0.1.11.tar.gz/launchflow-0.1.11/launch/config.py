import dataclasses
import json
import os
import requests
from typing import Optional

from launch import constants

_CONFIG_FILE = 'config.json'
_CONFIG_PATH = os.path.join(constants.CONFIG_DIR, _CONFIG_FILE)


@dataclasses.dataclass
class LaunchFlowConfig:
    default_team_id: Optional[int] = None

    def write(self):
        os.makedirs(constants.CONFIG_DIR, exist_ok=True)
        with open(_CONFIG_PATH, 'w') as f:
            json.dump(dataclasses.asdict(self), f)

    @classmethod
    def load(cls,
             server_address: str = '',
             id_token: str = '') -> 'LaunchFlowConfig':
        if os.path.exists(_CONFIG_PATH):
            with open(_CONFIG_PATH, 'r') as f:
                try:
                    json_config = json.load(f)
                    config = cls(**json_config)
                except Exception:
                    # If we fail to load it for whatever reason treat it as an
                    # unset config.
                    config = cls()
        else:
            config = cls()
        # if no team ID is set try to look it up to see if the user only has
        # access to one team. If this is true use that team for all actions.
        if config.default_team_id is None and server_address and id_token:
            response = requests.post(
                f'{server_address}/teams/list',
                headers={'Authorization': f'Bearer {id_token}'})

            if response.status_code != 200:
                raise ValueError(
                    f'failed to list teams. Error code: {response.status_code}'
                )

            json_response = response.json()
            if len(json_response) > 1:
                teams = [(team['display_name'], team['id'])
                         for team in json_response]
                raise ValueError(
                    'You have access to multiple teams. Please run '
                    '`launch actions set-default-team $TEAM_ID` to set the '
                    f'default team.\n\nTeams\n------\n{teams}')
            elif not json_response:
                raise ValueError(
                    'You do not have access to any teams. Please upgrade to '
                    'premium.')
            config.default_team_id = json_response[0]['id']
            config.write()
        return config
