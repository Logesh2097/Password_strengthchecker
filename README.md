# Password Strength Checker

[![CI](https://github.com/Logesh2097/Password_strengthchecker/actions/workflows/ci.yml/badge.svg)](https://github.com/Logesh2097/Password_strengthchecker/actions/workflows/ci.yml)

A small Python CGI web app that checks a password against a set of strength
rules and tells you the first rule it breaks.

## Overview

An HTML form posts a password to a CGI script. The script checks it and returns
a page saying either that the password is strong or what it is missing. It uses
only the Python standard library and was written as a learning project for CGI
and regular expressions.

## Features

- Five rules: at least 8 characters, an uppercase letter, a lowercase letter, a digit, and a special character.
- The rules live in one module with no web code, so they can be reused and tested on their own.
- The password is sent by `POST`, so it does not appear in the URL or the server's access log, and it is never echoed back in the response.
- No third-party dependencies.

## Architecture

```
index.html ── POST password ──▶ cgi-bin/check.py ──▶ password_strength.check_password_strength()
           ◀── result page ────
```

| File | Responsibility |
|---|---|
| `index.html` | The form |
| `cgi-bin/check.py` | Reads the form field and prints the result page |
| `cgi-bin/password_strength.py` | The rules |

## Technology stack

Python 3.10+ (standard library only), CGI, HTML. ruff and GitHub Actions for checks.

## Project structure

```
.
├── index.html
├── image2.jpg                    # page background
├── cgi-bin/
│   ├── check.py                  # CGI entry point
│   └── password_strength.py      # the rules
└── tests/
    └── test_password_strength.py
```

## Running the application

No installation is needed beyond Python.

```bash
git clone https://github.com/Logesh2097/Password_strengthchecker.git
cd Password_strengthchecker
python -m http.server --cgi 8000
```

Open <http://127.0.0.1:8000/> and submit a password.

`http.server --cgi` is deprecated from Python 3.13 and removed in 3.15. On
those versions, serve the folder with any CGI-capable web server (for example
Apache with `mod_cgi`), with `cgi-bin/` enabled for script execution. On Linux
and macOS `cgi-bin/check.py` must be executable (`chmod +x`); it is committed
that way.

There are no environment variables.

## Using the rules from Python

```python
from password_strength import check_password_strength, is_strong

check_password_strength("NoDigits!!")   # 'Password must contain at least one digit.'
is_strong("Str0ng!pass")                # True
```

## Testing

```bash
python -m unittest discover -s tests -v
ruff check .        # pip install ruff
```

The tests cover the rules and run the CGI script as a subprocess. The same
commands run in GitHub Actions on every push.

## Limitations and future improvements

- The rules measure composition only. A password such as `Password1!` passes; a check against a list of common passwords would catch it.
- Report every unmet rule at once instead of only the first.
- This is a local demo. Serve it over HTTPS before sending real passwords to it.
