def is_ipv4(ipstr):
    import ipaddress
    try:
        ipaddress.IPv4Network(ipstr)
        return True
    except ValueError:
        return False
