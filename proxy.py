import requests

proxy = {
    'http': 'http://PGHRL:prajwal2003@in.proxymesh.com:31280'
}

try:
    response = requests.get('http://example.com', proxies=proxy, timeout=10)
    print(response.status_code)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

