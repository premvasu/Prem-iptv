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
            elif line.startswith("#KODIPROP") or line.startswith("#EXTVLCOPT"):
                temp_tags.append(line)
            elif line.startswith("http"):
                if any(name.lower() in str(temp_tags).lower() for name in TARGET_CHANNELS):
                    # URL-ல் இருந்து குக்கீஸை மட்டும் பிரிக்கிறோம்
                    cookie_match = re.search(r"cookie=(.*)", line)
                    if cookie_match:
                        cookie_val = cookie_match.group(1).replace("%7C", "|")
                        # Network Stream பிளேயருக்கான #EXTHTTP வரி
                        http_header = '#EXTHTTP:{"Cookie":"' + cookie_val + '"}'
                        auto_list.append(http_header)
                    
                    # Sparkle TV மற்றும் பிற பிளேயர்களுக்கான DRM/Tags
                    auto_list.extend(temp_tags)
                    # %7C என்பதை | ஆக மாற்றி சுத்தமான URL-ஐ மட்டும் எடுக்கிறோம்
                    clean_url = line.split("?")[0].replace("%7C", "|")
                    auto_list.append(clean_url)
                temp_tags = []
    except: pass
    return auto_list

def merge_playlists():
    try:
        # 1. GitHub மூலம் ஆட்டோ அப்டேட் சேனல்களை முதலில் எடுக்கிறது
        auto_channels = get_auto_channels()
        auto_content = "\n".join(auto_channels)
        
        # 2. கூகுள் டிரைவில் உள்ள உங்கள் 100 சேனல்களை எடுக்கிறது
        master_resp = requests.get(MASTER_DRIVE_URL)
        master_content = master_resp.text
        
        # உங்கள் டிரைவ் கோப்பில் இருக்கும் #EXTM3U வரியை நீக்கிவிட்டு சுத்தமான டேட்டாவை எடுக்கிறது
        master_lines = master_content.splitlines()
        if master_lines and master_lines[0].startswith("#EXTM3U"):
            master_body = "\n".join(master_lines[1:])
        else:
            master_body = master_content

        # 3. வரிசைப்படுத்துதல்: முதலில் ஆட்டோ அப்டேட், பிறகு உங்கள் 100 சேனல்கள்
        final_playlist = "#EXTM3U\n\n" + auto_content + "\n\n" + master_body
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_playlist)
        print("Success: Auto-channels first, followed by Master list!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    merge_playlists()
    
