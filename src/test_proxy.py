import requests

proxies = {
    'https': f'http://crawler-gost-proxy.jobright-internal.com:8083'
}

url = 'https://ipinfo.io/ip'

for i in range(10):
    try:
        response = requests.get(url, proxies=proxies)

        ip = response.text.strip()

        print(f'Your IP: {ip}')

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
