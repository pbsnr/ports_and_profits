import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        # Test the home route
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Island Generator", response.data)  # Check if the title is in the response

    def test_generate_route(self):
        # Test the generate route with valid input
        payload = {
            "width": 10,
            "height": 10,
            "num_islands": 2,
            "island_size": 0.3
        }
        response = self.app.post("/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        grid = response.get_json()
        self.assertEqual(len(grid), 10)  # Check grid height
        self.assertEqual(len(grid[0]), 10)  # Check grid width

    def test_generate_route_invalid_input(self):
        # Test the generate route with invalid input
        payload = {
            "width": "invalid",
            "height": 10,
            "num_islands": 2,
            "island_size": 0.3
        }
        response = self.app.post("/generate", json=payload)
        self.assertEqual(response.status_code, 500)  # Expecting a server error due to invalid input

if __name__ == "__main__":
    unittest.main()