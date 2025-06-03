import unittest

from appstoreserverlibrary.models.ResponseBodyV2 import ResponseBodyV2

class TestResponseBodyV2(unittest.TestCase):
    def test_initialization(self):
        response_body = ResponseBodyV2(signedPayload="test_payload")
        self.assertEqual(response_body.signedPayload, "test_payload")

        response_body_default = ResponseBodyV2()
        self.assertIsNone(response_body_default.signedPayload)

if __name__ == '__main__':
    unittest.main()
