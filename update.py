import requests

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
            elif line.startswith("#KODIPROP") or line.startswith("#EXTVLCOPT"):
                # DRM மற்றும் இதர டேக்குகளை சேர்க்கிறது
                temp_tags.append(line)
            elif line.startswith("http"):
                # சேனல் நமது லிஸ்டில் இருக்கிறதா என்று பார்க்கிறோம்
                if any(name.lower() in str(temp_tags).lower() for name in TARGET_CHANNELS):
                    # இங்கே தான் முக்கிய மாற்றம்: 
                    # %7C என்பதை | என மாற்றுகிறோம் (Replace)
                    clean_link = line.replace("%7C", "|")
                    
                    new_m3u.extend(temp_tags)
                    new_m3u.append(clean_link)
                temp_tags = []

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_m3u))
        print("Playlist updated with fixed symbols!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_list()
    
