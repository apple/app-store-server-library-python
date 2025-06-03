import unittest

from appstoreserverlibrary.models.FirstSendAttemptResult import FirstSendAttemptResult

class TestFirstSendAttemptResult(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(FirstSendAttemptResult.SUCCESS, "SUCCESS")
        self.assertEqual(FirstSendAttemptResult.TIMED_OUT, "TIMED_OUT")
        self.assertEqual(FirstSendAttemptResult.TLS_ISSUE, "TLS_ISSUE")
        self.assertEqual(FirstSendAttemptResult.CIRCULAR_REDIRECT, "CIRCULAR_REDIRECT")
        self.assertEqual(FirstSendAttemptResult.NO_RESPONSE, "NO_RESPONSE")
        self.assertEqual(FirstSendAttemptResult.SOCKET_ISSUE, "SOCKET_ISSUE")
        self.assertEqual(FirstSendAttemptResult.UNSUPPORTED_CHARSET, "UNSUPPORTED_CHARSET")
        self.assertEqual(FirstSendAttemptResult.INVALID_RESPONSE, "INVALID_RESPONSE")
        self.assertEqual(FirstSendAttemptResult.PREMATURE_CLOSE, "PREMATURE_CLOSE")
        self.assertEqual(FirstSendAttemptResult.UNSUCCESSFUL_HTTP_RESPONSE_CODE, "UNSUCCESSFUL_HTTP_RESPONSE_CODE")
        self.assertEqual(FirstSendAttemptResult.OTHER, "OTHER")

if __name__ == '__main__':
    unittest.main()
