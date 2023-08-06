import cgi
import io
import os
import tempfile
import unittest
from unittest import mock
import zipfile

import requests_mock
from typer.testing import CliRunner

from launch import main


class CliTest(unittest.TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

    @requests_mock.Mocker()
    @mock.patch('subprocess.Popen')
    def test_run_local(self, m: requests_mock.Mocker,
                       popen_mock: mock.MagicMock):
        m.post('http://localhost:3569/submit_job')
        m.get('http://localhost:3569/get_job',
              response_list=[{
                  'json': {
                      'status': 'PENDING'
                  }
              }, {
                  'json': {
                      'status': 'RUNNING'
                  }
              }, {
                  'json': {
                      'status': 'FAILED'
                  }
              }])
        m.get('http://localhost:3569/get_job_logs',
              response_list=[{
                  'json': 'logs'
              }])
        result = self.runner.invoke(main.app, [
            'run', '--local', '-m', '--working-dir=/tmp/',
            '--requirements-file=/tmp/requirements.txt', '"main.py --my-flag"'
        ])
        self.assertEqual(0, result.exit_code, result.stdout)

        # There should be 4 requests.
        # 1 for submiting the job
        # 3 for retrieving the job logs
        # 3 for checking the status of the job until completion
        self.assertEqual(len(m.request_history), 7)
        self.assertEqual(m.request_history[0].path, '/submit_job')
        self.assertEqual(m.request_history[1].path, '/get_job_logs')
        self.assertEqual(m.request_history[2].path, '/get_job')
        self.assertEqual(m.request_history[3].path, '/get_job_logs')
        self.assertEqual(m.request_history[4].path, '/get_job')
        self.assertEqual(m.request_history[5].path, '/get_job_logs')
        self.assertEqual(m.request_history[6].path, '/get_job')

        self.assertEqual(
            m.request_history[0].json(), {
                'entrypoint': 'python -m "main.py --my-flag"',
                'working_dir': '/tmp',
                'requirements_file': '/tmp/requirements.txt'
            })

    @requests_mock.Mocker()
    @mock.patch('launch.auth.cache.get_user_creds')
    def test_run_remote_simple(self, m: requests_mock.Mocker,
                               auth_cache_creds: mock.MagicMock):
        m.post('https://apis.launchflow.com/jobs/create',
               response_list=[{
                   'json': {
                       'id': 1
                   }
               }])
        result = self.runner.invoke(
            main.app, ['run', '--flow-id=1', '"main.py --my-flag"'])

        self.assertEqual(result.exit_code, 0, result.stdout)
        auth_cache_creds.assert_called_once()
        self.assertEqual(len(m.request_history), 1)
        deploy_request = m.request_history[0]
        self.assertEqual(deploy_request.path, '/jobs/create')
        self.assertEqual(
            deploy_request.text,
            'flow_id=1&flow_entry_point=%22main.py+--my-flag%22'  # noqa: E501
        )

    @requests_mock.Mocker()
    @mock.patch('launch.auth.cache.get_user_creds')
    def test_run_remote_with_requirements(self, m: requests_mock.Mocker,
                                          auth_cache_creds: mock.MagicMock):
        with tempfile.NamedTemporaryFile(mode='w') as ntf:
            ntf.write('buildflow')
            ntf.seek(0)
            m.post('https://apis.launchflow.com/jobs/create',
                   response_list=[{
                       'json': {
                           'id': 1
                       }
                   }])
            result = self.runner.invoke(main.app, [
                'run', '--flow-id=1',
                f'--requirements-file={ntf.name}',
                '"main.py --my-flag"'
            ])

            self.assertEqual(result.exit_code, 0, result.exc_info)
            auth_cache_creds.assert_called_once()
            self.assertEqual(len(m.request_history), 1)
            deploy_request = m.request_history[0]
            self.assertEqual(deploy_request.path, '/jobs/create')
            c_type, c_data = cgi.parse_header(
                deploy_request.headers['Content-Type'])
            form_data = cgi.parse_multipart(
                io.BytesIO(deploy_request.body),
                {'boundary': c_data['boundary'].encode()})
            self.assertEqual(form_data['flow_entry_point'],
                             ['"main.py --my-flag"'])
            self.assertEqual(form_data['relative_requirements_file'],
                             ['./requirements.txt'])
            self.assertEqual(form_data['flow_id'],
                             ['1'])
            self.assertEqual(c_type, 'multipart/form-data')
            self.assertIn('zip_file', form_data)
            with zipfile.ZipFile(io.BytesIO(form_data['zip_file'][0])) as zf:
                self.assertEqual(len(zf.filelist), 1)
                req_file = zf.filelist[0]
                self.assertEqual(req_file.filename, 'requirements.txt')
                self.assertEqual(
                    zf.open(req_file).read().decode(), 'buildflow')

    @requests_mock.Mocker()
    @mock.patch('launch.auth.cache.get_user_creds')
    def test_run_remote_with_working_dir(self, m: requests_mock.Mocker,
                                         auth_cache_creds: mock.MagicMock):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, 'main.py'), 'w') as f:
                f.write('import buildflow')
            requirements_file = os.path.join(td, 'requirements.txt')
            with open(os.path.join(td, 'requirements.txt'), 'w') as f:
                f.write('buildflow\npandas')
            subdir = os.path.join(td, 'subdir')
            os.mkdir(subdir)
            with open(os.path.join(subdir, 'lib.py'), 'w') as f:
                f.write('import pandas')
            m.post('https://apis.launchflow.com/jobs/create',
                   response_list=[{
                       'json': {
                           'id': 1
                       }
                   }])
            result = self.runner.invoke(main.app, [
                'run', '--flow-id=1',
                f'--working-dir={td}',
                f'--requirements-file={requirements_file}',
                '"main.py --my-flag"'
            ])

            self.assertEqual(result.exit_code, 0, result.stdout)
            auth_cache_creds.assert_called_once()
            self.assertEqual(len(m.request_history), 1)
            deploy_request = m.request_history[0]
            self.assertEqual(deploy_request.path, '/jobs/create')
            c_type, c_data = cgi.parse_header(
                deploy_request.headers['Content-Type'])
            form_data = cgi.parse_multipart(
                io.BytesIO(deploy_request.body),
                {'boundary': c_data['boundary'].encode()})
            self.assertEqual(form_data['flow_entry_point'],
                             ['"main.py --my-flag"'])
            self.assertEqual(form_data['relative_requirements_file'],
                             ['./requirements.txt'])
            self.assertEqual(form_data['flow_id'],
                             ['1'])
            self.assertEqual(c_type, 'multipart/form-data')
            self.assertIn('zip_file', form_data)
            with zipfile.ZipFile(io.BytesIO(form_data['zip_file'][0])) as zf:
                self.assertEqual(len(zf.filelist), 3)
                zf_list = zf.filelist
                zf_list.sort(key=lambda f: f.filename)
                main_file = zf_list[0]
                self.assertEqual(main_file.filename, 'main.py')
                self.assertEqual(
                    zf.open(main_file).read().decode(), 'import buildflow')
                req_file = zf_list[1]
                self.assertEqual(req_file.filename, 'requirements.txt')
                self.assertEqual(
                    zf.open(req_file).read().decode(), 'buildflow\npandas')
                sub_file = zf_list[2]
                self.assertEqual(sub_file.filename, 'subdir/lib.py')
                self.assertEqual(
                    zf.open(sub_file).read().decode(), 'import pandas')


if __name__ == '__main__':
    unittest.main()
