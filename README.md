# Cookie-Thumper
Session hijacker

# Cookie Thumper — Web Session & Security Test Tool

**Cookie Thumper** is a Python script that uses Selenium and BeautifulSoup to automate security testing on web applications, focusing on:

- Session replay by cookie injection
- CSRF token rotation validation
- Session fixation vulnerability testing

---

## Features

- Inject cookies from a JSON file to simulate logged-in sessions
- Check if session cookies grant access to protected pages
- Verify CSRF tokens rotate properly to prevent token reuse attacks
- Test if session fixation vulnerabilities exist by forcing a session ID before login

---

## Requirements

- Python 3.8+
- Google Chrome browser installed
- ChromeDriver compatible with your Chrome version
- Can also be done via Firefox 
- Python packages:
  
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install selenium beautifulsoup4
  ```

---

Setup

1. Place ChromeDriver in your system and update the path in the script if necessary (default /usr/bin/chromedriver).

2. If you have used my other tools LS5, Torscraper it will be there anyway or you altered the oath in th to suit your needs.


3. Prepare your cookies JSON file (cookies.json) with cookies from the target domain, example:
```json
[
  {
    "name": "XSRF-TOKEN",
    "value": "your_xsrf_token_value",
    "path": "/",
    "secure": true
  },
  {
    "name": "session",
    "value": "your_session_cookie_value",
    "path": "/",
    "secure": true
  }
]
```
Filled out:
```json
[
  {
    "name": "XSRF-TOKEN",
    "value": "eyJpdiI6IjZzS1lVTlh2TXZRaXU3T1BVZ0Y3MGc9PSIsInZhbHVlIjoiZ3NZVG5HU2pqT0ZkWmdOdFpHSkhPdz09IiwibWFjIjoiNTFkNzMzZTg0MjQ1ZDUzNTk0MDc3YjI1MTZkZDc2MTQxMjcxMGZjZjVkNzFkOTAzNmIyZTQ1NjVlZDZiZWI5MSJ9",
    "path": "/",
    "secure": true
  },
  {
    "name": "pwned_labs_session",
    "value": "eyJpdiI6IkptMUhFV2p5U0Myb1cwRnNnSWVQXC9BPT0iLCJ2YWx1ZSI6IjE3azZ0Q0xuY3pRSkJPNkdtK0ZXaTZzZ0prb3hVaWFTYWhkT0lxRmN0bFhFZFpnZXZMQnd0Y0xXRU1pUGNLUkJ6QzRSQlladDBVb3VvSjd4d1ZURmU5b2lRcGpUb1ZvYkhtNzNsYVd6RXNkVE5MS29ZdWthVmppV0pXbmNBVkpNbWlMUEpZaHljZGxZNG9RMVpBVGdKZGdHd3pZUWxMZ0RjMTQ3S0s4N3Z3YVhmT0hRZG0wRUlBSmxOeGFpYXVZdG8iLCJtYWMiOiJjOWQxMjFmN2U2YmExODg2NjcxMGU5ZjQ1YjJjZGY1MmYxYmFlNzUyYmZmZDQzZDkyYjQ4ZjI3NzZhOWY4NTRkODliIn0=",
    "path": "/",
    "secure": true
  }
]                                                                       
```



---

Usage

Run the script with required arguments:
```bash
python3 cookiethumperv1.py \
  --target-url https://pwnedlabs.io/users/DeadmanXXXII \
  --login-url https://pwnedlabs.io/auth/google/redirect \
  --cookie-file ./cookies.json \
  --domain pwnedlabs.io
```
Arguments

Argument	Description	Required	Default

--target-url	URL of the page to test session validity	Yes	
--login-url	URL of the login page for CSRF & fixation tests	Yes	
--cookie-file	Path to JSON file containing cookies	Yes	
--domain	Domain of the target site (for cookie scope)	Yes	
--fake-session-id	Session ID value to test session fixation	No	evilSession12345



---

How It Works

1. Cookie Injection & Session Replay
Injects cookies from the JSON file into a browser session and verifies if you are logged in by checking page content.


2. CSRF Token Rotation Test
Loads the login page twice and extracts CSRF tokens to confirm they change between requests.


3. Session Fixation Test
Injects a fake session cookie, attempts login, and checks if the session ID is regenerated.




---

Troubleshooting

InvalidCookieDomainException:
Ensure the --domain matches the domain of URLs exactly, and that the driver is on the correct page before adding cookies.

Chromedriver Issues:
Verify your ChromeDriver version matches your installed Chrome browser version.

Timeouts or Element Not Found:
Adjust time.sleep durations or update element selectors based on the target site’s HTML structure.



---

License

MIT License


---

Disclaimer

This tool is intended for authorized security testing only. Do not use it against websites without permission.


---

- Cookie thumper in action
![Terminal](https://raw.githubusercontent.com/DeadmanXXXII/Cookie-Thumper/main/Screenshot_20250722-222557.png)

