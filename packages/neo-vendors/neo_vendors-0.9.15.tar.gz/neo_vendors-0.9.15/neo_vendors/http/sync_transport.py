import traceback

import requests

from neo_vendors.date_time import utc_now
from neo_vendors.http import request_context


class SessionLoggable(requests.Session):
    encoding = 'utf-8'
    request_outgoing_handler: request_context.RequestOutgoingHandlerProtocol

    def __init__(self, request_outgoing_handler: request_context.RequestOutgoingHandlerProtocol):
        super().__init__()
        self.request_outgoing_handler = request_outgoing_handler

    def create_context(self, request: requests.PreparedRequest) -> request_context.RequestOutgoing:
        if request.body is None:
            request_body_bytes = None
        elif isinstance(request.body, str):
            request_body_bytes = request.body.encode(self.encoding)
        else:
            request_body_bytes = request.body
        context = request_context.RequestOutgoing(
            request_datetime=utc_now(),
            request_url=request.url,
            request_method=request.method,
            request_headers=dict(request.headers),
            request_body=request_body_bytes,
        )
        return context

    def update_context(self, context: request_context.RequestOutgoing, response: requests.Response):
        context.response_datetime = utc_now()
        context.response_status_code = response.status_code
        context.response_headers = dict(response.headers)
        context.response_body = response.content
        if context.response_datetime is not None and context.request_datetime is not None:
            context.elapsed_time = context.response_datetime - context.request_datetime
        else:
            context.elapsed_time = None

    def set_exception_context(self, context: request_context.RequestOutgoing, exception_log: str):
        context.exception = exception_log

    def send(self, request: requests.PreparedRequest, **kwargs) -> requests.Response:
        context = self.create_context(request)
        try:
            response = super().send(request, **kwargs)
            self.update_context(context, response)
            return response
        except Exception as exc:
            self.set_exception_context(context, traceback.format_exc())
            raise exc from exc
        finally:
            self.request_outgoing_handler(context)
