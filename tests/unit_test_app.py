import unittest
from app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Configure test client
        app.testing = True
        self.client = app.test_client()

    def test_home_page(self):
        # Send a GET request to path `/`
        response = self.client.get("/")

        # Verify response 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verify content in response
        self.assertIn(b"Welcome to a very simple Python app!", response.data)


if __name__ == "__main__":
    unittest.main()