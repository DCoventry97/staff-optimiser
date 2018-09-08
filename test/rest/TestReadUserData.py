import unittest
from src.server.rest import read_user_data


class TestReadUserData(unittest.TestCase):
    # Tests for the read() function
    def test_read(self):
        username = "User"
        # test that read() returns something
        self.assertFalse(read_user_data.read(username), None)
