import requests
import socket
import json
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

def getInfo(ipAddress):
    url = f"https://ipapi.co/{ipAddress}/json/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "IP": data.get("ip"),
            "Version": "IPv4" if "." in ipAddress else "IPv6",
            "City": data.get("city"),
            "Region": data.get("region"),
            "Region Code": data.get("region_code"),
            "Country": data.get("country_name"),
            "Country Code": data.get("country_code"),
            "Continent": data.get("continent_code"),
            "Postal Code": data.get("postal"),
            "Latitude": data.get("latitude"),
            "Longitude": data.get("longitude"),
            "Timezone": data.get("timezone"),
            "UTC Offset": data.get("utc_offset"),
            "Country Calling Code": data.get("country_calling_code"),
            "Currency": data.get("accurrency"),
            "Languages": data.get("languages"),
            "ASN": data.get("asn"),
            "ISP": data.get("org")
        }
    except requests.RequestException as e:
        print(f"[ ipWise ] : {Fore.RED}Error fetching IP information: {e}")
        return None

def reverseDNS(ipAddress):
    try:
        return socket.gethostbyaddr(ipAddress)[0]
    except socket.herror:
        return f"[ ipWise ] : {Fore.YELLOW}No reverse DNS record found"

def isPrivateIP(ipAddress):
    segmn = ipAddress.split('.')
    if len(segmn) != 4:
        return False
    return (
        segmn[0] == '10' or
        (segmn[0] == '172' and 16 <= int(segmn[1]) <= 31) or
        (segmn[0] == '192' and segmn[1] == '168')
    )

def mainWorker():
    while True:
        ipAddress = input(f"[ ipWise ] : {Fore.GREEN}Enter an IP address :: ")
        if ipAddress.lower() == 'quit':
            print(f"[ ipWise ] : {Fore.YELLOW} Program Ended.")
            break
        
        if not ipAddress:
            print(f"[ ipWise ] : {Fore.YELLOW}Please enter a valid IP address.")
            continue
        
        if isPrivateIP(ipAddress):
            print(f"\n[ ipWise ] : {Fore.RED}{ipAddress} is a private IP. Unable to get info.")
            continue

        ipInfo = getInfo(ipAddress)
        revDNS = reverseDNS(ipAddress)
        if ipInfo:
            print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} *IP Information* ")
            for key, value in ipInfo.items():
                print(f"{Fore.CYAN}{key}: {Fore.WHITE}{value}")
            print(f"{Fore.MAGENTA}Reverse DNS: {Fore.WHITE}{revDNS}")
            print(f"{Fore.YELLOW}Timestamp: {Fore.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            filename = f"ipInfo_{ipAddress.replace('.', '_')}.json"
            with open(filename, 'w') as f:
                json.dump(ipInfo, f, indent=4)
            print(f"\n[ ipWise ] : {Fore.GREEN}following info saved at {Fore.WHITE}{filename}")
        else:
            print(f"[ ipWise ] : {Fore.RED}can't get info about the IP provided, please check if it is valid.")

if __name__ == "__main__":
    try:
        mainWorker()
    except Exception as e:
        print(f"{Fore.RED} error occurred: {e}")
