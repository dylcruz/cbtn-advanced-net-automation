from scrapli import AuthOptions, Netconf, TransportOptions, TransportSsh2Options
import xmltodict

def main():
    n = Netconf(
        host='10.0.0.15',
        auth_options=AuthOptions(
            username='dylan',
            password='cisco'
        ),
        transport_options=TransportOptions(ssh2=TransportSsh2Options()),
    )

    n.open()
    response = n.get_config(source='running')
    n.close()
    
    response_dict = xmltodict.parse(response.result)
    ospf_rid = response_dict['rpc-reply']['data']['native']['router']['router-ospf']['ospf']['process-id']['router-id']
    print(f'The router-id for R1 is "{ospf_rid}"')

if __name__ == '__main__':
    main()
