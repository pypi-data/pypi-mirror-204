from tests.TestUtils import *
import pytest
from EVECelery import EVECeleryWorker
from redis.exceptions import ConnectionError
from redis.exceptions import AuthenticationError


class TestCeleryWorker:
    def test_init_no_running_servers(self, mock_env_no_servers):
        """test responses on init when no servers are running"""
        with pytest.raises(ConnectionError):
            EVECeleryWorker(connection_check=True)

        EVECeleryWorker()  # should not raise an exception since connection_check is by default false

    def test_init_running_servers(self, mock_env_rabbitmq_redis):
        """test responses on init when servers are running"""
        EVECeleryWorker(connection_check=True)  # should not raise an exception

    def test_init_running_servers_redis_bad_auth(self, mock_env_rabbitmq_redis, monkeypatch):
        """test bad auth to redis"""
        monkeypatch.setenv('EVECelery_Redis_ResultBackend_Password', 'WrongPass')
        with pytest.raises(AuthenticationError):
            EVECeleryWorker(connection_check=True)  # should raise auth error
