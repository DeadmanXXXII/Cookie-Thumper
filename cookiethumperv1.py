import argparse
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# ----- FUNCTIONS -----

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service("/usr/bin/chromedriver")  # Update path if needed
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def load_cookies_from_file(file_path):
    """Load cookies from a JSON or txt file with one JSON object per line"""
    with open(file_path, "r") as f:
        content = f.read().strip()
        try:
            # Try JSON array format
            cookies = json.loads(content)
        except json.JSONDecodeError:
            # Try line-by-line JSON objects (each line a cookie)
            cookies = []
            for line in content.splitlines():
                if line.strip():
                    cookies.append(json.loads(line))
    return cookies

def inject_cookies(driver, url, cookies, domain):
    print(f"[*] Navigating to {url}")
    driver.get(url)
    time.sleep(1)
    driver.delete_all_cookies()
    for cookie in cookies:
        # Ensure cookie has domain set correctly
        cookie['domain'] = domain
        # Remove attributes not accepted by Selenium
        cookie.pop('sameSite', None)
        cookie.pop('expiry', None)
        driver.add_cookie(cookie)
    driver.get(url)
    time.sleep(2)

def check_session_validity(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    if "login" not in soup.text.lower():
        print("[+] Session valid: user appears logged in.")
    else:
        print("[-] Session invalid: redirected to login.")

def extract_csrf_token(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    token_input = soup.find("input", {"name": "_token"})
    if token_input:
        return token_input.get("value")
    return None

def test_csrf_token_change(driver, login_url):
    print("[*] Testing CSRF Token Reuse...")
    driver.get(login_url)
    time.sleep(1)
    token1 = extract_csrf_token(driver)
    print(f"[-] First Token: {token1}")
    driver.refresh()
    time.sleep(1)
    token2 = extract_csrf_token(driver)
    print(f"[-] Second Token: {token2}")
    if token1 != token2:
        print("[+] CSRF tokens rotate correctly.")
    else:
        print("[!] CSRF token does not change — potential reuse issue.")

def test_session_fixation(driver, login_url, domain, fake_session_id):
    print("[*] Testing Session Fixation...")
    driver.get(login_url)
    driver.delete_all_cookies()
    try:
        driver.add_cookie({
            "name": "pwned_labs_session",
            "value": fake_session_id,
            "domain": domain,
            "path": "/",
            "secure": True,
            "httpOnly": False
        })
    except Exception as e:
        print(f"[!] Failed to add cookie: {e}")
        return

    driver.get(login_url)
    time.sleep(1)

    # Attempt a fake login - adjust selectors if necessary
    try:
        driver.find_element(By.NAME, "email").send_keys("fake@evil.com")
        driver.find_element(By.NAME, "password").send_keys("anything123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        cookies = driver.get_cookies()
        new_sid = [c for c in cookies if c["name"] == "pwned_labs_session"]
        if new_sid and new_sid[0]["value"] == fake_session_id:
            print("[!] Session Fixation Possible — session ID persisted after login!")
        else:
            print("[+] Session fixation mitigated — session regenerated after login.")
    except Exception as e:
        print(f"[-] Could not simulate login: {e}")

# ----- MAIN FLOW -----

def main():
    parser = argparse.ArgumentParser(description="Cookie Injection & Web Security Test Tool")
    parser.add_argument("--target-url", required=True, help="Target URL (e.g., user profile page)")
    parser.add_argument("--login-url", required=True, help="Login URL for testing CSRF and fixation")
    parser.add_argument("--cookie-file", required=True, help="Path to JSON cookie file")
    parser.add_argument("--domain", required=True, help="Domain for setting cookies (e.g., pwnedlabs.io)")
    parser.add_argument("--fake-session-id", default="evilSession12345", help="Fake session ID for session fixation test")
    args = parser.parse_args()

    driver = init_driver()
    try:
        print("\n=== Phase 1 & 2: Cookie Injection & Session Replay ===")
        cookies = load_cookies_from_file(args.cookie_file)
        inject_cookies(driver, args.target_url, cookies, args.domain)
        check_session_validity(driver)

        print("\n=== Phase 3: CSRF Token Change Detection ===")
        test_csrf_token_change(driver, args.login_url)

        print("\n=== Phase 4: Session Fixation Test ===")
        test_session_fixation(driver, args.login_url, args.domain, args.fake_session_id)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
