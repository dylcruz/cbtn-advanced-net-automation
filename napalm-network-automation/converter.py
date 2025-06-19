import yaml

target_dict = { 'get_bgp_neighbors': { 'global': { 'peers': { '10.0.10.10': { 'address_family': { 'ipv4 unicast': { 'accepted_prefixes': 1,
                                                                                                      'received_prefixes': 1,
                                                                                                      'sent_prefixes': 1}},
                                                                'description': '',
                                                                'is_enabled': True,
                                                                'is_up': True,
                                                                'local_as': 65001,
                                                                'remote_as': 65001,
                                                                'remote_id': '3.3.3.3',
                                                                'uptime': 32982},
                                                '10.0.10.2': { 'address_family': { 'ipv4 unicast': { 'accepted_prefixes': 1,
                                                                                                     'received_prefixes': 1,
                                                                                                     'sent_prefixes': 1}},
                                                               'description': '',
                                                               'is_enabled': True,
                                                               'is_up': True,
                                                               'local_as': 65001,
                                                               'remote_as': 65001,
                                                               'remote_id': '2.2.2.2',
                                                               'uptime': 33270},
                                                '10.0.10.6': { 'address_family': { 'ipv4 unicast': { 'accepted_prefixes': 1,
                                                                                                     'received_prefixes': 1,
                                                                                                     'sent_prefixes': 1}},
                                                               'description': '',
                                                               'is_enabled': True,
                                                               'is_up': True,
                                                               'local_as': 65001,
                                                               'remote_as': 65001,
                                                               'remote_id': '4.4.4.4',
                                                               'uptime': 32838}},
                                     'router_id': '1.1.1.1'}}}

filename = 'validate-R1.yaml'
with open(filename, 'w') as file:
    output = yaml.dump(target_dict, file, default_flow_style=False)
