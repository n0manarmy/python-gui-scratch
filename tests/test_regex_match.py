import unittest
import re

class TestRegexMatch(unittest.TestCase):

    def test_regex_match(self):
        v1 = "ASD-1234"
        v2 = "AS-1234"
        v3 = "AS-11234"
        v4 = "ASD-11234"
        v5 = "ASDD-1234"
        v6 = "ASD-123"

        pattern = "([A-z]{3}-[0-9]{1,})"
        # print(re.search(pattern, v1))
        self.assertTrue(re.match(pattern, v1))
        self.assertFalse(re.match(pattern, v2))
        self.assertFalse(re.match(pattern, v3))
        self.assertTrue(re.match(pattern, v4))
        self.assertFalse(re.match(pattern, v5))
        self.assertTrue(re.match(pattern, v6))


if __name__ == '__main__':
    unittest.main()