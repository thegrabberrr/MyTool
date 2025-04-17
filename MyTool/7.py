import requests

# Sites connus avec format d'URL pour vérifier le pseudo
SITES = {
    "Instagram": "https://www.instagram.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Facebook": "https://www.facebook.com/{}",
    "YouTube": "https://www.youtube.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Medium": "https://medium.com/@{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Xbox": "https://account.xbox.com/en-us/Profile?gamertag={}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Pornhub": "https://www.pornhub.com/users/{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def check_username(username):
    print(f"\n🔍 Searching for username: {username}\n")
    for site, url in SITES.items():
        profile_url = url.format(username)
        try:
            response = requests.get(profile_url, headers=HEADERS, timeout=5)
            if response.status_code == 200:
                print(f"✅ {site}: Found → {profile_url}")
            elif response.status_code == 404:
                print(f"❌ {site}: Not found")
            else:
                print(f"❓ {site}: Status code {response.status_code}")
        except Exception as e:
            print(f"⚠️ {site}: Error → {e}")

# === Lancement ===
if __name__ == "__main__":
    username = input("Phone Number Lookup Account:").strip()
    if username != "":
        check_username(username)
    else:
        print("❌ No username entered. Returning to menu.")

    input("\n🔁 Press Enter to return to the main menu...")
