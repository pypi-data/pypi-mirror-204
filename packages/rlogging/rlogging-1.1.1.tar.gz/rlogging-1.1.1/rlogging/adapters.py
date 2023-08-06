import inspect
import logging
import sys
import uuid
from inspect import FrameInfo
from types import FrameType
from typing import Any


class RsLoggerAdapter(logging.LoggerAdapter):
    """Путь логирования

    Создание логов, через флоу позволяет обоготить их

    """

    flow_id: uuid.UUID

    def __init__(self, logger: logging.Logger, extra: dict | None = None) -> None:
        extra = extra if extra is not None else {}

        super().__init__(logger, extra)

        self.flow_id = uuid.uuid1()

    def _extra_update(self, kwargs: dict, extra: dict):
        kwargs['extra'] = extra | kwargs.get('extra', {})

    def get_frame(self, stacklevel: int = 41) -> FrameType:
        return sys._getframe(5)

    def get_class_info(self) -> dict | None:
        frame = self.get_frame()
        obj = frame.f_locals.get('self')

        if obj is None:
            return None

        module = inspect.getmodule(obj.__class__)
        class_path = f'{module.__name__}.{obj.__class__.__name__}'

        return {'class': class_path, 'object': obj, 'object_id': id(obj)}

    def process(self, msg: Any, kwargs: dict) -> tuple[Any, dict]:
        kwargs.setdefault('stacklevel', 2)

        extra = {
            'flow_id': self.flow_id,
        }

        self._extra_update(kwargs, extra)
        self._extra_update(kwargs, self.extra)

        if extra := self.get_class_info():
            self._extra_update(kwargs, extra)

        return msg, kwargs


class AppLoggerAdapter(RsLoggerAdapter):
    def queries(self, queries: list, *args, **kwargs):
        kwargs.setdefault('stacklevel', 4)
        self.info(f'processing queries: {len(queries)}', **kwargs)


class HttpLoggerAdapter(AppLoggerAdapter):
    """Флоу для логирования веб запросов/ответов"""

    def request(
        self,
        url: str,
        method: str,
        *args,
        **kwargs,
    ):
        kwargs.setdefault('stacklevel', 3)

        extra = {
            'http': {
                'url': url,
                'method': method,
            }
        }
        self._extra_update(kwargs, extra)

        self.info('http request', **kwargs)

    def response(self, code: int, *args, **kwargs):
        kwargs.setdefault('stacklevel', 3)

        extra = {
            'http': {
                'code': code,
            },
        }
        self._extra_update(kwargs, extra)

        self.info('http response', **kwargs)

    def processing(
        self,
        path: str,
        route: str,
        route_name: str,
        view: str,
        view_args: tuple,
        view_kwargs: dict,
        namespace: str,
        *args,
        **kwargs,
    ):
        kwargs.setdefault('stacklevel', 4)

        extra = {
            'processing': {
                'path': path,
                'route': route,
                'route_name': route_name,
                'view': view,
                'view_args': view_args,
                'view_kwargs': view_kwargs,
                'namespace': namespace,
            },
        }
        self._extra_update(kwargs, extra)

        self.info('http process_view', **kwargs)
