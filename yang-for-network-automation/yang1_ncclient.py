from ncclient import manager
from xml.dom.minidom import parseString

DEVICE = {
    "host": "10.0.0.29",
    "port": 830,
    "username": "dylan",
    "password": "password1",
    "hostkey_verify": False
}
XPATH_FILTER = "/native"

SUBTREE_FILTER = '''
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
      <description/>
    </interface>
  </interfaces>
'''

def main():
    with manager.connect(**DEVICE) as m:
        response = m.get(("xpath", XPATH_FILTER))
        pretty_xml = parseString(response.xml).toprettyxml()
        print(pretty_xml)

if __name__ == "__main__":
    main()
