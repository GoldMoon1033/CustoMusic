#!/usr/bin/env python3
"""
CustoMusic Launcher
Handles startup checks, dependency verification, and launches the main application.
"""

import sys
import os
import subprocess
from pathlib import Path

class MusicPlayerLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.main_script = self.project_dir / "main.py"
        self.setup_script = self.project_dir / "setup.py"
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        missing_deps = []
        
        try:
            import pygame
        except ImportError:
            missing_deps.append("pygame")
        
        try:
            import mutagen
        except ImportError:
            missing_deps.append("mutagen")
        
        return missing_deps
    
    def check_project_files(self):
        """Check if required project files exist"""
        required_files = [
            "main.py",
            "music_player.py", 
            "playlist_manager.py",
            "settings_manager.py",
            "ui_components.py"
        ]
        
        missing_files = []
        for filename in required_files:
            if not (self.project_dir / filename).exists():
                missing_files.append(filename)
        
        return missing_files
    
    def run_setup(self):
        """Run the setup script"""
        if self.setup_script.exists():
            print("🔧 Running setup script...")
            try:
                result = subprocess.run([sys.executable, str(self.setup_script)], 
                                      capture_output=False)
                return result.returncode == 0
            except Exception as e:
                print(f"❌ Setup failed: {e}")
                return False
        else:
            print("❌ Setup script not found")
            return False
    
    def create_playlists_directory(self):
        """Create playlists directory if it doesn't exist"""
        playlists_dir = self.project_dir / "playlists"
        if not playlists_dir.exists():
            print("📁 Creating playlists directory...")
            playlists_dir.mkdir()
            
            # Create a simple example
            example_dir = playlists_dir / "Example"
            example_dir.mkdir()
            
            readme_content = """# Example Playlist

This is an example playlist folder.

To use this music player:
1. Add your music files to this folder or create new playlist folders
2. Supported formats: MP3, FLAC, WAV, OGG, WMA, AIFF
3. The player will automatically create playlist.json files for organization

Happy listening! 🎵
"""
            
            with open(example_dir / "README.txt", 'w') as f:
                f.write(readme_content)
            
            return True
        return False
    
    def launch_main_application(self):
        """Launch the main music player application"""
        if not self.main_script.exists():
            print("❌ Main application script not found")
            return False
        
        try:
            print("🎵 Launching CustoMusic...")
            subprocess.run([sys.executable, str(self.main_script)])
            return True
        except Exception as e:
            print(f"❌ Failed to launch application: {e}")
            return False
    
    def show_help_message(self):
        """Show help and troubleshooting information"""
        print("""
🎵 CustoMusic - Help & Troubleshooting

QUICK START:
1. Run: python run.py
2. Add music files to playlist folders
3. Enjoy your music!

COMMANDS:
  python run.py          - Launch the music player
  python run.py --setup  - Run setup wizard
  python run.py --help   - Show this help
  python run.py --check  - Check system requirements

ADDING MUSIC:
1. Navigate to the 'playlists' folder
2. Create folders for your playlists (e.g., "Rock", "Classical")
3. Add music files to these folders
4. The player will automatically organize them

SUPPORTED FORMATS:
- MP3 (.mp3) - Most common format
- FLAC (.flac) - High quality lossless
- WAV (.wav) - Uncompressed audio
- OGG (.ogg) - Open source format
- WMA (.wma) - Windows Media Audio
- AIFF (.aiff) - Apple format

TROUBLESHOOTING:
- If dependencies are missing, run: python run.py --setup
- For import errors, try: pip install pygame mutagen
- Check Python version: python --version (needs 3.7+)
- Make sure audio drivers are working on your system

UTILITIES:
  python utils.py analyze          - Analyze your playlists
  python utils.py import <folder>  - Import music from folder
  python utils.py backup          - Backup your playlists

CUSTOMIZATION:
- Colors: Use File → Settings to customize colors
- Themes: Choose from 7 built-in color themes
- Playlists: Edit playlist.json files for custom names/order

For more help, check the README.md file.
        """)
    
    def check_system_requirements(self):
        """Check and display system requirements"""
        print("🔍 System Requirements Check")
        print("=" * 40)
        
        # Python version
        python_version = sys.version_info
        if python_version >= (3, 7):
            print(f"✅ Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            print(f"❌ Python: {python_version.major}.{python_version.minor}.{python_version.micro} (needs 3.7+)")
        
        # Dependencies
        missing_deps = self.check_dependencies()
        if not missing_deps:
            print("✅ Dependencies: All required packages installed")
        else:
            print(f"❌ Dependencies: Missing {', '.join(missing_deps)}")
            print(f"   Install with: pip install {' '.join(missing_deps)}")
        
        # Project files
        missing_files = self.check_project_files()
        if not missing_files:
            print("✅ Project Files: All required files present")
        else:
            print(f"❌ Project Files: Missing {', '.join(missing_files)}")
        
        # Playlists directory
        playlists_dir = self.project_dir / "playlists"
        if playlists_dir.exists():
            playlist_count = len([d for d in playlists_dir.iterdir() if d.is_dir()])
            print(f"✅ Playlists: Directory exists with {playlist_count} playlists")
        else:
            print("⚠️  Playlists: Directory will be created on first run")
        
        # Audio system (basic check)
        try:
            import pygame
            pygame.mixer.pre_init()
            pygame.mixer.init()
            pygame.mixer.quit()
            print("✅ Audio System: Basic audio functionality available")
        except Exception as e:
            print(f"❌ Audio System: {e}")
        
        print("\nReady to run!" if not missing_deps and not missing_files else "Setup required")
    
    def run(self, args):
        """Main launcher logic"""
        if "--help" in args or "-h" in args:
            self.show_help_message()
            return
        
        if "--check" in args:
            self.check_system_requirements()
            return
        
        if "--setup" in args:
            if self.run_setup():
                print("✅ Setup completed! You can now run the music player.")
            else:
                print("❌ Setup failed. Please check the error messages above.")
            return
        
        # Check if setup is needed
        missing_deps = self.check_dependencies()
        missing_files = self.check_project_files()
        
        if missing_deps or missing_files:
            print("⚠️  Setup required!")
            print("\nMissing dependencies:" if missing_deps else "", end="")
            for dep in missing_deps:
                print(f" {dep}", end="")
            print("\nMissing files:" if missing_files else "", end="")
            for file in missing_files:
                print(f" {file}", end="")
            print("\n")
            
            response = input("Would you like to run setup now? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                if not self.run_setup():
                    print("❌ Setup failed. Cannot launch application.")
                    return
            else:
                print("❌ Cannot launch without required dependencies and files.")
                print("Run 'python run.py --setup' when ready.")
                return
        
        # Create playlists directory if needed
        self.create_playlists_directory()
        
        # Launch the application
        self.launch_main_application()

def main():
    """Main entry point"""
    launcher = MusicPlayerLauncher()
    launcher.run(sys.argv[1:])

if __name__ == "__main__":
    main()