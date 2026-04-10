import requests
import re

# உங்கள் Google Drive டைரக்ட் டவுன்லோட் லிங்க்
MASTER_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1Cb5xTE7PmtGaNqL71VBxGuTRfgaLg1iM"

# ஆட்டோ அப்டேட் சேனல்கள் வரும் இடம்
AUTO_SOURCE = "https://github.com/alex4528x/m3u/raw/refs/heads/main/jtv.m3u"

# --- இங்கே உங்கள் விருப்பப்படி வரிசைப்படுத்துங்கள் ---
# நீங்கள் முதலில் எந்தப் பெயரை வைக்கிறீர்களோ அதுவே பிளேயரில் முதலில் வரும்
TARGET_CHANNELS = [
    "star sports 1 tamil hd",
    "star sports 2 tamil hd",
    "zee thirai hd", 
    "star Vijay hd", 
    "Vijay Super HD",
    "Zee Tamil hd",
    "vijay takkar"
    "Colors Tamil HD",
    "Jaya TV hd", 
    "Kalaignar TV", 
    "Raj TV", 
    "News7 Tamil", 
    "News J", 
    "Puthiya Thalimurai", 
]

def get_auto_channels():
    # ஒரு அகராதியை (Dictionary) உருவாக்கி சேனல்களை அதில் சேமிப்போம்
    found_channels = {}
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
                # இந்த சேனல் நமது TARGET_CHANNELS பட்டியலில் இருக்கிறதா என்று பார்க்கிறோம்
                for target_name in TARGET_CHANNELS:
                    if target_name.lower() in str(temp_tags).lower():
                        channel_data = []
                        cookie_match = re.search(r"cookie=(.*)", line)
                        if cookie_match:
                            cookie_val = cookie_match.group(1).replace("%7C", "|")
                            channel_data.append('#EXTHTTP:{"Cookie":"' + cookie_val + '"}')
                        
                        channel_data.extend(temp_tags)
                        clean_url = line.split("?")[0].replace("%7C", "|")
                        channel_data.append(clean_url)
                        
                        # சேனல் பெயரை கீ-யாக வைத்து தகவல்களைச் சேமிக்கிறோம்
                        found_channels[target_name] = "\n".join(channel_data)
                temp_tags = []
    except: pass

    # இப்போது நாம் கொடுத்த TARGET_CHANNELS வரிசைப்படி லிஸ்ட்டை உருவாக்குகிறோம்
    ordered_list = []
    for name in TARGET_CHANNELS:
        if name in found_channels:
            ordered_list.append(found_channels[name])
    
    return ordered_list

def merge_playlists():
    try:
        # 1. ஆட்டோ அப்டேட் சேனல்களை நாம் சொன்ன வரிசையில் எடுக்கிறது
        auto_channels = get_auto_channels()
        auto_content = "\n\n".join(auto_channels)
        
        # 2. கூகுள் டிரைவ் மாஸ்டர் லிஸ்ட்டை எடுக்கிறது
        master_resp = requests.get(MASTER_DRIVE_URL)
        master_content = master_resp.text
        master_lines = master_content.splitlines()
        
        if master_lines and master_lines[0].startswith("#EXTM3U"):
            master_body = "\n".join(master_lines[1:])
        else:
            master_body = master_content

        # 3. இரண்டையும் இணைக்கிறது (முதலில் ஆட்டோ, பிறகு மாஸ்டர்)
        final_playlist = "#EXTM3U\n\n" + auto_content + "\n\n" + master_body
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_playlist)
        print("Success: Channels ordered exactly as requested!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    merge_playlists()
    
