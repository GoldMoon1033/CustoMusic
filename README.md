# 🎵 CustoMusic

A comprehensive music player with intelligent playlist management, customizable UI, and advanced playback controls. Built with Python for cross-platform compatibility and ease of use.

![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-green.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)

## ✨ Key Features

### 🎶 Smart Playlist Management
- **Folder-based playlists** - Organize music into folders for automatic playlist creation
- **Custom naming & ordering** - Use descriptor files for personalized playlist and track names
- **Auto-initialization** - Descriptor files created automatically on first run
- **Format support** - FLAC, WAV, WMA, OGG, AGG, MP3, AIFF

### 🎛️ Advanced Playback Controls
- **Variable playback speed** - 0.5x to 2.0x speed control with live adjustment
- **Rewind functionality** - Jump back 10 seconds instantly
- **Multiple loop modes** - Single track, playlist, or no looping
- **Shuffle mode** - Randomized track playback
- **Precise seeking** - Click progress bar to jump to any position
- **Forward-only timer** - Clean time display format

### 🎨 Customizable Interface
- **HEX color themes** - Full customization with hex color picker
- **7 preset themes** - Dark, Ocean, Forest, Sunset, Purple, Monochrome
- **Collapsible sections** - Hide playlist or track panels with toggle buttons
- **Scalable UI** - Responsive design that adapts to window resizing
- **Scrollable lists** - Proper scrollbars, no content overflow
- **Minimalistic design** - Clean, distraction-free interface

## 🚀 Quick Start

### One-Command Installation
```bash
python run.py --setup
```

### Manual Installation
```bash
# Install dependencies
pip install pygame mutagen

# Run the application
python main.py
```

## 📁 Complete Project Structure

```
CustoMusic/
├── main.py                 # Main application and GUI
├── music_player.py         # Audio playback engine (pygame)
├── playlist_manager.py     # Playlist and descriptor management
├── settings_manager.py     # Configuration and theme system
├── ui_components.py        # Custom scrollable UI components
├── utils.py               # Playlist utilities and tools
├── setup.py               # Automated setup and installation
├── run.py                 # Smart launcher with checks
├── requirements.txt       # Project dependencies
├── README.md             # This documentation
└── playlists/            # Your music playlists (auto-created)
    ├── Rock Music/
    │   ├── song1.mp3
    │   ├── song2.flac
    │   └── playlist.json  # Auto-generated descriptor
    ├── Classical/
    │   ├── piece1.wav
    │   └── playlist.json
    └── Favorites/
        └── playlist.json
```

## 📖 Usage Guide

### Getting Started
1. **Run setup**: `python run.py --setup` (first time only)
2. **Add music**: Create folders in `playlists/` and add your music files
3. **Launch player**: `python run.py` or `python main.py`
4. **Enjoy**: Select playlists and tracks, customize as needed!

### Creating Playlists
1. **Create folder** in `playlists/` directory (e.g., "My Rock Music")
2. **Add music files** - drag and drop your audio files
3. **Launch app** - descriptor files are auto-generated
4. **Customize** (optional) - edit `playlist.json` for custom names

### Playlist Descriptor Format
```json
{
  "display_name": "🎸 My Rock Collection",
  "description": "The best rock songs of all time",
  "created": "2024-01-01T12:00:00",
  "tracks": {
    "song1.mp3": {
      "display_name": "Epic Rock Anthem",
      "order": 1,
      "added": "2024-01-01T12:00:00"
    },
    "song2.flac": {
      "display_name": "Guitar Masterpiece",
      "order": 2,
      "added": "2024-01-01T12:05:00"
    }
  }
}
```

### Advanced Controls
- **Speed Control**: Adjust playback from 0.5x to 2.0x speed
- **Rewind**: ⏪ button jumps back 10 seconds
- **Loop Modes**: 🔁 playlist loop, 🔂 single track loop
- **Shuffle**: 🔀 randomize track order
- **Seeking**: Click anywhere on progress bar
- **Volume**: Smooth volume slider with visual feedback

## 🛠️ Utilities & Tools

### Built-in Utilities
```bash
# Analyze your music collection
python utils.py analyze

# Import music from existing folders
python utils.py import /path/to/music --by-artist

# Backup your playlists
python utils.py backup

# Clean up empty playlists
python utils.py clean

# Check system requirements
python run.py --check
```

### Playlist Management
- **Auto-organization** by artist or folder structure
- **Bulk import** from existing music directories
- **Backup/restore** functionality for playlist safety
- **Analysis tools** for collection statistics

## 🎨 Customization

### Color Themes
Access via **File → Settings**:

- **Default** - Professional blue (#4a90e2) and gray (#2c3e50)
- **Dark** - Dark theme (#34495e) with orange accents (#e67e22)
- **Ocean** - Blue tones (#3498db) with teal highlights (#1abc9c)
- **Forest** - Green theme (#27ae60) with warm accents (#f39c12)
- **Sunset** - Orange/red scheme (#e67e22, #e74c3c)
- **Purple** - Purple theme (#9b59b6) with pink accents (#e91e63)
- **Monochrome** - Professional grayscale (#5d6d7e, #95a5a6)

### Custom Colors
- Use hex format: `#ff5733` (red-orange), `#33ff57` (green)
- Colors apply to buttons, progress bars, and highlights
- Live preview of color changes
- Reset to defaults option available

### UI Customization
- **Collapsible panels** - Hide playlists or tracks with − buttons
- **Resizable window** - Drag to resize, UI adapts automatically
- **Scrollable lists** - Mouse wheel support, proper scrollbars
- **Minimalistic design** - Clean layout without clutter

## 🔧 Technical Details

### Supported Audio Formats

| Format | Extension | Quality | Metadata | Notes |
|--------|-----------|---------|----------|--------|
| MP3 | `.mp3` | Lossy | ✅ | Most common, good compatibility |
| FLAC | `.flac` | Lossless | ✅ | High quality, larger files |
| WAV | `.wav` | Lossless | ❌ | Uncompressed, very large |
| OGG | `.ogg` | Lossy | ✅ | Open source alternative |
| WMA | `.wma` | Lossy | ✅ | Windows Media Audio |
| AIFF | `.aiff` | Lossless | ✅ | Apple audio format |
| AGG | `.agg` | Varies | ✅ | Audio container format |

### System Requirements
- **Python 3.7+** (automatically checked)
- **pygame 2.1.0+** for audio playback
- **mutagen 1.45.0+** for metadata reading
- **50-100MB RAM** during operation
- **Audio output device** with working drivers

### Performance Features
- **Efficient memory usage** - Only current track loaded
- **Background processing** - Non-blocking UI
- **Lazy loading** - Playlists loaded on demand
- **Smart caching** - Settings and metadata cached
- **Multi-threading** - Responsive interface during playback

## 🐛 Troubleshooting

### Installation Issues
```bash
# Check what's missing
python run.py --check

# Run complete setup
python run.py --setup

# Manual dependency install
pip install pygame mutagen
```

### Common Problems

**"No audio output"**
- Check system volume and audio device
- Verify pygame installation: `python -c "import pygame"`
- Test with different audio files

**"Playlists not showing"**
- Check `playlists/` folder exists and contains subfolders
- Verify music files have supported extensions
- Try **File → Refresh Playlists**

**"UI elements not responding"**
- Close and restart the application
- Check if window is properly focused
- Try resizing the window

**"Colors not applying"**
- Restart application after color changes
- Ensure hex colors are valid (e.g., #ff0000)
- Use **Reset to Defaults** if needed

### Debug Mode
Set environment variable for detailed logging:
```bash
# Windows
set DEBUG=1 && python main.py

# Linux/macOS  
DEBUG=1 python main.py
```

## 💡 Tips & Tricks

### Organization Tips
- Create themed playlists: "Workout", "Study", "Party"
- Use emoji in display names: "🎸 Rock", "🎼 Classical"
- Keep playlists under 100 tracks for best performance
- Use descriptive folder names - they become playlist names

### Playback Tips
- Use speed control for language learning (0.8x)
- Rewind function perfect for music practice
- Single loop great for learning new songs
- Shuffle mode for discovering forgotten tracks

### Customization Tips
- Dark theme reduces eye strain
- Collapse unused panels for more space
- Adjust window size for your screen
- Export playlists to share with friends

## 🤝 Contributing

### Development Setup
```bash
git clone https://github.com/GoldMoon1033/CustoMusic.git
cd CustoMusic
pip install -r requirements.txt
python run.py --check
```

### Architecture Overview
- **main.py** - GUI application using tkinter
- **music_player.py** - Audio engine with pygame backend
- **playlist_manager.py** - File system and JSON descriptor management
- **settings_manager.py** - Configuration persistence and themes
- **ui_components.py** - Custom widgets (scrollable frames, buttons)

### Enhancement Ideas
- **Equalizer** - Audio frequency adjustment
- **Visualizations** - Spectrum analyzer display
- **Internet radio** - Stream online stations
- **Plugin system** - Extensible architecture
- **Mobile app** - Companion mobile interface
- **Cloud sync** - Cross-device playlist sync

## 📄 License

MIT License - Free to use, modify, and distribute for any purpose.

---

## 🎯 Perfect For

- **Music enthusiasts** who want full control over their listening experience
- **Audiophiles** who need support for lossless formats like FLAC
- **Organizers** who prefer folder-based playlist management
- **Customizers** who want personalized themes and layouts
- **Students** who need speed control for educational audio
- **Anyone** who wants a clean, distraction-free music player

**Ready to revolutionize your music listening experience? Get started with `python run.py --setup`!** 🎵
