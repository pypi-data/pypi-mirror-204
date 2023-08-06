import dataclasses
import signal
from typing import Dict
import unittest
from unittest import mock

from fastapi.testclient import TestClient
import requests_mock

from launch.local_relay import JobSubmission
from launch.local_relay import app


@dataclasses.dataclass
class FakeDriveInfo:
    pid: str = '123'


@dataclasses.dataclass
class FakeJob:
    status: str
    metadata: Dict = dataclasses.field(default_factory=dict)
    driver_info: FakeDriveInfo = FakeDriveInfo()


class LocalRelayServerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(app)

    @mock.patch('launch.local_relay.JobSubmissionClient')
    def test_no_job(self, job_sub_mock):
        response = self.client.get('/get_job')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'],
                         'no job has been started on the server yet.')

        response = self.client.get('/stop_job')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'],
                         'no job has been started on the server yet.')

        response = self.client.get('/drain_job')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'],
                         'no job has been started on the server yet.')

    @requests_mock.Mocker()
    @mock.patch('launch.local_relay.JobSubmissionClient')
    @mock.patch('os.kill')
    def test_run_job(
        self,
        m: requests_mock.Mocker,
        os_kill_mock: mock.MagicMock,
        job_sub_mock: mock.MagicMock,
    ):
        # query for throughput
        m.get(
            'http://localhost:9090/api/v1/query?query=rate%28ray_num_events_processed%5B1m%5D%29',  # noqa: E501
            response_list=[{
                'json': {}
            }],
        )
        # query for num replicas
        m.get(
            'http://localhost:9090/api/v1/query?query=ray_num_replicas',
            response_list=[{
                'json': {}
            }],
        )
        # query for processor latency
        m.get(
            'http://localhost:9090/api/v1/query?query=avg_over_time%28ray_process_time%5B1m%5D%29',  # noqa: E501
            response_list=[{
                'json': {}
            }],
        )

        job_id = 'new_job_id'
        submit_mock = job_sub_mock.return_value.submit_job
        submit_mock.return_value = job_id
        get_mock = job_sub_mock.return_value.get_job_info
        get_mock.return_value = FakeJob(status='RUNNING')
        stop_mock = job_sub_mock.return_value.stop_job

        request = JobSubmission(entrypoint='main.py',
                                working_dir='/tmp',
                                requirements_file='/tmp/requirements.txt')
        submit_response = self.client.post('/submit_job', data=request.json())

        # Validate that the job was started.
        self.assertEqual(submit_response.status_code, 200,
                         submit_response.json())
        submit_mock.assert_called_once_with(
            entrypoint='main.py',
            runtime_env={
                'working_dir': '/tmp',
                'pip': '/tmp/requirements.txt'
            },
        )

        # Validate get returns the expected job.
        get_response = self.client.get('/get_job')
        self.assertEqual(get_response.status_code, 200, get_response.json())

        get_mock.assert_called_once_with(job_id)

        get_json = get_response.json()
        self.assertEqual(get_json['status'], 'RUNNING')
        self.assertIn('throughput', get_json['metadata'])
        self.assertIn('num_replicas', get_json['metadata'])
        self.assertIn('process_time', get_json['metadata'])

        self.assertEqual(len(m.request_history), 3)
        throughput_request = m.request_history[0]
        self.assertEqual(throughput_request.path, '/api/v1/query')
        self.assertEqual(throughput_request.query,
                         'query=rate%28ray_num_events_processed%5b1m%5d%29')
        num_replicas_request = m.request_history[1]
        self.assertEqual(num_replicas_request.path, '/api/v1/query')
        self.assertEqual(num_replicas_request.query, 'query=ray_num_replicas')
        processor_latency_request = m.request_history[2]
        self.assertEqual(processor_latency_request.path, '/api/v1/query')
        self.assertEqual(processor_latency_request.query,
                         'query=avg_over_time%28ray_process_time%5b1m%5d%29')

        # Validate we can't start another job until this one is finished.
        request = JobSubmission(entrypoint='main.py',
                                working_dir='/tmp',
                                requirements_file='')
        second_submit_response = self.client.post('/submit_job',
                                                  data=request.json())
        self.assertEqual(second_submit_response.status_code, 400)
        self.assertEqual(
            second_submit_response.json()['detail'],
            'job already running, please cancel job or wait for it to finish.')

        # Now validate we can start a job after the other one is done.
        get_mock = job_sub_mock.return_value.get_job_info
        get_mock.return_value = FakeJob(status='FAILED')
        request = JobSubmission(entrypoint='main.py',
                                working_dir='/tmp',
                                requirements_file='/tmp/requirements.txt')
        second_submit_response = self.client.post('/submit_job',
                                                  data=request.json())
        self.assertEqual(second_submit_response.status_code, 200)

        # Validate stop job
        get_response = self.client.get('/stop_job')
        self.assertEqual(get_response.status_code, 200, get_response.json())
        stop_mock.assert_called_once_with(job_id)

        # Validate drain job
        get_response = self.client.get('/drain_job')
        self.assertEqual(get_response.status_code, 200, get_response.json())
        os_kill_mock.assert_called_once_with(123, signal.SIGTERM)


if __name__ == '__main__':
    unittest.main()
