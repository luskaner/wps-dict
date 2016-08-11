# wps-dict
Wps-dict is an utility to dynamically generate pins based on the BSSID, ESSID and serial passed into the application based on a highly modular architecture, that allows providers to _provide_ the pins and hints to which tool to run and, of course, the tools themselves.

## Tools included
- [Belkin pingen](https://github.com/devttys0/wps/blob/master/pingens/belkin/pingen.c)
- [Dlink pingen](https://github.com/devttys0/wps/blob/master/pingens/dlink/pingen.py)
- [ComputePin](https://www.wifi-libre.com/topic-9-algoritmo-computepin-c83a35-de-zaochunsheng-la-brecha-en-la-brecha.html)
- [Easybox WPS](https://www.sec-consult.com/fxdata/seccons/prod/temedia/advisories_txt/20130805-0_Vodafone_EasyBox_Default_WPS_PIN_Vulnerability_v10.txt)
- [FTE_Keygen](https://github.com/0x90/wps-scripts/blob/master/goyscript/software/WPSPinGeneratorMOD)
- [Trendnet WPS](https://github.com/kcdtv/tdn/blob/master/tdn.sh)

## Providers included
- Application Builtin
- [Download Wireless Net](http://www.downloadwireless.net/scripts-live/patrones_conocidos.txt)
- [GoyScript](https://raw.githubusercontent.com/0x90/wps-scripts/master/goyscript/software/PINs.goy)
- [WPS Bunker](http://wpsbunker.hackaffeine.com/download_wps_db.php)
- [WPS DB](http://wpsdb.site40.net)

## Dependencies
- Python 3+
- Python package `netaddr` (_installable via `pip3`_)
- Python package `pyquery` (_installable via `pip3`_)

_Note: Wifislax 4.12 and Kali linux Rolling scripts to install dependencies [here](https://github.com/luskaner/wps-dict/tree/master/dependencies)_

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
                             [--include-providers [PROVIDER [PROVIDER ...]] |
                             --exclude-providers [PROVIDER [PROVIDER ...]]]

optional arguments:
  -h, --help            show this help message and exit
  --include-providers [PROVIDER [PROVIDER ...]]
                        Specify the provider(s) to get the info from or "all" to use them all:
                        Available providers: builtin, goy_script, download_wireless_net, wps_bunker
                        Default: "all"
  --exclude-providers [PROVIDER [PROVIDER ...]]
                        Specify the provider(s) to NOT get the info from or "none" to use them all:
                        Available providers: builtin, goy_script, download_wireless_net, wps_bunker
                        Default: "none"
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
                        Specify the tools(s) to generate the pins from, "all" to use all tools or, "none" to NOT
                        use any tools or "auto" to use them depending on the providers:
                        Available tools: dlink_pingen, fte_keygen, trendnetwps, belkin_pingen, easybox, computepin
                        Default: "smart" (chooses the tools to include depending on the bssid, essid and serial)
  --exclude-tools [TOOL [TOOL ...]]
                        Specify the tools(s) to generate the pins from, "all" to NOT use any tools, "none" to use
                        all tools or "auto" to use them depending on the providers
                        Available tools: dlink_pingen, fte_keygen, trendnetwps, belkin_pingen, easybox, computepin
                        Default: "smart" (chooses the tools to exclude depending on the bssid, essid and serial)
  --include-providers [PROVIDER [PROVIDER ...]]
                        Specify the provider(s) to get the info from, "all" to use them all or "none" to NOT any providers:
                        Available providers: builtin, goy_script, download_wireless_net, wps_bunker, wps_db
                        Default: "all"
  --exclude-providers [PROVIDER [PROVIDER ...]]
                        Specify the provider(s) to NOT get the info from or, "all" to NOT use any provider or "none" to use them all:
                        Available providers: builtin, goy_script, download_wireless_net, wps_bunker, wps_db
                        Default: "none"
```
