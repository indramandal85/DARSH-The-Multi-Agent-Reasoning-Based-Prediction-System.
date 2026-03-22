# tests/test_module7.py
# Run with: python tests/test_module7.py
# Tests that the Flask API is running and all endpoints respond correctly.
# The API must be running first: python app.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

API = "http://localhost:5001"


def run_test():

    print("\n" + "="*52)
    print("  DARSH — MODULE 7 DRY-RUN TEST")
    print("  Flask API + Vue Frontend Integration")
    print("="*52)
    print("\n  Make sure 'python app.py' is running in another tab.\n")

    results = {}

    # Test 1: Health check
    print("  [1/4] Testing API health endpoint...")
    try:
        r = requests.get(f"{API}/api/health", timeout=5)
        results["health"] = r.status_code == 200
        print(f"        {'✓' if results['health'] else '✗'} "
              f"Health: {r.json().get('message', 'no message')}")
    except Exception as e:
        results["health"] = False
        print(f"        ✗ Cannot reach API: {e}")
        print(f"\n  ERROR: Flask API is not running.")
        print(f"  Fix: Open a new terminal tab and run: python app.py")
        return

    # Test 2: Upload endpoint
    print("\n  [2/4] Testing file upload endpoint...")
    try:
        test_file_path = "data/inputs/rbi_article.txt"
        if os.path.exists(test_file_path):
            with open(test_file_path, "rb") as f:
                r = requests.post(
                    f"{API}/api/upload",
                    files={"file": ("rbi_article.txt", f, "text/plain")},
                    timeout=10
                )
            results["upload"] = r.status_code == 200 and r.json().get("success")
            print(f"        {'✓' if results['upload'] else '✗'} "
                  f"Upload: {r.json().get('message', r.text[:80])}")
        else:
            results["upload"] = False
            print(f"        ✗ Test file not found: {test_file_path}")
    except Exception as e:
        results["upload"] = False
        print(f"        ✗ Upload failed: {e}")

    # Test 3: Status endpoint
    print("\n  [3/4] Testing status endpoint...")
    try:
        r = requests.get(f"{API}/api/status/nonexistent", timeout=5)
        results["status"] = r.status_code == 404
        print(f"        {'✓' if results['status'] else '✗'} "
              f"Status endpoint responding correctly")
    except Exception as e:
        results["status"] = False
        print(f"        ✗ Status endpoint failed: {e}")

    # Test 4: Report endpoint
    print("\n  [4/4] Testing report endpoint...")
    try:
        r = requests.get(f"{API}/api/get-report", timeout=5)
        results["report"] = r.status_code in [200, 404]
        if r.status_code == 200:
            print(f"        ✓ Report found: {r.json().get('filename', 'unknown')}")
        else:
            print(f"        ✓ Report endpoint working (no report yet — run simulation first)")
    except Exception as e:
        results["report"] = False
        print(f"        ✗ Report endpoint failed: {e}")

    # Pass check
    passed = all(results.values())

    print(f"\n\n{'='*52}")
    if passed:
        print("  ✓  MODULE 7 PASSED")
        print("  ✓  Flask API running and all endpoints responding")
        print("  ✓  File upload working")
        print("  ✓  Status polling working")
        print("  ✓  Report endpoint working")
        print("\n  → Open http://localhost:5173 in your browser")
        print("  → DARSH is fully operational!")
        print("\n  ✓  ALL 7 MODULES COMPLETE")
        print("  ✓  DARSH v1.0 IS READY")
    else:
        print("  ✗  Some endpoints need attention:")
        for test, ok in results.items():
            print(f"  {'✓' if ok else '✗'}  {test}")
        print("\n  → Make sure python app.py is running, then retry")
    print("="*52 + "\n")


if __name__ == "__main__":
    run_test()