import requests
import os
import random
import string

# Configuration
TARGET_URL = "http://127.0.0.1:8000/polls/upload/"
# If you are redirected to login, we might need to handle that, 
# but for now we test the endpoint directly.

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_dummy_file(filename, size_bytes):
    with open(filename, 'wb') as f:
        f.write(os.urandom(size_bytes))

def run_fuzz_test():
    print(f"--- Starting Fuzzing Attack on {TARGET_URL} ---")
    
    # Test Case 1: Upload a standard safe file (Baseline)
    print("\n[1] Testing Valid File Upload...")
    files = {'file': ('test_safe.txt', 'This is a safe text file.')}
    try:
        # We need to get the CSRF token first if CSRF protection is active.
        # For a simple fuzzer, we often disable CSRF temporarily or fetch the token.
        # For this test, we will see if we get a 403 (CSRF Error) which IS a pass (security working!)
        response = requests.post(TARGET_URL, files=files)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200 or response.status_code == 302:
            print("Result: Handled gracefully.")
        elif response.status_code == 403:
            print("Result: PASSED (CSRF Protection is active).")
        else:
            print("Result: Unexpected status.")
    except Exception as e:
        print(f"Request failed: {e}")

    # Test Case 2: Massive File (Buffer Overflow Attempt)
    print("\n[2] Testing Massive File Name...")
    long_name = "A" * 5000 + ".txt"
    files = {'file': (long_name, 'content')}
    try:
        response = requests.post(TARGET_URL, files=files)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 500:
            print("Result: FAILED (Server Crashed).")
        else:
            print("Result: PASSED (Server rejected or handled it).")
    except Exception as e:
        print(f"Request failed: {e}")

    # Test Case 3: SQL Injection in Filename
    print("\n[3] Testing SQL Injection in Filename...")
    sql_name = "test'; DROP TABLE polls_uploadedfile; --.txt"
    files = {'file': (sql_name, 'content')}
    try:
        response = requests.post(TARGET_URL, files=files)
        print(f"Status Code: {response.status_code}")
        # Django automatically handles this, so we expect a 200/302/403, NOT a DB error.
        print("Result: Check your server logs. If no crash, Django protected the DB.")
    except Exception as e:
        print(f"Request failed: {e}")

    # Test Case 4: Empty Upload
    print("\n[4] Testing Empty Upload...")
    try:
        response = requests.post(TARGET_URL, data={})
        print(f"Status Code: {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")

    print("\n--- Fuzzing Complete ---")

if __name__ == "__main__":
    run_fuzz_test()
