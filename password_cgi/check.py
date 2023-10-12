#!C:\Python311\python.exe
print ("Content-type: text/html\r\n\r\n")

import cgi
import re

# Function to check password strength
def check_password_strength(password):
    # Minimum length check
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    
    # Regular expressions for various password requirements
    has_uppercase = re.search(r"[A-Z]", password)
    has_lowercase = re.search(r"[a-z]", password)
    has_digit = re.search(r"\d", password)
    has_special_char = re.search(r"[!@#$%^&*()_+\-=[\]{};':\"\\|,.<>/?]", password)
    
    # Check if all requirements are met
    if not has_uppercase:
        return "Password must contain at least one uppercase letter."
    if not has_lowercase:
        return "Password must contain at least one lowercase letter."
    if not has_digit:
        return "Password must contain at least one digit."
    if not has_special_char:
        return "Password must contain at least one special character."
    
    return "Password is strong."

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get password value from form
password = form.getvalue("password", "")

# Perform password strength check
result = check_password_strength(password)

# Print CGI response
print ("Content-type:text/html\n\r\n\r")
print ("<html>")
print ("<head>")
print ("<title>Password Strength Check</title>")
print ("</head>")
print ("<body>")
print("<h2>")
print("<style>")
print('''body {background-image: url('image2.jpg');
          background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;

}''')
print("</style>")
print('''<h1>
    <p style="text-align:center;">''')
print("<p>Result: " + result + "</p>")
print("</h1>")
print("</p>")
print("</h2>")
int("<br>")
print("<br>")
print("<form action='submit.py'>")
print("<input type='submit' value='next'>")
print("</form>")
print ("</body>")
print ("</html>")

