from http import HTTPStatus

from modern_python_package.core import do_things


def test_do_things_correctly(mocker):
    # GIVEN
    get_response_mock = mocker.patch(
        "modern_python_package.core.httpx.get").return_value
    get_response_mock.status_code = HTTPStatus.OK
    get_response_mock.json.return_value = {"enterprise": True}

    # WHEN
    actual = do_things()

    # THEN
    assert actual == 42


def test_do_things_non_enterprise(mocker):
    # GIVEN
    get_response_mock = mocker.patch(
        "modern_python_package.core.httpx.get").return_value
    get_response_mock.status_code = HTTPStatus.OK
    get_response_mock.json.return_value = {"enterprise": False}

    # WHEN
    actual = do_things()

    # THEN
    assert actual == 0
