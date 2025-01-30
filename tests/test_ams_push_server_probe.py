import unittest
from unittest.mock import patch, MagicMock
import requests
import sys
from io import StringIO
from argo_probe_ams_push_server.check import main

class TestNagiosCheck(unittest.TestCase):

    @patch('requests.get')
    @patch('sys.exit')
    def test_success_response(self, mock_exit, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "push_servers": [{"status": "SERVING"}]
        }
        mock_get.return_value = mock_response

        test_args = ["script_name", "-H", "api.example.com", "--token", "valid_token"]
        with patch.object(sys, 'argv', test_args), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()

            expected_url = "https://api.example.com:443/v1/status?&details=true"
            expected_headers = {"x-api-key": "valid_token"}

            mock_get.assert_called_with(
                expected_url, timeout=30, verify=False, headers=expected_headers
            )

            self.assertIn("SERVING", mock_stdout.getvalue().strip())
            mock_exit.assert_called_with(0)

    @patch('requests.get')
    @patch('sys.exit')
    def test_success_incorrect_payload(self, mock_exit, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # Missing "push_servers"
        mock_get.return_value = mock_response

        test_args = ["script_name", "-H", "api.example.com", "--token", "valid_token"]
        with patch.object(sys, 'argv', test_args), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()

            expected_url = "https://api.example.com:443/v1/status?&details=true"
            expected_headers = {"x-api-key": "valid_token"}

            mock_get.assert_called_with(
                expected_url, timeout=30, verify=False, headers=expected_headers
            )

            self.assertIn("No push server available in response", mock_stdout.getvalue().strip())
            mock_exit.assert_called_with(2)

    @patch('requests.get')
    @patch('sys.exit')
    def test_connection_error(self, mock_exit, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        test_args = ["script_name", "-H", "api.example.com", "--token", "valid_token"]
        with patch.object(sys, 'argv', test_args), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()

            expected_url = "https://api.example.com:443/v1/status?&details=true"
            expected_headers = {"x-api-key": "valid_token"}

            mock_get.assert_called_with(
                expected_url, timeout=30, verify=False, headers=expected_headers
            )

            self.assertIn("Failed to connect", mock_stdout.getvalue().strip())
            mock_exit.assert_called_with(2)

if __name__ == '__main__':
    unittest.main()
