import functools
import inspect
import logging
from datetime import datetime
from typing import Any, Optional, Dict
from collections import deque

import pytest as pytest

__all__ = ['AscendPythonReadConnector']


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


class MetadataSupport:
  def __init__(self,
               name,
               fingerprint,
               is_prefix,
               ):
    self.name: str = name
    self.fingerprint: str = fingerprint
    self.is_prefix: bool = is_prefix

  def to_dict(self):
    return dict((k, v) for k, v in self.__dict__.items() if v is not None)


class AscendPythonReadConnector:
  """This decorator automates the testing of read connectors by wrapping the read connector module
  in code that operates as if it was running in the platform"""

  def __init__(self,
               module=None,
               credentials=None,
               name=None,
               patches=None,
               skip_read_bytes=False,
               ):
    if patches is None:
      patches = []
    self.credentials = credentials
    self.module = module
    self.name = name
    self.def_context = _get_method(module, 'context')
    self.def_list_objects = _get_method(module, 'list_objects')
    self.def_read_bytes = _get_method(module, 'read_bytes')
    self.def_read_spark_dataframe = _get_method(module, 'read_spark_dataframe')
    self.def_read_pandas_dataframe = _get_method(module, 'read_pandas_dataframe')
    self.patches = patches
    self.skip_read_bytes = skip_read_bytes

    # inject pytest fixtures if they were applied to the global method
    caller_globals = inspect.stack()[1][0].f_globals
    caller_globals['context_result'] = _result_fixture('function', None)
    caller_globals['list_objects_result'] = _result_fixture('function', None)
    caller_globals['read_bytes_result'] = _result_fixture('function', None)
    caller_globals['mock_results'] = _result_fixture('function', None)

  def __process_list_objects(self, context, metadata):
        depth = 0
        queue = deque([(context, metadata, depth)])
        results = []

        while queue:
            current_context, current_metadata, current_depth = queue.popleft()
            for item in self.def_list_objects(current_context, current_metadata):
                logging.debug('partition level: %s meta: %s', current_depth, item)
                results.append(item)
                if item["is_prefix"]:
                    queue.append((current_context, item, current_depth + 1))

        return results

  def __call__(self, func):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
      logging.debug('calling the wrapper')

      # patch as requested
      patched = [m.start() for m in self.patches]
      context_result = self.def_context(self.credentials)
      context_result = context_result if context_result else {}

      # get the list objects/partitions
      list_objects_result = [o for o in self.__process_list_objects(context_result, {})]

      read_bytes_result = []
      if not self.skip_read_bytes:
        for result in list_objects_result:
          if self.def_read_bytes:
            assert not self.def_read_spark_dataframe
            assert not self.def_read_pandas_dataframe
            read_bytes_result = (list(b for b in self.def_read_bytes(context_result, MetadataSupport(**result).to_dict())))
          elif self.def_read_spark_dataframe:
            assert not self.def_read_bytes
            assert not self.def_read_pandas_dataframe
            read_bytes_result = self.def_read_spark_dataframe(context_result, MetadataSupport(**result).to_dict())
          elif self.def_read_pandas_dataframe:
            assert not self.def_read_bytes
            assert not self.def_read_spark_dataframe
            read_bytes_result = self.def_read_pandas_dataframe(context_result, MetadataSupport(**result).to_dict())

      logging.debug('read connector interface calls complete')
      # write the data back to the test method for assertion
      full_args = inspect.getfullargspec(func)
      if 'context_result' in full_args.args:
        kwargs['context_result'] = context_result
      if 'list_objects_result' in full_args.args:
        kwargs['list_objects_result'] = list_objects_result
      if 'read_bytes_result' in full_args.args:
        kwargs['read_bytes_result'] = read_bytes_result
      if 'mock_results' in full_args.args:
        kwargs['mock_results'] = patched

      # un-patch if required
      [p.stop() for p in patched if hasattr(p, "stop")]

      return func(*args, **kwargs)

    return wrapper
