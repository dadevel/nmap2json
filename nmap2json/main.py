from xml.etree import ElementTree
import json
import sys

from nmap2json.model import Host


def main() -> int:
    try:
        for path in sys.argv[1:]:
            with open(path) as file:
                for event, element in ElementTree.iterparse(file, events=['start', 'end']):
                    if element.tag == 'nmaprun' and event == 'start':
                        if not element.attrib.get('xmloutputversion', '').startswith('1.'):
                            print('parser error: unsupported xml schema version', file=sys.stderr)
                            return 1
                    elif element.tag == 'host' and event == 'end':
                        host = Host.from_xml(element)
                        print_json(host)
        return 0
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}', file=sys.stderr)
        return 1


def print_json(host: Host):
    for port in host.ports.values():
        host_attrs = {k: v for k, v in host.__dict__.items() if k != 'ports'}  # remove ports attribute
        port_attrs = {'port' if k == 'number' else k: v for k, v in port.__dict__.items()}  # rename number to port
        print(json.dumps(host_attrs | port_attrs, indent=None, sort_keys=False, separators=(',', ':')))


if __name__ == '__main__':
    exit(main())
