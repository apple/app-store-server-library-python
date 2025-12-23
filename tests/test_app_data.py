# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

import json
import unittest

from appstoreserverlibrary.models.AppData import AppData
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter
from tests.util import read_data_from_file


class AppDataTest(unittest.TestCase):
    def test_app_data_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/appData.json')

        app_data_dict = json.loads(json_data)
        app_data = _get_cattrs_converter(AppData).structure(app_data_dict, AppData)

        self.assertEqual(987654321, app_data.appAppleId)
        self.assertEqual("com.example", app_data.bundleId)
        self.assertEqual(Environment.SANDBOX, app_data.environment)
        self.assertEqual("Sandbox", app_data.rawEnvironment)
        self.assertEqual("signed-app-transaction-info", app_data.signedAppTransactionInfo)
