import requests

def ip_lookup(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data['status'] == 'success':
            print("\n\033[1m🔍 IP Lookup Result:\033[0m")
            print(f"  IP       : {data.get('query')}")
            print(f"  Country  : {data.get('country')} ({data.get('countryCode')})")
            print(f"  Region   : {data.get('regionName')}")
            print(f"  City     : {data.get('city')}")
            print(f"  Zip      : {data.get('zip')}")
            print(f"  Lat/Lon  : {data.get('lat')}, {data.get('lon')}")
            print(f"  ISP      : {data.get('isp')}")
            print(f"  Org      : {data.get('org')}")
            print(f"  Timezone : {data.get('timezone')}")
        else:
            print("\033[91m❌ Error:\033[0m IP not found or invalid.")
    except Exception as e:
        print(f"\033[91m❌ Exception occurred:\033[0m {e}")

def main():
    print("\n\033[94m--- IP Lookup Tool ---\033[0m")
    print("Enter a valid *public* IPv4 address")
    
    ip = input("Enter an IP address: ").strip()
    if ip:
        ip_lookup(ip)
    else:
        print("No input provided.")

    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()
