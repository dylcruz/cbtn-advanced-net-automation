from ipaddress import ip_network, ip_address
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

target = input("Enter the target IP address: ")
ipaddr = ip_address(target)
route_list = []

cisco_filter = nr.filter(platform="ios")
junos_filter = nr.filter(platform="junos")


def get_routes_cisco(task):
    response = task.run(task=send_command, command="show ip route")
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for prefix in prefixes:
        net = ip_network(prefix)
        if ipaddr in net:
            source_proto = prefixes[prefix]["source_protocol"]
            if source_proto == "connected":
                try:
                    outgoing_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]
                    for intf in outgoing_intf:
                        exit_intf = intf
                        route_list.append(
                            f"{task.host} is connected to {target} via interface {exit_intf}"
                        )
                except KeyError:
                    pass
            else:
                try:
                    next_hop_list = prefixes[prefix]["next_hop"]["next_hop_list"]
                    for key in next_hop_list:
                        next_hop = next_hop_list[key]["next_hop"]
                        route_list.append(
                            f"{task.host} can reach {target} via next hop: {next_hop} ({source_proto})"
                        )
                except KeyError:
                    pass


def get_routes_junos(task):
    response = task.run(task=send_command, command="show route")
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    routes = task.host["facts"]["route-information"]["route-table"][0]["rt"]
    for route in routes:
        try:
            net = ip_network(route["rt-destination"])
            if ipaddr in net:
                source_proto = route["rt-entry"]["protocol-name"]
                if source_proto == "Direct":
                    next_hops = route["rt-entry"]["nh"]
                    for hop in next_hops:
                        outgoing_intf = hop["via"]
                        route_list.append(
                            f"{task.host} is connected to {target} via interface {outgoing_intf}"
                        )
                else:
                    next_hops = route["rt-entry"]["nh"]
                    for hop in next_hops:
                        print(hop)
                        hop_ip = hop["to"]
                        route_list.append(
                            f"{task.host} can reach {target} via next hop: {hop_ip} ({source_proto})"
                        )
        except KeyError:
            pass


results_cisco = cisco_filter.run(task=get_routes_cisco)
results_junos = junos_filter.run(task=get_routes_junos)

if route_list:
    for route in sorted(route_list):
        rprint(route)
else:
    print(f"Target address {target} not found on any devices in the inventory.")
