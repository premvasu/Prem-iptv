import requests
import re

# உங்கள் Google Drive டைரக்ட் டவுன்லோட் லிங்க்
MASTER_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1Cb5xTE7PmtGaNqL71VBxGuTRfgaLg1iM"

# ஆட்டோ அப்டேட் சேனல்கள் வரும் இடம்
AUTO_SOURCE = "https://github.com/alex4528x/m3u/raw/refs/heads/main/jtv.m3u"

# நீங்கள் ஆட்டோ அப்டேட் செய்ய விரும்பும் 20 சேனல்கள்
TARGET_CHANNELS = [
    "Sun TV", "Vijay TV", "Zee Tamil", "KTV", "Sun Music", 
    "Adithya TV", "Jaya TV", "Kalaignar TV", "Raj TV", "Sun News",
    "News7 Tamil", "Polimer News", "Puthiya Thalaimurai", "Star Sports 1 Tamil",
    "Sony Sports Ten 1", "Disney Channel", "Nick Tamil", "Discovery Tamil",
    "National Geographic Tamil", "Animal Planet Tamil"
]

def get_auto_channels():
    auto_list = []
    try:
        resp = requests.get(AUTO_SOURCE)
        lines = resp.text.splitlines()
        temp_tags = []
        for line in lines:
            if line.startswith("#EXTINF"):
                temp_tags = [line]
            elif line.startswith("#KODIPROP"):
                temp_tags.append(line)
            elif line.startswith("http"):
                if any(name.lower() in str(temp_tags).lower() for name in TARGET_CHANNELS):
                    cookie_match = re.search(r"cookie=(.*)", line)
                    if cookie_match:
                        cookie_val = cookie_match.group(1).replace("%7C", "|")
                        auto_list.append('#EXTHTTP:{"Cookie":"' + cookie_val + '"}')
                    auto_list.extend(temp_tags)
                    auto_list.append(line.split("?")[0])
                temp_tags = []
    except: pass
    return auto_list

def merge_playlists():
    try:
        # 1. கூகுள் டிரைவில் உள்ள உங்கள் 100 சேனல்களை எடுக்கிறது
        master_resp = requests.get(MASTER_DRIVE_URL)
        master_content = master_resp.text
        
        # 2. GitHub மூலம் ஆட்டோ அப்டேட் சேனல்களை எடுக்கிறது
        auto_channels = get_auto_channels()
        auto_content = "\n".join(auto_channels)
        
        # 3. இரண்டையும் இணைக்கிறது
        # உங்கள் டிரைவ் கோப்பில் ஏற்கனவே #EXTM3U இருந்தால் அதைச் சரிசெய்கிறது
        if master_content.startswith("#EXTM3U"):
            final_playlist = master_content + "\n\n" + auto_content
        else:
            final_playlist = "#EXTM3U\n" + master_content + "\n\n" + auto_content
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_playlist)
        print("Merge Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    merge_playlists()
    
