# 🎵 CustoMusic

A feature-rich music player with intelligent playlist management, customizable UI, and comprehensive playback controls. Built with Python and tkinter for cross-platform compatibility.

## ✨ Key Features

### 🎶 Smart Playlist Management
- **Folder-based playlists** - Create playlists by organizing music into folders
- **Custom naming & ordering** - Use descriptor files for personalized playlist and track names
- **Auto-initialization** - Descriptor files created automatically on first run
- **Multiple format support** - FLAC, WAV, WMA, OGG, AGG, MP3, AIFF

### 🎛️ Advanced Playback Controls
- **Variable playback speed** - 0.5x to 2.0x speed control
- **Rewind functionality** - Jump back 10 seconds instantly
- **Multiple loop modes** - Single track, playlist, or no looping
- **Shuffle mode** - Randomized track playback
- **Precise seeking** - Click progress bar to jump to any position

### 🎨 Customizable Interface
- **Hex color themes** - Fully customizable color schemes
- **Preset themes** - 7 built-in color themes (Dark, Ocean, Forest, etc.)
- **Collapsible sections** - Hide playlist or track panels to save space
- **Scalable UI** - Responsive design that adapts to window resizing
- **Scrollable lists** - No content overflow, smooth scrolling with mouse wheel

### 🔧 Advanced Features
- **Session persistence** - Remembers last played track and position
- **Metadata support** - Displays track information when available
- **Export playlists** - Save to M3U or PLS formats
- **Settings management** - Comprehensive configuration system

## 📋 Requirements

### Dependencies
```bash
pip install pygame mutagen
```

### System Requirements
- Python 3.7 or higher
- Audio output device
- At least 100MB free disk space

## 🚀 Installation & Setup

### 1. Clone or Download
```bash
git clone https://github.com/GoldMoon1033/CustoMusic.git
cd CustoMusic
```

### 2. Install Dependencies
```bash
pip install pygame mutagen
```

### 3. Run the Application
```bash
python main.py
```

## 📁 Project Structure

```
CustoMusic/
├── main.py                 # Main application and UI
├── music_player.py         # Audio playback engine
├── playlist_manager.py     # Playlist and file management
├── settings_manager.py     # Configuration and themes
├── ui_components.py        # Custom UI components
├── playlists/             # Playlist folders (auto-created)
│   ├── Rock Music/        # Example playlist folder
│   │   ├── song1.mp3
│   │   ├── song2.flac
│   │   └── playlist.json  # Auto-generated descriptor
│   └── Classical/
│       ├── piece1.wav
│       └── playlist.json
└── README.md              # This documentation
```

## 📖 How to Use

### Creating Playlists
1. **Create folders** in the `playlists` directory
2. **Add music files** to each folder
3. **Run the application** - descriptor files are created automatically
4. **Customize names** by editing `playlist.json` files (optional)

### Playlist Descriptor Format
```json
{
  "display_name": "My Rock Collection",
  "description": "Best rock songs of all time",
  "tracks": {
    "song1.mp3": {
      "display_name": "Awesome Rock Song",
      "order": 1
    },
    "song2.flac": {
      "display_name": "Another Great Track",
      "order": 2
    }
  }
}
```

### Basic Playback
1. **Select playlist** from left panel
2. **Double-click track** to start playing
3. **Use controls** - play/pause, next/previous, volume
4. **Adjust speed** - Use speed slider for faster/slower playback

### Advanced Controls
- **Rewind**: ⏪ button jumps back 10 seconds
- **Shuffle**: 🔀 button enables random track order
- **Loop Playlist**: 🔁 button repeats entire playlist
- **Loop Single**: 🔂 button repeats current track
- **Seeking**: Click progress bar to jump to position

### Customizing Colors
1. **Go to Settings** - File → Settings
2. **Choose colors** - Pick primary and secondary colors
3. **Use presets** - Apply built-in themes
4. **Reset if needed** - Return to default colors

## 🎨 Color Themes

### Built-in Presets
- **Default** - Classic blue and gray
- **Dark** - Dark mode with orange accents
- **Ocean** - Blue tones with teal accents
- **Forest** - Green theme with warm highlights
- **Sunset** - Orange and red color scheme
- **Purple** - Purple theme with pink accents
- **Monochrome** - Grayscale professional look

### Custom Colors
- Use hex format: `#4a90e2` (blue), `#e74c3c` (red)
- Colors apply to buttons, highlights, and accents
- Settings saved automatically

## ⚙️ Configuration

### Settings File Location
- **Windows**: `%USERPROFILE%\.music_player\settings.json`
- **Linux/macOS**: `~/.music_player/settings.json`

### Key Settings
```json
{
  "primary_color": "#4a90e2",
  "secondary_color": "#2c3e50",
  "default_volume": 70,
  "remember_position": true,
  "auto_advance": true,
  "window_width": 1000,
  "window_height": 700
}
```

## 🔧 Supported Audio Formats

| Format | Extension | Quality | Notes |
|--------|-----------|---------|-------|
| MP3 | `.mp3` | Lossy | Most common format |
| FLAC | `.flac` | Lossless | High quality, larger files |
| WAV | `.wav` | Lossless | Uncompressed audio |
| OGG | `.ogg` | Lossy | Open source format |
| WMA | `.wma` | Lossy | Windows Media Audio |
| AIFF | `.aiff` | Lossless | Apple format |
| AGG | `.agg` | Varies | Audio container format |

## 🐛 Troubleshooting

### Common Issues

**"No audio output"**
- Check system audio settings
- Verify audio files are not corrupted
- Restart the application

**"Playlist not showing"**
- Ensure folders exist in `playlists` directory
- Check file permissions
- Refresh playlists (File → Refresh Playlists)

**"Playback stuttering"**
- Close other audio applications
- Reduce playback speed if needed
- Check available system resources

**"Colors not applying"**
- Restart application after color changes
- Check if hex colors are valid format
- Reset to defaults if issues persist

### Debug Information
- Check `~/.music_player/` for log files
- Settings are backed up on corruption
- Descriptor files can be manually edited

## ⚡ Performance

### Optimization Features
- **Efficient memory usage** - Only loads current track
- **Background threading** - UI remains responsive during playback
- **Lazy loading** - Playlists loaded on demand
- **Caching** - Settings and metadata cached for speed

### System Resources
- **Memory**: 50-100MB typical usage
- **CPU**: 1-5% during playback
- **Storage**: Settings and cache under 1MB

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Install development dependencies: `pip install pygame mutagen`
3. Make changes and test thoroughly
4. Submit pull request with clear description

### Areas for Enhancement
- **Additional formats** - Support for more audio codecs
- **Visualizations** - Audio spectrum display
- **Network features** - Internet radio support
- **Plugin system** - Extensible architecture
- **Mobile support** - Touch-friendly interface

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🎯 Technical Architecture

### Core Components
- **main.py** - Application UI and user interaction management
- **music_player.py** - Audio engine using pygame for playback control
- **playlist_manager.py** - File system integration and descriptor management
- **settings_manager.py** - Configuration persistence and theme management
- **ui_components.py** - Custom widgets for enhanced user interface

### Design Principles
- **Modular architecture** - Separated concerns for maintainability
- **Event-driven** - Callback system for component communication
- **Cross-platform** - Pure Python implementation for compatibility
- **User-centric** - Intuitive interface with advanced customization

---

**Perfect for**: Music enthusiasts who want control over their listening experience with a clean, customizable interface that respects their organizational preferences.
