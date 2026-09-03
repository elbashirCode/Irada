import unittest

from app import app


class AppSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_home_page_is_successful_and_contains_irada_content(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Irada", response.get_data(as_text=True))
        self.assertIn("إرادة", response.get_data(as_text=True))

    def test_health_endpoint_returns_ok_status(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()