#!/usr/bin/env python3
"""
Setup script for CustoMusic
Handles installation, dependency checking, and initial setup.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class MusicPlayerSetup:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.playlists_dir = self.project_dir / "playlists"
        self.config_dir = Path.home() / '.music_player'
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        if sys.version_info < (3, 7):
            print("❌ Error: Python 3.7 or higher is required")
            print(f"   Current version: {sys.version}")
            return False
        
        print(f"✅ Python version: {sys.version}")
        return True
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("\n📦 Installing dependencies...")
        
        requirements_file = self.project_dir / "requirements.txt"
        
        if requirements_file.exists():
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ])
                print("✅ Dependencies installed successfully")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies")
                print("   Try running: pip install pygame mutagen")
                return False
        else:
            # Install individual packages
            packages = ["pygame>=2.1.0", "mutagen>=1.45.0"]
            for package in packages:
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", package
                    ])
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package}")
                    return False
            return True
    
    def create_directory_structure(self):
        """Create necessary directories"""
        print("\n📁 Creating directory structure...")
        
        # Create playlists directory
        self.playlists_dir.mkdir(exist_ok=True)
        print(f"✅ Created playlists directory: {self.playlists_dir}")
        
        # Create config directory
        self.config_dir.mkdir(exist_ok=True)
        print(f"✅ Created config directory: {self.config_dir}")
        
        return True
    
    def create_sample_playlists(self):
        """Create sample playlist structure"""
        print("\n🎵 Creating sample playlists...")
        
        sample_playlists = [
            {
                "name": "My Favorites",
                "display_name": "⭐ My Favorite Songs",
                "description": "A collection of my most loved tracks"
            },
            {
                "name": "Workout Music",
                "display_name": "💪 High Energy Workout",
                "description": "Energetic songs for workout sessions"
            },
            {
                "name": "Relaxation",
                "display_name": "🧘 Chill & Relax",
                "description": "Peaceful music for relaxation"
            },
            {
                "name": "Classical",
                "display_name": "🎼 Classical Collection",
                "description": "Beautiful classical music pieces"
            }
        ]
        
        for playlist_info in sample_playlists:
            playlist_dir = self.playlists_dir / playlist_info["name"]
            playlist_dir.mkdir(exist_ok=True)
            
            # Create descriptor file
            descriptor_path = playlist_dir / "playlist.json"
            if not descriptor_path.exists():
                descriptor = {
                    "display_name": playlist_info["display_name"],
                    "description": playlist_info["description"],
                    "created": self._get_timestamp(),
                    "tracks": {}
                }
                
                with open(descriptor_path, 'w', encoding='utf-8') as f:
                    json.dump(descriptor, f, indent=2, ensure_ascii=False)
            
            # Create README file with instructions
            readme_path = playlist_dir / "README.txt"
            if not readme_path.exists():
                readme_content = f"""# {playlist_info['display_name']}

{playlist_info['description']}

## How to add music:
1. Copy your music files (.mp3, .flac, .wav, .ogg, etc.) to this folder
2. Restart the music player or refresh playlists
3. The playlist.json file will be automatically updated

## Supported formats:
- MP3 (.mp3)
- FLAC (.flac) 
- WAV (.wav)
- OGG (.ogg)
- WMA (.wma)
- AIFF (.aiff)

## Custom naming:
Edit playlist.json to customize track names and order.
"""
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)
            
            print(f"✅ Created playlist: {playlist_info['display_name']}")
        
        return True
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut (Windows only for now)"""
        if sys.platform == "win32":
            print("\n🖥️ Creating desktop shortcut...")
            try:
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                shortcut_path = os.path.join(desktop, "CustoMusic.lnk")
                target = os.path.join(self.project_dir, "main.py")
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = f'"{target}"'
                shortcut.WorkingDirectory = str(self.project_dir)
                shortcut.IconLocation = sys.executable
                shortcut.save()
                
                print("✅ Desktop shortcut created")
                return True
            except ImportError:
                print("ℹ️  Desktop shortcut creation requires: pip install winshell pywin32")
                return True
            except Exception as e:
                print(f"⚠️  Could not create desktop shortcut: {e}")
                return True
        else:
            print("ℹ️  Desktop shortcut creation only supported on Windows")
            return True
    
    def verify_installation(self):
        """Verify that everything is set up correctly"""
        print("\n🔍 Verifying installation...")
        
        # Check if main.py exists
        main_file = self.project_dir / "main.py"
        if not main_file.exists():
            print("❌ main.py not found")
            return False
        print("✅ main.py found")
        
        # Test import of required modules
        try:
            import pygame
            print(f"✅ pygame version: {pygame.version.ver}")
        except ImportError:
            print("❌ pygame not installed")
            return False
        
        try:
            import mutagen
            print(f"✅ mutagen version: {mutagen.version_string}")
        except ImportError:
            print("❌ mutagen not installed") 
            return False
        
        # Check directory structure
        if not self.playlists_dir.exists():
            print("❌ playlists directory missing")
            return False
        print("✅ playlists directory exists")
        
        if not self.config_dir.exists():
            print("❌ config directory missing")
            return False
        print("✅ config directory exists")
        
        return True
    
    def _get_timestamp(self):
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🎵 CustoMusic Setup")
        print("=" * 40)
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            print("\n❌ Setup failed: Could not install dependencies")
            return False
        
        # Create directories
        if not self.create_directory_structure():
            print("\n❌ Setup failed: Could not create directories")
            return False
        
        # Create sample playlists
        if not self.create_sample_playlists():
            print("\n❌ Setup failed: Could not create sample playlists")
            return False
        
        # Create desktop shortcut (optional)
        self.create_desktop_shortcut()
        
        # Verify installation
        if not self.verify_installation():
            print("\n❌ Setup failed: Installation verification failed")
            return False
        
        print("\n" + "=" * 40)
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Add your music files to the playlist folders")
        print("2. Run: python main.py")
        print("3. Enjoy your music! 🎶")
        print("\nPlaylist folders created:")
        for folder in self.playlists_dir.iterdir():
            if folder.is_dir():
                print(f"   📁 {folder.name}")
        
        return True

def main():
    """Main setup function"""
    setup = MusicPlayerSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "install":
            success = setup.install_dependencies()
            sys.exit(0 if success else 1)
        
        elif command == "verify":
            success = setup.verify_installation()
            sys.exit(0 if success else 1)
        
        elif command == "clean":
            # Clean up config directory
            import shutil
            if setup.config_dir.exists():
                shutil.rmtree(setup.config_dir)
                print("✅ Cleaned config directory")
            sys.exit(0)
        
        elif command == "help":
            print("CustoMusic Setup")
            print("Usage: python setup.py [command]")
            print("\nCommands:")
            print("  (no command)  - Run full setup")
            print("  install       - Install dependencies only")
            print("  verify        - Verify installation")
            print("  clean         - Clean config directory")
            print("  help          - Show this help")
            sys.exit(0)
        
        else:
            print(f"Unknown command: {command}")
            print("Run 'python setup.py help' for usage information")
            sys.exit(1)
    
    else:
        # Run full setup
        success = setup.run_setup()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()