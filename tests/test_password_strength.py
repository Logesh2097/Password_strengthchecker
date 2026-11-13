import os
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import urlencode

CGI_DIR = Path(__file__).resolve().parent.parent / "cgi-bin"
sys.path.insert(0, str(CGI_DIR))

from password_strength import STRONG, check_password_strength, is_strong  # noqa: E402


class PasswordStrengthTests(unittest.TestCase):
    def test_a_password_meeting_every_rule_is_strong(self):
        self.assertEqual(check_password_strength("Str0ng!pass"), STRONG)
        self.assertTrue(is_strong("Str0ng!pass"))

    def test_a_short_password_is_rejected_first(self):
        self.assertIn("at least 8 characters", check_password_strength("aB1!"))

    def test_an_empty_password_is_rejected(self):
        self.assertFalse(is_strong(""))

    def test_each_missing_character_class_is_named(self):
        cases = {
            "lowercase1!": "uppercase",
            "UPPERCASE1!": "lowercase",
            "NoDigits!!": "digit",
            "NoSpecial11": "special character",
        }
        for password, expected in cases.items():
            with self.subTest(password=password):
                self.assertIn(expected, check_password_strength(password))

    def test_brackets_and_backslash_count_as_special_characters(self):
        for special in "[]\\-_":
            with self.subTest(special=special):
                self.assertTrue(is_strong(f"Passw0rd{special}"))


class CgiScriptTests(unittest.TestCase):
    def run_cgi(self, method="POST", **fields):
        body = urlencode(fields).encode()
        env = {
            **os.environ,
            "REQUEST_METHOD": method,
            "CONTENT_LENGTH": str(len(body)),
            "CONTENT_TYPE": "application/x-www-form-urlencoded",
            "QUERY_STRING": urlencode(fields) if method == "GET" else "",
        }
        result = subprocess.run(
            [sys.executable, str(CGI_DIR / "check.py")],
            input=body, env=env, capture_output=True, check=True, timeout=30,
        )
        return result.stdout.decode()

    def test_the_response_has_one_header_block_then_html(self):
        output = self.run_cgi(password="Str0ng!pass")

        headers, _, body = output.partition("\r\n\r\n")
        self.assertEqual(headers, "Content-Type: text/html; charset=utf-8")
        self.assertTrue(body.startswith("<!DOCTYPE html>"))
        self.assertNotIn("Content-Type", body)

    def test_a_strong_password_is_reported_strong(self):
        self.assertIn("Password is strong.", self.run_cgi(password="Str0ng!pass"))

    def test_a_weak_password_is_told_what_is_missing(self):
        self.assertIn("at least one digit", self.run_cgi(password="NoDigits!!"))

    def test_a_password_in_the_url_is_ignored(self):
        self.assertIn("at least 8 characters", self.run_cgi(method="GET", password="Str0ng!pass"))

    def test_the_password_is_never_echoed_back(self):
        self.assertNotIn("Str0ng!pass", self.run_cgi(password="Str0ng!pass"))


if __name__ == "__main__":
    unittest.main()
