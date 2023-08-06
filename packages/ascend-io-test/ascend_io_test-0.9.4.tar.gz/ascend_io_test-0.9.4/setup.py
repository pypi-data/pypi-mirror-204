# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ascend_io_test', 'ascend_io_test.framework']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=3.3.1,<4.0.0', 'pytest-mock>=3.10.0,<4.0.0', 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'ascend-io-test',
    'version': '0.9.4',
    'description': 'The Ascend Python Test Framework',
    'long_description': '========================\nAscend.io Test Framework\n========================\n\nThis package helps developers who are writing custom python for Ascend.io automated pipelines by providing a local\ntesting framework. Local testing speeds the development of python pipeline code. The local framework exercises the\ncode as if the code was running directly in the platform while giving you access to patching and mocking frameworks.\n\nDocumentation, including examples, is located in our `Ascend Developer Hub <https://developer.ascend.io>`_.\n\nRelease Notes\n-------------\n\n-------------\n0.9.4\n-------------\n* Add ``skip_read_bytes`` to ``AscendPythonReadConnector`` so tests can skip reading data\n\n\nExample\n------------\nHere is a basic python transformation test case example. The python code under test is located in a file\nwith the name ``my_python_transform.py`` and imported with the name ``my_python_transform``. Other variables,\nimports, and code are omitted for brevity::\n\n    @AscendPySparkTransform(spark=spark_session,\n                            module=my_python_transform,\n                            schema=input_schema,\n                            data=[(123, \'NORMAL\', today, today + datetime.timedelta(days=1))],\n                            credentials=test_creds,\n                            discover_schema=True,\n                            patches=[patch(\'requests.post\', return_value=Mock(status_code=200,\n                                                                              text=\'{"internalReportIds":"REPORT_A"}\')),\n                                     patch(\'requests.get\', return_value=Mock(status_code=200,\n                                                                             text=\'{"status":"SUCCESS", "downloadLink": "https://test.my.download"}\')),\n                                     patch(\'pandas.read_csv\', return_value=build_mock_csv()),\n                                     ], )\n    def test_normal_loading_process_single_record(input_dataframe, transform_result: DataFrame, mock_results: List[Mock]):\n      """Check that a normal call does the work properly.\n            Assert values are correct.\n            Assert mock services are called."""\n      assert input_dataframe\n      assert transform_result\n      assert transform_result.count() == 3\n      dataset = transform_result.collect()\n      # check field mapping\n      assert dataset[0][\'CUSTOMER_ID\'] == \'101\'\n      assert dataset[1][\'CUSTOMER_ID\'] == \'102\'\n      assert dataset[2][\'CUSTOMER_ID\'] == \'103\'\n      assert dataset[0][\'YOUR_NAME\'] == "customerName.one"\n      assert dataset[0][\'THE_OBJECTIVE\'] == "customerBudget.one"\n      assert dataset[0][\'AD_ID\'] == "tempId.one"\n      assert dataset[0][\'AD_NAME\'] == "myName.one"\n      assert dataset[0][\'GEO_LOC\'] == "geo_location.one"\n      assert dataset[0][\'ORDER_ID\'] == "orderId.test"\n      assert dataset[0][\'ORDER_NAME\'] == "orderName.test"\n      assert dataset[0][\'DT\'] == "__time.one"\n      assert dataset[0][\'AUDIO_IMPRESSIONS\'] == 1\n      assert transform_result.columns.__contains__(\'RUN_ID\')\n      assert transform_result.columns.__contains__(\'REPORT_START_DT\')\n      assert transform_result.columns.__contains__(\'REPORT_END_DT\')\n      assert transform_result.columns.__contains__(\'record_number\')\n      # check mocks were properly called\n      mock_results[0].assert_called_once()\n      mock_results[1].assert_called_once_with(f"https://custom.io/v1/async-query/REPORT_A",\n                                              headers={\'agency\': \'12\', \'x-api-key\': \'key\', \'Content-Type\': \'application/json\'})\n      mock_results[2].assert_called_once_with("https://test.my.download", header=0, skip_blank_lines=True)\n\n\nDecorators are available for all types of Ascend python implementation strategies. Testing scenarios are only limited\nby your creativity and desire to produce high quality code.\n\nDownload your pipelines using the `Ascend CLI <https://pypi.org/project/ascend-io-cli/>`_ like this::\n\n    ascend download data-flow MY_DATASERVICE MY_DATA_FLOW\n\nWrite some tests. When your test cases are complete, pushing the code to the platform is simple with\nthe `CLI <https://pypi.org/project/ascend-io-cli/>`_. For example::\n\n    ascend apply data-flow MY_DATASERVICE MY_DATA_FLOW\n\n\n\n---------------\nRead the Docs\n---------------\n* `Ascend Developer Hub <https://developer.ascend.io>`_\n* `Ascend.io <https://www.ascend.io>`_\n* `Ascend CLI <https://pypi.org/project/ascend-io-cli/>`_\n',
    'author': 'Ascend.io Engineering',
    'author_email': 'support@ascend.io',
    'maintainer': 'Ascend.io Engineering',
    'maintainer_email': 'support@ascend.io',
    'url': 'https://www.ascend.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
