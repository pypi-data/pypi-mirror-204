import pytest
from pytest_mock import MockFixture

from fiddler import FiddlerApi
from fiddler.v2.api.api import Client
from fiddler.v2.schema.server_info import ServerInfo, Version


def test_client_v1_creation_fail():
    with pytest.raises(ValueError):
        FiddlerApi('', '', '')


def test_client_v2_creation_fail():
    with pytest.raises(ValueError):
        FiddlerApi('', '', '', version=2)


def test_get_server_info_without_server_version(mocker: MockFixture):
    mocker.patch('fiddler.connection.Connection.check_connection', return_value='OK')

    server_info_dict = {
        'feature_flags': {
            'fairness': False,
        },
    }

    mock_get_server_info = mocker.patch.object(Client, '_get_server_info')
    mock_get_server_info.return_value = ServerInfo(**server_info_dict)

    client = FiddlerApi('https://test.fiddler.ai', 'test', 'foo-token', version=2)

    assert client.v2.server_info.server_version is None
    assert client.v2.server_info.feature_flags == server_info_dict['feature_flags']


def test_get_server_info_with_server_version(mocker: MockFixture):
    mocker.patch('fiddler.connection.Connection.check_connection', return_value='OK')

    server_info_dict = {
        'feature_flags': {
            'fairness': False,
        },
        'server_version': '23.1.1',
    }

    mock_get_server_info = mocker.patch.object(Client, '_get_server_info')
    mock_get_server_info.return_value = ServerInfo(**server_info_dict)

    client = FiddlerApi('https://test.fiddler.ai', 'test', 'foo-token', version=2)

    assert client.v2.server_info.server_version == Version.parse(
        server_info_dict['server_version']
    )
    assert client.v2.server_info.feature_flags == server_info_dict['feature_flags']
