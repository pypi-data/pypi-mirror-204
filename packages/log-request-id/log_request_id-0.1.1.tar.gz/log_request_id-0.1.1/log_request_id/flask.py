import os
from collections.abc import Callable
from typing import Optional

from .request_id import (DEFAULT_REQUEST_ID_OBJECT_NAME,
                         default_request_id_generator, register_context_getter)


@register_context_getter(skip=os.getenv("LOG_REQUEST_ID_FRAMEWORK_SUPPORT") == "flask")
def get_flask_context_request_id(request_id_object_name=DEFAULT_REQUEST_ID_OBJECT_NAME):
    from flask import g, has_request_context

    return g.get(request_id_object_name, None) if has_request_context() else None


def init_flask_request_id_handler(
    app,
    request_id_object_name: str = DEFAULT_REQUEST_ID_OBJECT_NAME,
    request_id_generator: Callable = default_request_id_generator,
):
    app.before_request(
        lambda: _init_request_id(
            request_id_object_name=request_id_object_name, request_id_generator=request_id_generator
        )
    )
    app.after_request(lambda response: _set_response_header(response, request_id_object_name=request_id_object_name))


def _init_request_id(
    request_id_object_name: str = DEFAULT_REQUEST_ID_OBJECT_NAME,
    request_id_generator: Callable = default_request_id_generator,
):
    from flask import g, has_request_context, request

    request_id = request.headers.get("X-Request-ID", request_id_generator())

    if has_request_context() and g.get(request_id_object_name) is None:
        setattr(g, request_id_object_name, request_id)


def _set_response_header(
    response,
    request_id_object_name: str = DEFAULT_REQUEST_ID_OBJECT_NAME,
):
    from flask import g, has_request_context

    if has_request_context():
        request_id = g.get(request_id_object_name)
        response.headers.add("X-Request-ID", request_id)

    return response


def suppress_flask_request_id(request_id_object_name: Optional[str] = None):
    from flask import g, has_request_context

    request_id_object_name = request_id_object_name or DEFAULT_REQUEST_ID_OBJECT_NAME

    if has_request_context():
        g.pop(request_id_object_name, None)
