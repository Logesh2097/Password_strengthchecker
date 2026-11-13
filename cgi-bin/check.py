#!/usr/bin/env python3
"""CGI script: read a password from the form and report how strong it is."""

from __future__ import annotations

import html
import os
import sys
from urllib.parse import parse_qs

from password_strength import check_password_strength

MAX_BODY_BYTES = 4096

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Password Strength Check</title>
  <style>
    body {{
      background-image: url('/image2.jpg');
      background-repeat: no-repeat;
      background-attachment: fixed;
      background-size: cover;
      text-align: center;
    }}
  </style>
</head>
<body>
  <h1>Result: {result}</h1>
  <p><a href="/">Check another password</a></p>
</body>
</html>"""


def read_password() -> str:
    """Return the ``password`` form field. Only a POST body is read, so the
    password never appears in a URL or in the server's access log."""
    if os.environ.get("REQUEST_METHOD", "GET").upper() != "POST":
        return ""
    try:
        length = min(int(os.environ.get("CONTENT_LENGTH") or 0), MAX_BODY_BYTES)
    except ValueError:
        length = 0
    body = sys.stdin.buffer.read(length).decode("utf-8", errors="replace")
    return parse_qs(body, keep_blank_values=True).get("password", [""])[0]


def main() -> None:
    result = check_password_strength(read_password())
    sys.stdout.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
    sys.stdout.write(PAGE.format(result=html.escape(result)))


if __name__ == "__main__":
    main()
