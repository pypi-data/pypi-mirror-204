import os
import signal
import subprocess
from sys import platform
from dataclasses import dataclass
from pkg_resources import resource_filename
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ray.job_submission import JobSubmissionClient

from launch.prometheus import queries

RAY_CLUSTER_ADDRESS = 'http://127.0.0.1:8265'


@dataclass
class JobInfo:
    job_id: str
    status: str
    metrics: Dict[str, str]


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event("startup")
def startup():
    prom_dir = resource_filename('launch', 'prometheus')
    subprocess.run(('ray start --head --dashboard-host=0.0.0.0 --port=6379 '
                    '--autoscaling-config=~/ray_bootstrap_config.yaml '
                    '--temp-dir=/var/tmp/ray'),
                   shell=True)
    if platform == "linux" or platform == "linux2":
        executable = 'linux/prometheus'
    elif platform == "darwin":
        executable = 'mac/prometheus'
    else:
        raise ValueError(
            f'launch CLI is not supported for platform: {platform}')
    prom_config = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'remote_prom_config.yml')
    subprocess.Popen(
        f'./{executable} --config.file={prom_config}',  # noqa
        cwd=f'{prom_dir}/.',
        shell=True)


@app.get('/get_job')
async def get_job(job_id: str):
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    job_info = client.get_job_info(job_id)
    job_info.metadata['throughput'] = queries.throughput()
    job_info.metadata['num_replicas'] = queries.num_replicas()
    job_info.metadata['process_time'] = queries.processor_latency()
    return job_info


@app.get('/drain_job')
async def drain_job(job_id: str):
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    job_info = client.get_job_info(job_id)
    pid = job_info.driver_info.pid
    os.kill(int(pid), signal.SIGTERM)
    return True
