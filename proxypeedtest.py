import requests

proxy = {
    'http': 'http://PGHRL:prajwal2003@in.proxymesh.com:31280'
}

try:
    response = requests.get('https://twitter.com/login', proxies=proxy, timeout=10)
    print(f"Status Code: {response.status_code}, Response Time: {response.elapsed.total_seconds()}s")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
