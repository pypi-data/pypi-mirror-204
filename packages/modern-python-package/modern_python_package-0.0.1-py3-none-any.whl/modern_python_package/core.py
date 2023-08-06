from http import HTTPStatus

import httpx


def do_things() -> int | None:
    response = httpx.get("https://gitlab.com/api/v4/version")
    if response.status_code != HTTPStatus.OK:
        return None

    data = response.json()

    if data["enterprise"]:
        return 42
    else:
        return 0
