import functools
import inspect
import io
import logging
from typing import Any

import pytest

__all__ = ['AscendPythonBytestreamReadConnector']


def _get_method(module, name):
  if module and hasattr(module, name):
    meth = getattr(module, name)
    return meth if callable(meth) else None
  return None


def _result_fixture(scope, params):
  @pytest.fixture(scope=scope, params=params)
  def result():
    pass

  return result


class AscendPythonBytestreamReadConnector:
  """Read as if processing bytestream from S3 connectors"""

  def __init__(self,
               module=None,
               bytestream=None,
               reader=None,
               ):
    self.module = module
    self.bytestream = bytes(bytestream, 'utf-8') if isinstance(bytestream, str) else bytes(bytestream) if bytestream else None
    self.reader = reader if reader else io.BytesIO(self.bytestream)
    self.def_parser_function = _get_method(self.module, 'parser_function')
    self.on_next = []

    # inject pytest fixtures if they were applied to the global method
    caller_globals = inspect.stack()[1][0].f_globals
    caller_globals['on_next_results'] = _result_fixture('function', None)

  def _on_next(self, record):
    self.on_next.append(record)

  def __call__(self, func):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
      logging.debug('calling the wrapper')

      self.def_parser_function(self.reader, self._on_next)

      logging.debug('read connector interface calls complete')
      # write the data back to the test method for assertion
      full_args = inspect.getfullargspec(func)
      if 'on_next_results' in full_args.args:
        kwargs['on_next_results'] = self.on_next

      return func(*args, **kwargs)

    return wrapper
