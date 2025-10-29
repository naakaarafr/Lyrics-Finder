import streamlit as st
import requests
from urllib.parse import quote
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Page configuration
st.set_page_config(
    page_title="Lyrics Finder",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #1ed760;
    }
    .lyrics-box {
        background-color: rgba(28, 28, 28, 0.6);
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #1DB954;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        max-height: 600px;
        overflow-y: auto;
        color: #e0e0e0;
    }
    .success-message {
        padding: 1rem;
        background-color: rgba(29, 185, 84, 0.15);
        border-left: 5px solid #1DB954;
        border-radius: 5px;
        color: #1ed760;
    }
    .error-message {
        padding: 1rem;
        background-color: rgba(220, 53, 69, 0.15);
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        color: #ff6b6b;
    }
    .info-message {
        padding: 1rem;
        background-color: rgba(23, 162, 184, 0.15);
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        color: #5dade2;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_lyrics(artist, song):
    """Try multiple APIs to fetch lyrics"""
    apis = [
        {
            'name': 'lyrics-api.fly.dev',
            'func': lambda: get_from_fly_dev(artist, song)
        },
        {
            'name': 'api-ninjas.com',
            'func': lambda: get_from_api_ninjas(artist, song)
        },
        {
            'name': 'lrclib.net',
            'func': lambda: get_from_lrclib(artist, song)
        },
        {
            'name': 'lyrics.ovh',
            'func': lambda: get_from_lyrics_ovh(artist, song)
        }
    ]
    
    for api in apis:
        with st.spinner(f'🔍 Trying {api["name"]}...'):
            try:
                result = api['func']()
                if result:
                    return result
            except Exception as e:
                continue
    
    return None

def get_from_fly_dev(artist, song):
    """Fetch from lyrics-api.fly.dev"""
    url = f'https://lyrics-api.fly.dev/api/lyrics/{quote(artist)}/{quote(song)}'
    response = requests.get(url, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        if 'lyrics' in data and data['lyrics']:
            return {
                'title': data.get('title', song),
                'artist': data.get('artist', artist),
                'lyrics': data['lyrics'],
                'source': 'lyrics-api.fly.dev'
            }
    return None

def get_from_api_ninjas(artist, song):
    """Fetch from api-ninjas"""
    url = 'https://api.api-ninjas.com/v1/lyrics'
    params = {'title': song, 'artist': artist}
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0 and 'lyrics' in data[0]:
            result = data[0]
            return {
                'title': result.get('title', song),
                'artist': result.get('artist', artist),
                'lyrics': result['lyrics'],
                'source': 'api-ninjas.com'
            }
    return None

def get_from_lrclib(artist, song):
    """Fetch from lrclib.net"""
    url = 'https://lrclib.net/api/get'
    params = {'artist_name': artist, 'track_name': song}
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        lyrics = data.get('plainLyrics') or data.get('syncedLyrics', '')
        if lyrics:
            # Remove timestamps if present
            clean_lyrics = '\n'.join([
                line.split(']')[-1].strip() if ']' in line else line
                for line in lyrics.split('\n')
            ])
            return {
                'title': data.get('trackName', song),
                'artist': data.get('artistName', artist),
                'lyrics': clean_lyrics,
                'source': 'lrclib.net'
            }
    return None

def get_from_lyrics_ovh(artist, song):
    """Fetch from lyrics.ovh"""
    url = f'https://api.lyrics.ovh/v1/{quote(artist)}/{quote(song)}'
    response = requests.get(url, timeout=10, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        if 'lyrics' in data and data['lyrics']:
            return {
                'title': song,
                'artist': artist,
                'lyrics': data['lyrics'],
                'source': 'lyrics.ovh'
            }
    return None

# Main App UI
st.title("🎵 Lyrics Finder")
st.markdown("### Find lyrics for your favorite songs")

# Create columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    artist = st.text_input("🎤 Artist Name", placeholder="e.g., Arijit Singh")
    song = st.text_input("🎶 Song Title", placeholder="e.g., Tum Hi Ho")

with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer
    search_button = st.button("🔍 Search Lyrics", use_container_width=True)

# Add some spacing
st.markdown("---")

# Initialize session state for lyrics
if 'lyrics_data' not in st.session_state:
    st.session_state.lyrics_data = None

# Search logic
if search_button:
    if not artist or not song:
        st.markdown('<div class="error-message">❌ Please enter both artist name and song title</div>', unsafe_allow_html=True)
    else:
        # Clear previous results
        st.session_state.lyrics_data = None
        
        # Fetch lyrics
        result = fetch_lyrics(artist, song)
        
        if result:
            st.session_state.lyrics_data = result
        else:
            st.markdown('<div class="error-message">❌ Lyrics not found. Please check the spelling or try a different song.</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="info-message">
                    <strong>💡 Suggestions:</strong><br>
                    • Check the spelling of artist and song name<br>
                    • Try using the full song title<br>
                    • Some songs might not be available in the databases<br>
                    • Try searching on Genius.com or AZLyrics.com
                </div>
            """, unsafe_allow_html=True)

# Display lyrics if available
if st.session_state.lyrics_data:
    data = st.session_state.lyrics_data
    
    st.markdown(f'<div class="success-message">✅ Lyrics found from {data["source"]}</div>', unsafe_allow_html=True)
    
    # Song info
    st.markdown(f"## 🎵 {data['title']}")
    st.markdown(f"### 🎤 {data['artist']}")
    
    # Lyrics display
    st.markdown(f'<div class="lyrics-box">{data["lyrics"]}</div>', unsafe_allow_html=True)
    
    # Download button
    lyrics_text = f"{data['title']} - {data['artist']}\n\n{data['lyrics']}"
    st.download_button(
        label="📥 Download Lyrics",
        data=lyrics_text,
        file_name=f"{data['artist']}_{data['title']}_lyrics.txt",
        mime="text/plain",
        use_container_width=True
    )

