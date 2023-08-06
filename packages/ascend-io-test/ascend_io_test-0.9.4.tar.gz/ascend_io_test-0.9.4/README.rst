========================
Ascend.io Test Framework
========================

This package helps developers who are writing custom python for Ascend.io automated pipelines by providing a local
testing framework. Local testing speeds the development of python pipeline code. The local framework exercises the
code as if the code was running directly in the platform while giving you access to patching and mocking frameworks.

Documentation, including examples, is located in our `Ascend Developer Hub <https://developer.ascend.io>`_.

Release Notes
-------------

-------------
0.9.4
-------------
* Add ``skip_read_bytes`` to ``AscendPythonReadConnector`` so tests can skip reading data


Example
------------
Here is a basic python transformation test case example. The python code under test is located in a file
with the name ``my_python_transform.py`` and imported with the name ``my_python_transform``. Other variables,
imports, and code are omitted for brevity::

    @AscendPySparkTransform(spark=spark_session,
                            module=my_python_transform,
                            schema=input_schema,
                            data=[(123, 'NORMAL', today, today + datetime.timedelta(days=1))],
                            credentials=test_creds,
                            discover_schema=True,
                            patches=[patch('requests.post', return_value=Mock(status_code=200,
                                                                              text='{"internalReportIds":"REPORT_A"}')),
                                     patch('requests.get', return_value=Mock(status_code=200,
                                                                             text='{"status":"SUCCESS", "downloadLink": "https://test.my.download"}')),
                                     patch('pandas.read_csv', return_value=build_mock_csv()),
                                     ], )
    def test_normal_loading_process_single_record(input_dataframe, transform_result: DataFrame, mock_results: List[Mock]):
      """Check that a normal call does the work properly.
            Assert values are correct.
            Assert mock services are called."""
      assert input_dataframe
      assert transform_result
      assert transform_result.count() == 3
      dataset = transform_result.collect()
      # check field mapping
      assert dataset[0]['CUSTOMER_ID'] == '101'
      assert dataset[1]['CUSTOMER_ID'] == '102'
      assert dataset[2]['CUSTOMER_ID'] == '103'
      assert dataset[0]['YOUR_NAME'] == "customerName.one"
      assert dataset[0]['THE_OBJECTIVE'] == "customerBudget.one"
      assert dataset[0]['AD_ID'] == "tempId.one"
      assert dataset[0]['AD_NAME'] == "myName.one"
      assert dataset[0]['GEO_LOC'] == "geo_location.one"
      assert dataset[0]['ORDER_ID'] == "orderId.test"
      assert dataset[0]['ORDER_NAME'] == "orderName.test"
      assert dataset[0]['DT'] == "__time.one"
      assert dataset[0]['AUDIO_IMPRESSIONS'] == 1
      assert transform_result.columns.__contains__('RUN_ID')
      assert transform_result.columns.__contains__('REPORT_START_DT')
      assert transform_result.columns.__contains__('REPORT_END_DT')
      assert transform_result.columns.__contains__('record_number')
      # check mocks were properly called
      mock_results[0].assert_called_once()
      mock_results[1].assert_called_once_with(f"https://custom.io/v1/async-query/REPORT_A",
                                              headers={'agency': '12', 'x-api-key': 'key', 'Content-Type': 'application/json'})
      mock_results[2].assert_called_once_with("https://test.my.download", header=0, skip_blank_lines=True)


Decorators are available for all types of Ascend python implementation strategies. Testing scenarios are only limited
by your creativity and desire to produce high quality code.

Download your pipelines using the `Ascend CLI <https://pypi.org/project/ascend-io-cli/>`_ like this::

    ascend download data-flow MY_DATASERVICE MY_DATA_FLOW

Write some tests. When your test cases are complete, pushing the code to the platform is simple with
the `CLI <https://pypi.org/project/ascend-io-cli/>`_. For example::

    ascend apply data-flow MY_DATASERVICE MY_DATA_FLOW



---------------
Read the Docs
---------------
* `Ascend Developer Hub <https://developer.ascend.io>`_
* `Ascend.io <https://www.ascend.io>`_
* `Ascend CLI <https://pypi.org/project/ascend-io-cli/>`_
