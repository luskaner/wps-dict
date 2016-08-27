# wps-dict
Wps-dict is an utility to dynamically generate pins based on the BSSID, ESSID and serial passed into the application based on a highly modular architecture, that allows providers to _provide_ the pins and hints to which tool to run and, of course, the tools themselves.

Wps-dict includes both a CLI version named `wps-dict-cli.py` and a GUI GTK 3 version named `wps-dict-gui.py`

## Installing requirements
### Pre-requirements
* Python 3.1 _or higher_

### Requirements
Install them by running `make` or `make debian`
_Note: for more in-depth info see the [requirements page](Requirements)_

## Tools included
- [Belkin pingen](https://github.com/devttys0/wps/blob/master/pingens/belkin/pingen.c)
- [Dlink pingen](https://github.com/devttys0/wps/blob/master/pingens/dlink/pingen.py)
- [ComputePin](https://www.wifi-libre.com/topic-9-algoritmo-computepin-c83a35-de-zaochunsheng-la-brecha-en-la-brecha.html)
- [Easybox WPS](https://www.sec-consult.com/fxdata/seccons/prod/temedia/advisories_txt/20130805-0_Vodafone_EasyBox_Default_WPS_PIN_Vulnerability_v10.txt)
- [FTE_Keygen](https://github.com/0x90/wps-scripts/blob/master/goyscript/software/WPSPinGeneratorMOD)
- [Trendnet WPS](https://github.com/kcdtv/tdn/blob/master/tdn.sh)

## Providers included
- [Application Builtin](https://github.com/luskaner/wps-dict/blob/master/wps-dict/providers/offline/builtin.py)
- [Download Wireless Net](http://www.downloadwireless.net/scripts-live/patrones_conocidos.txt)
- [GoyScript](https://raw.githubusercontent.com/0x90/wps-scripts/master/goyscript/software/PINs.goy)
- [WPS Bunker](http://wpsbunker.hackaffeine.com/download_wps_db.php)
- [WPS DB](http://wpsdb.site40.net)
