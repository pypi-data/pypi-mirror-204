import decimal
import functools
import inspect
import logging
from datetime import datetime
from typing import Any

import pyspark.sql.types
import pyspark.sql.types as T
import pytest as pytest
from pyspark.sql import SparkSession, DataFrame

__all__ = ['AscendPySparkTransform']


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


def _get_schema_discovery_df(spark: SparkSession, schema: T.StructType) -> DataFrame:
  """Capture a dataframe with default values for the purposes of determining
  the output schema for a particular transformation"""
  now = datetime.now()

  def get_dummy_val(dt: T.DataType) -> Any:
    if isinstance(dt, T.StringType):
      return 'A'
    if isinstance(dt, T.BooleanType):
      return False
    if isinstance(dt, (T.DoubleType, T.FloatType)):
      return 1.0
    if isinstance(dt, (T.IntegerType, T.LongType, T.ShortType)):
      return 1
    if isinstance(dt, T.DecimalType):
      return decimal.Decimal(0)
    if isinstance(dt, T.DateType):
      return now.date()
    if isinstance(dt, T.TimestampType):
      return now
    return None

  row = {f.name: get_dummy_val(f.dataType) for f in schema}
  return spark.createDataFrame(data=[T.Row(**row)], schema=schema, verifySchema=False)


class AscendPySparkTransform:
  """This decorator automates the testing of custom python transforms."""

  def __init__(self,
               spark,
               module=None,
               discover_schema=True,
               schema=None,
               data=None,
               patches=None,
               credentials=None,
               ):
    if data is None:
      data = []
    if patches is None:
      patches = []
    self.spark_session = spark
    self.module = module
    self.discover_schema = discover_schema
    self.in_schema = schema
    self.in_data = data
    self.credentials = credentials
    self.patches = patches
    self.def_transform = _get_method(self.module, 'transform')
    self.def_infer_schema = _get_method(self.module, 'infer_schema')

    caller_globals = inspect.stack()[1][0].f_globals
    caller_globals['transform_schema'] = _result_fixture('function', None)
    caller_globals['transform_exception'] = _result_fixture('function', None)
    caller_globals['input_dataframe'] = _result_fixture('function', None)
    caller_globals['transform_result'] = _result_fixture('function', None)
    caller_globals['mock_results'] = _result_fixture('function', None)

  def __call__(self, func):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
      logging.debug('calling the transform wrapper')

      # patch as requested
      patched = [m.start() for m in self.patches if hasattr(m, "start")]

      transform_schema_df = None

      if self.discover_schema:
        if self.def_infer_schema:
          transform_schema = self.def_infer_schema(self.spark_session, [], self.credentials)
          transform_schema_df = self.spark_session.createDataFrame(schema=transform_schema, data=[])
        else:
          empty_df = _get_schema_discovery_df(self.spark_session, self.in_schema)
          transform_schema_df = self.def_transform(self.spark_session, [empty_df], self.credentials)
          logging.debug(f'schema discovery returned {transform_schema_df}')

      if self.in_data:
        input_dataframe = self.spark_session.createDataFrame(self.in_data, self.in_schema)
      else:
        input_dataframe = self.spark_session.createDataFrame(self.spark_session.sparkContext.emptyRDD(),
                                                             self.in_schema if self.in_schema else pyspark.sql.types.StructType())

      transform_result = None
      transform_exception = None
      try:
        transform_result = self.def_transform(self.spark_session, [input_dataframe], self.credentials)
      except Exception as ex:
        transform_exception = ex

      logging.debug('transform interface calls complete')
      # write the data back to the test method for assertion
      full_args = inspect.getfullargspec(func)
      if 'transform_schema' in full_args.args:
        kwargs['transform_schema'] = transform_schema_df.schema if transform_schema_df else None
      if 'input_dataframe' in full_args.args:
        kwargs['input_dataframe'] = input_dataframe
      if 'transform_result' in full_args.args:
        kwargs['transform_result'] = transform_result
      if 'mock_results' in full_args.args:
        kwargs['mock_results'] = patched
      if 'transform_exception' in full_args.args:
        kwargs['transform_exception'] = transform_exception
      elif transform_exception:
        raise transform_exception

      # un-patch if required
      [p.stop() for p in self.patches if hasattr(p, "stop")]

      return func(*args, **kwargs)

    return wrapper
