import nbforms

import unittest
import responses

class TestNbforms(unittest.TestCase):

    @responses.activate
    def setUp(self):
        self.correct_api_key = "SOME_API_KEY"
        responses.add(responses.POST, "https://nbforms-demo-server.herokuapp.com/auth", body=self.correct_api_key)
        self.form = nbforms.Form("test/nbforms_config.json")

    def test_config_storage(self):
        self.assertEqual(len(self.form._identifiers), 4)
        self.assertEqual(self.form._identifiers, ["q1", "q2", "q3", "q4"])

    def test_api_key_storage(self):
        self.assertEqual(self.form._api_key, self.correct_api_key, "incorrect API key")
        self.assertEqual(nbforms.__API_KEYS__[self.form._server_url], self.correct_api_key, "API key not stored in global variable")

    def test_response_storage(self):
        self.form.ask("q1")
        self.assertIsNone(self.form._responses["q1"])
        self.assertFalse(self.form._updated_since_last_post["q1"])

    @responses.activate
    def test_requests(self):
        responses.add(responses.POST, "https://nbforms-demo-server.herokuapp.com/submit", body="SUBMISSION SUCCESSFUL")
        self.form._send_response()
