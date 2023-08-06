import requests

def get_proxy(timeout: int, country: str, protocol: str):
    """
    :param timeout int: ping of proxies
    :param country string: country of proxy (all, ua, uk, etc.)
    :param protocol string: protocol (http, socks4, socks5)
    """

    proxy = requests.get(f'https://api.proxyscrape.com/v2/?request=getproxies&protocol={str(protocol)}&timeout={str(timeout)}&country={country}&ssl=all&anonymity=all').text.split('\n')

    proxies = []

    for p in proxy:
        proxies.append(p.replace('\r',''))
    
    proxies = proxies[:-1]

    return proxies

print('PyProxy initialized!')