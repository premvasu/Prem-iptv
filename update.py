import requests
import re

# உங்கள் Google Drive டைரக்ட் டவுன்லோட் லிங்க்
MASTER_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1Cb5xTE7PmtGaNqL71VBxGuTRfgaLg1iM"

# புதிய மற்றும் உறுதியான சோர்ஸ் (இது ஸ்பார்க்கல் டிவியில் நன்றாக வேலை செய்யும்)
NEW_SOURCE = "https://raw.githubusercontent.com/Anshuman71/JioTV/main/jio.m3u"

TARGET_CHANNELS = [
    "Sun TV", "Vijay TV", "Zee Tamil", "KTV", "Sun Music", 
    "Adithya TV", "Sun News", "Star Sports 1 Tamil", "Sony Sports Ten 1",
    "Jaya TV", "Kalaignar TV", "Raj TV", "News7 Tamil", "Polimer News", 
    "Puthiya Thalaimurai", "Disney Channel", "Nick Tamil", "Discovery Tamil",
    "National Geographic Tamil", "Animal Planet Tamil"
]

def get_new_channels():
    found_channels = {}
    try:
        # புதிய சோர்ஸிலிருந்து தரவைப் பெறுகிறது
        resp = requests.get(NEW_SOURCE, timeout=15)
        lines = resp.text.splitlines()
        
        current_info = ""
        for line in lines:
            if line.startswith("#EXTINF"):
                current_info = line
            elif line.startswith("http"):
                for target in TARGET_CHANNELS:
                    # சேனல் பெயரைத் தேடுகிறது
                    if target.lower() in current_info.lower():
                        # ஸ்பார்க்கல் டிவிக்குத் தேவையான யூசர் ஏஜென்டை லிங்கிற்குப் பின்னால் இணைக்கிறது
                        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                        final_link = f"{line}|User-Agent={ua}&Origin=https://www.jiotv.com&Referer=https://www.jiotv.com/"
                        
                        found_channels[target] = f"{current_info}\n{final_link}"
                current_info = ""
    except Exception as e:
        print(f"Error fetching new source: {e}")
    
    return [found_channels[name] for name in TARGET_CHANNELS if name in found_channels]

def merge_playlists():
    try:
        # 1. புதிய சோர்ஸ் சேனல்கள்
        auto_content = "\n\n".join(get_new_channels())
        
        # 2. உங்கள் கூகுள் டிரைவ் மாஸ்டர் லிஸ்ட்
        master_resp = requests.get(MASTER_DRIVE_URL, timeout=15)
        master_content = master_resp.text
        master_lines = master_content.splitlines()
        
        # முதல் வரியான #EXTM3U ஐத் தவிர்த்து மற்றவற்றை எடுக்கிறது
        master_body = "\n".join(master_lines[1:]) if master_lines and master_lines[0].startswith("#EXTM3U") else master_content

        # 3. இரண்டையும் இணைத்தல்
        final_playlist = "#EXTM3U\n\n" + auto_content + "\n\n" + master_body
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_playlist)
        print("Master List Updated with New Source!")
    except Exception as e:
        print(f"Merge Error: {e}")

if __name__ == "__main__":
    merge_playlists()
    
