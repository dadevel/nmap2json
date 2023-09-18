# nmap2json

Convert [nmap](https://nmap.org/) XML to JSONL 

# Setup

Install the Python package with [pipx](https://github.com/pypa/pipx).

~~~ bash
pipx install git+https://github.com/dadevel/nmap2json.git@main
~~~

# Usage

Example: Extract web servers.

~~~ bash
nmap2json ./*.xml | jq -r 'select(.application=="http")|"\(.address):\(.port)"'
~~~
