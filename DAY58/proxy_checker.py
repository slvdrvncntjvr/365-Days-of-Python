import requests
import concurrent.futures
import time
import random
import os

TARGET_URL = "http://httpbin.org/ip"
TIMEOUT = 5

def load_proxies(file_path="proxies.txt"):
    if not os.path.exists(file_path):
        print(f"Proxy file '{file_path}' not found. Please create one with proxy addresses.")
        return []
    with open(file_path, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

def check_proxy(proxy, target_url=TARGET_URL, timeout=TIMEOUT):
    proxies_dict = {"http": proxy, "https": proxy}
    start_time = time.time()
    try:
        response = requests.get(target_url, proxies=proxies_dict, timeout=timeout)
        if response.status_code == 200:
            elapsed = time.time() - start_time
            return proxy, elapsed
    except Exception:
        return None

def check_all_proxies(proxies):
    working = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            result = future.result()
            if result:
                working.append(result)
    return working

def rotate_proxy(working_proxies):
    if not working_proxies:
        return None
    return random.choice(working_proxies)[0]

def main():
    proxies = load_proxies()
    if not proxies:
        print("No proxies to test.")
        return

    print("Testing proxies...")
    working_proxies = check_all_proxies(proxies)
    if not working_proxies:
        print("No working proxies found.")
        return

    working_proxies.sort(key=lambda x: x[1])
    print("\nWorking Proxies (sorted by response time):")
    for proxy, elapsed in working_proxies:
        print(f"{proxy} - {elapsed:.2f} seconds")

    chosen = rotate_proxy(working_proxies)
    print(f"\nRotated Proxy: {chosen}")

if __name__ == "__main__":
    main()
