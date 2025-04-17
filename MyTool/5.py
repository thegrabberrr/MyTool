import socket
from urllib.parse import urlparse

def extract_hostname(url):
    parsed_url = urlparse(url)
    if not parsed_url.netloc:
        # Si l'URL n'a pas http://, on l'ajoute
        parsed_url = urlparse("https://" + url)
    return parsed_url.netloc

def get_ip_from_url(url):
    try:
        hostname = extract_hostname(url)
        ip_address = socket.gethostbyname(hostname)
        print(f"\n🌐 URL       : {url}")
        print(f"🔎 Hostname  : {hostname}")
        print(f"📍 IP Address: {ip_address}")
    except Exception as e:
        print(f"\n❌ Error resolving {url}: {e}")

def main():
    print("\n\033[94m--- IP Lookup from Website ---\033[0m")
    print("🔹 Enter the URL of a website (e.g. example.com or https://example.com)\n")
    
    url = input("Enter a URL: ").strip()
    if url:
        get_ip_from_url(url)
    else:
        print("No URL entered.")

    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()
