#!/usr/bin/env python3
"""testing client.py methods"""
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import *
from fixtures import TEST_PAYLOAD

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch('client.get_json')
    def test_org(self, domain, mock_get_json):
        expected_result = mock_get_json.return_value = {"hello": "world"}
        client = GithubOrgClient(domain)
        result = client.org
        self.assertEqual(result, expected_result)
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{domain}')
class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch('client.get_json')
    def test_org(self, domain, mock_get_json):
        expected_result = mock_get_json.return_value = {"hello": "world"}
        client = GithubOrgClient(domain)
        result = client.org
        self.assertEqual(result, expected_result)
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{domain}')
class TestGithubOrgClient(unittest.TestCase):

    def test_public_repos_url(self):
        with patch('client.GithubOrgClient.org') as mock_org:
            mock_org.return_value = {"repos_url": "test_url"}
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, "test_url/repos")
            mock_org.assert_called_once()
class TestGithubOrgClient(unittest.TestCase):

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        mock_public_repos_url.return_value = "http://test_url"
        mock_get_json.return_value = [{"name": "test_repo"}]
        client = GithubOrgClient("test")
        result = client.public_repos()
        self.assertEqual(result, ["test_repo"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()
class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result
@parameterized_class(TEST_PAYLOADS)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        cls.mocked_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("test")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("test")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

    def mocked_requests_get(self, url):
        if url == self.org_payload["repos_url"]:
            return self.mocked_repos_payload
        elif url == self._public_repos_url:
            return self.mocked_repos_payload
        return None

    def setUp(self):
        self.get_mock = patch('requests.get')
        self.mock = self.get_mock.start()

        def side_effect(url):
            return self.mocked_requests_get(url)

        self.mock.side_effect = side_effect

        self.mocked_repos_payload = self.repos_payload
        
        self.mocked_get.return_value = self.mock
        self.mock.return_value.json.return_value = self.org_payload
@parameterized_class(TEST_PAYLOADS)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    
    def test_public_repos(self):
        client = GithubOrgClient("test")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("test")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
