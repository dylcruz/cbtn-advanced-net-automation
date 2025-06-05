from ipaddress import ip_network, ip_address

target = input('Enter the target IP address: ')
ipaddr = ip_address(target)

ip_list = ['10.0.0.0/30', '10.0.0.4/30']
for prefix in ip_list:
    net = ip_network(prefix)
    if ipaddr in net:
        print(f'{ipaddr} is in the {net} network')
