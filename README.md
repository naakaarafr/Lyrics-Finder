# 🎵 Lyrics Finder

A streamlit-based web application that helps you find song lyrics quickly and easily. The app searches through multiple lyrics databases to provide accurate results for your favorite songs.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Multi-Source Search**: Automatically searches across multiple lyrics APIs for best results
- **Clean Interface**: User-friendly Streamlit interface with a modern design
- **Download Functionality**: Save lyrics as text files for offline access
- **Fallback System**: If one API fails, automatically tries alternative sources
- **Real-time Search**: Get instant results with visual loading indicators
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🎯 Supported APIs

The application integrates with multiple lyrics providers:

1. **lyrics-api.fly.dev** - Primary source
2. **api-ninjas.com** - Secondary source
3. **lrclib.net** - Includes synced lyrics support
4. **lyrics.ovh** - Backup source

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/naakaarafr/Lyrics-Finder.git
   cd Lyrics-Finder
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   Or install dependencies manually:
   ```bash
   pip install streamlit requests
   ```

3. **Run the application**
   ```bash
   streamlit run lyricsfinder.py
   ```

4. **Access the app**
   
   The app will automatically open in your default browser at `http://localhost:8501`

## 📖 Usage

1. **Enter Song Details**
   - Input the artist name in the "Artist Name" field
   - Input the song title in the "Song Title" field

2. **Search**
   - Click the "🔍 Search Lyrics" button
   - The app will search through multiple databases automatically

3. **View Results**
   - Lyrics will be displayed in a scrollable, formatted box
   - Song and artist information appears at the top
   - Source of the lyrics is indicated

4. **Download (Optional)**
   - Click the "📥 Download Lyrics" button to save as a text file

## 🛠️ Technical Details

### Project Structure

```
Lyrics-Finder/
│
├── lyricsfinder.py       # Main application file
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```

### Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP library for API calls
- **urllib**: URL encoding utilities

### API Integration

The application uses a fallback mechanism that tries each API in sequence:

```python
1. lyrics-api.fly.dev
2. api-ninjas.com
3. lrclib.net
4. lyrics.ovh
```

If the first API doesn't return results, it automatically tries the next one until lyrics are found or all sources are exhausted.

## 🎨 Customization

### Styling

The app uses custom CSS for a Spotify-inspired theme. You can modify the styling in the `st.markdown()` section of the code:

- **Colors**: Change the color scheme by modifying hex values
- **Layout**: Adjust padding, margins, and border-radius
- **Typography**: Modify font families and sizes

### Adding New APIs

To add a new lyrics API:

1. Create a new function following the pattern:
   ```python
   def get_from_new_api(artist, song):
       # Your API implementation
       return {
           'title': song,
           'artist': artist,
           'lyrics': lyrics_text,
           'source': 'api-name'
       }
   ```

2. Add it to the `apis` list in the `fetch_lyrics()` function

## ⚠️ Troubleshooting

### Common Issues

**Issue**: Lyrics not found
- **Solution**: Check spelling of artist and song names
- Try using the exact/official song title
- Some songs may not be available in the databases

**Issue**: SSL/Certificate warnings
- **Solution**: The app handles this automatically with `verify=False` for certain APIs

**Issue**: Timeout errors
- **Solution**: Check your internet connection
- Some APIs may be temporarily unavailable

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Ideas

- Add more lyrics API sources
- Implement caching for faster repeated searches
- Add language translation support
- Include album art display
- Add playlist/batch search functionality

## 👨‍💻 Author

**naakaarafr**
- GitHub: [@naakaarafr](https://github.com/naakaarafr)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- All the free lyrics API providers
- Open source community

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

**Note**: This application is for educational and personal use only. Please respect copyright laws and the terms of service of the lyrics providers.
