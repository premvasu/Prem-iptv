import requests

# இதில் உங்களுக்கு வேண்டிய 20 சேனல் பெயர்களை மாற்றிக்கொள்ளலாம்
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
        keep = False
        for line in lines:
            if line.startswith("#EXTINF"):
                if any(name.lower() in line.lower() for name in TARGET_CHANNELS):
                    new_m3u.append(line)
                    keep = True
                else: keep = False
            elif line.startswith("http") and keep:
                new_m3u.append(line)
                keep = False
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_m3u))
    except: pass

if __name__ == "__main__":
    update_list()
  
