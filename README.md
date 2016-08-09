# wps-dict
Wps-dict is an utility to dynamically generate pins based on the BSSID, ESSID and serial passed into the application based on a highly modular architecture, that allows providers to _provide_ the pins and hints to which tool to run and, of course, the tools themselves.

## Tools included
- Belkin pingen
- Dlink pingen
- ComputePin
- Easybox WPS
- FTE_Keygen
- Trendnet WPS

## Providers included
- Builtin
- Download Wireless Net
- GoyScript
- WPS Bunker
- WPS DB

## Builtin Help
### Main section
```
usage: wps-dict.py [-h] {generate,update_db} ...

positional arguments:
  {generate,update_db}

optional arguments:
  -h, --help            show this help message and exit
```
### Update database section
```
usage: wps-dict.py update_db [-h]

optional arguments:
  -h, --help  show this help message and exit
```
### Generate dictionary section
```
usage: wps-dict.py generate [-h] [-e ESSID] [-s SERIAL]
                            [--include-tools [TOOL [TOOL ...]] |
                            --exclude-tools [TOOL [TOOL ...]]]
                            [--include-providers [PROVIDER [PROVIDER ...]] |
                            --exclude-providers [PROVIDER [PROVIDER ...]]]
                            bssid

positional arguments:
  bssid                 BSSID in MAC address format
                        (see https://pythonhosted.org/netaddr/tutorial_02.html#formatting for supported formats)

optional arguments:
  -h, --help            show this help message and exit
  -e ESSID, --essid ESSID
  -s SERIAL, --serial SERIAL
  --include-tools [TOOL [TOOL ...]]
                        Specify the tools(s) to generate the pins from or, "all" to use all tools:
                        Available tools: computepin, trendnetwps, belkin_pingen, easybox, fte_keygen, dlink_pingen
                        Default: "smart" (chooses the tools to include depending on the bssid, essid and serial)
  --exclude-tools [TOOL [TOOL ...]]
                        Specify the tools(s) to exclude generating the pins from or, "none" to use all tools:
                        Available tools: computepin, trendnetwps, belkin_pingen, easybox, fte_keygen, dlink_pingen
                        Default: "smart" (chooses the tools to exclude depending on the bssid, essid and serial)
  --include-providers [PROVIDER [PROVIDER ...]]
                        Specify the provider(s) to get the pins or info from or, "none" to not use providers:
                        Available providers: builtin, wps_db, wps_bunker, download_wireless_net, goy_script
                        Default: "all"
  --exclude-providers [PROVIDER [PROVIDER ...]]
                        Specify the provider(s) to NOT get the pins or info from or, "all" to not use any provider:
                        Available providers: builtin, wps_db, wps_bunker, download_wireless_net, goy_script
                        Default: "none"
```
