# test.py
import unittest
from ..main import app


class YourAppTestCase(unittest.TestCase):
  def setUp(self):
    self.app = app.test_client()

  def tearDown(self):
    pass

  def test_homepage(self):
    resp = self.app.get('/')
    self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
  unittest.main()
