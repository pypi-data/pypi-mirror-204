from starlette.applications import Starlette
from starlette.types import Scope

from sag_py_fastapi_request_id import request_context
from sag_py_fastapi_request_id.request_context_middleware import RequestContextMiddleware


def test_call_no_request_id_for_lifespan() -> None:
    # Arrange
    app = Starlette()
    middleware = RequestContextMiddleware(app)
    scope: Scope = {"type": "lifespan"}

    # Act
    middleware._set_request_id(scope)

    # Assert
    assert request_context.get_request_id() == ""


def test_call_request_id_for_websocket() -> None:
    # Arrange
    app = Starlette()
    middleware = RequestContextMiddleware(app)
    scope: Scope = {"type": "websocket"}

    # Act
    middleware._set_request_id(scope)

    # Assert
    assert len(request_context.get_request_id()) == 32


def test_call_request_id_for_http() -> None:
    # Arrange
    app = Starlette()
    middleware = RequestContextMiddleware(app)
    scope: Scope = {"type": "http"}

    # Act
    middleware._set_request_id(scope)

    # Assert
    assert len(request_context.get_request_id()) == 32
