import requests
import re

# உங்களுக்கு வேண்டிய 20 சேனல் பெயர்கள்
TARGET_CHANNELS = [
    "Sun TV", "Vijay TV", "Zee Tamil", "KTV", "Sun Music", 
    "Adithya TV", "Jaya TV", "Kalaignar TV", "Raj TV", "Sun News",
    "News7 Tamil", "Polimer News", "Puthiya Thalaimurai", "Star Sports 1 Tamil",
    "Sony Sports Ten 1", "Disney Channel", "Nick Tamil", "Discovery Tamil",
    "National Geographic Tamil", "Animal Planet Tamil"
]

SOURCE_URL = "https://github.com/alex4528x/m3u/raw/refs/heads/main/jtv.m3u"

def update_list():
    try:
        response = requests.get(SOURCE_URL)
        lines = response.text.splitlines()
        
        new_m3u = ["#EXTM3U"]
        temp_tags = []
        
        for line in lines:
            if line.startswith("#EXTINF"):
                temp_tags = [line]
            elif line.startswith("#KODIPROP"):
                temp_tags.append(line)
            elif line.startswith("http"):
                # நமது லிஸ்டில் உள்ள சேனலா என்று பார்க்கிறோம்
                if any(name.lower() in str(temp_tags).lower() for name in TARGET_CHANNELS):
                    
                    # URL-ல் இருந்து குக்கீஸை மட்டும் பிரிக்கிறோம்
                    # இதற்காக ஒரு 'Regular Expression' பயன்படுத்துகிறோம்
                    cookie_match = re.search(r"cookie=(.*)", line)
                    
                    if cookie_match:
                        cookie_val = cookie_match.group(1)
                        # URL-ல் இருக்கும் %7C போன்றவற்றை | ஆக மாற்றுகிறோம்
                        cookie_val = cookie_val.replace("%7C", "|")
                        
                        # நீங்கள் கேட்ட அந்த #EXTHTTP வரியை இங்கே உருவாக்குகிறோம்
                        http_header = '#EXTHTTP:{"Cookie":"' + cookie_val + '"}'
                        new_m3u.append(http_header)
                        
                        # மெயின் லிங்க்கில் இருந்து குக்கீஸ் பகுதியை நீக்கிவிட்டு சுத்தமான URL-ஐ மட்டும் எடுக்கிறோம்
                        clean_url = line.split("?")[0]
                        
                        new_m3u.extend(temp_tags)
                        new_m3u.append(clean_url)
                temp_tags = []

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_m3u))
        print("Success: Playlist created with EXTHTTP headers!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_list()
    
