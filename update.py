import requests

# 1. உங்கள் Vercel லிங்க் (இங்கே உங்கள் உண்மையான Vercel URL-ஐப் போடவும்)
MY_VERCEL_URL = "https://உங்கள்-லிங்க்-இங்கே.vercel.app"

# 2. உங்கள் Google Drive மாஸ்டர் லிங்க்
MASTER_DRIVE_URL = "https://drive.google.com/uc?export=download&id=1Cb5xTE7PmtGaNqL71VBxGuTRfgaLg1iM"

def merge_playlists():
    try:
        # Vercel-ல் இருந்து ஜியோ சேனல்களை எடுக்கிறது
        jio_resp = requests.get(MY_VERCEL_URL, timeout=15)
        jio_content = jio_resp.text
        
        # கூகுள் டிரைவ்-ல் இருந்து 100 சேனல்களை எடுக்கிறது
        drive_resp = requests.get(MASTER_DRIVE_URL, timeout=15)
        drive_content = drive_resp.text
        
        # இரண்டையும் இணைத்து ஒரே ஃபைலாக மாற்றுகிறது
        final_playlist = jio_content + "\n\n" + drive_content
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_playlist)
        print("Success: Playlist Combined!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    merge_playlists()
    
