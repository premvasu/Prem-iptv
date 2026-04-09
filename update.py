import requests
import re

# உங்கள் Google Drive டைரக்ட் டவுன்லோட் லிங்க்
MASTER_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1Cb5xTE7PmtGaNqL71VBxGuTRfgaLg1iM"

# ஆட்டோ அப்டேட் சோர்ஸ்
AUTO_SOURCE = "https://github.com/alex4528x/m3u/raw/refs/heads/main/jtv.m3u"

TARGET_CHANNELS = [
    "Sun TV", "Vijay TV", "Zee Tamil", "KTV", "Sun Music", 
    "Adithya TV", "Sun News", "Star Sports 1 Tamil", "Sony Sports Ten 1",
    "Jaya TV", "Kalaignar TV", "Raj TV", "News7 Tamil", "Polimer News", 
    "Puthiya Thalaimurai", "Disney Channel", "Nick Tamil", "Discovery Tamil",
    "National Geographic Tamil", "Animal Planet Tamil"
]

def get_auto_channels():
    found_channels = {}
    # ஸ்பார்க்கல் டிவிக்கு மிகவும் பிடித்தமான iPhone User-Agent
    ua = "AppleCoreMedia/1.0.0.19E241 (iPhone; iPhone OS 15_4; Microsoft)"
    
    try:
        resp = requests.get(AUTO_SOURCE, timeout=15)
        lines = resp.text.splitlines()
        temp_tags = []
        
        for line in lines:
            if line.startswith("#EXTINF"):
                # EPG மற்றும் லோகோ தகவல்களை அப்படியே எடுக்கிறது
                temp_tags = [line]
            elif line.startswith("#KODIPROP") or line.startswith("#EXTVLCOPT"):
                temp_tags.append(line)
            elif line.startswith("http"):
                for target_name in TARGET_CHANNELS:
                    if target_name.lower() in str(temp_tags).lower():
                        cookie_match = re.search(r"cookie=(.*)", line)
                        if cookie_match:
                            cookie_val = cookie_match.group(1).replace("%7C", "|")
                            
                            # URL-க்கு உள்ளேயே குக்கீஸை இணைக்கும் 'Pipe Method'
                            # இதுதான் ஸ்பார்க்கல் டிவியில் 403 எரரைத் தவிர்க்கும் ரகசியம்
                            clean_url = line.split("?")[0].replace("%7C", "|")
                            sparkle_link = f"{clean_url}|Cookie={cookie_val}&User-Agent={ua}&Origin=https://jiotv.com&Referer=https://jiotv.com/"
                            
                            channel_data = []
                            channel_data.extend(temp_tags)
                            channel_data.append(sparkle_link)
                            
                            found_channels[target_name] = "\n".join(channel_data)
                temp_tags = []
    except: pass
    return [found_channels[name] for name in TARGET_CHANNELS if name in found_channels]

def merge_playlists():
    try:
        auto_content = "\n\n".join(get_auto_channels())
        master_resp = requests.get(MASTER_DRIVE_URL, timeout=15)
        master_content = master_resp.text
        
        # கூகுள் டிரைவ் லிஸ்டில் உள்ள முதல் வரியை நீக்கிவிட்டு இணைக்கிறது
        master_lines = master_content.splitlines()
        master_body = "\n".join(master_lines[1:]) if master_lines and master_lines[0].startswith("#EXTM3U") else master_content

        # பிளேலிஸ்ட் ஃபார்மட்
        final_playlist = "#EXTM3U\n\n" + auto_content + "\n\n" + master_body
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_playlist)
        print("Success: Playlist optimized for Sparkle TV!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    merge_playlists()
    
