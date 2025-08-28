#!/usr/bin/env python3
"""
Music Player Utilities
Provides helpful functions for playlist management, file operations, and maintenance.
"""

import os
import json
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import time

class MusicPlayerUtils:
    def __init__(self, playlists_dir="playlists"):
        self.playlists_dir = Path(playlists_dir)
        self.supported_formats = {'.mp3', '.flac', '.wav', '.ogg', '.wma', '.aiff', '.agg'}
        
    def scan_music_directory(self, source_dir: str, organize_by_artist: bool = False) -> Dict[str, List[str]]:
        """Scan a directory for music files and suggest playlist organization"""
        source_path = Path(source_dir)
        
        if not source_path.exists():
            print(f"❌ Directory not found: {source_dir}")
            return {}
        
        print(f"🔍 Scanning {source_dir} for music files...")
        
        music_files = []
        for file_path in source_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                music_files.append(file_path)
        
        if not music_files:
            print("❌ No supported music files found")
            return {}
        
        print(f"✅ Found {len(music_files)} music files")
        
        if organize_by_artist:
            return self._organize_by_artist(music_files)
        else:
            return self._organize_by_folder(music_files, source_path)
    
    def _organize_by_artist(self, music_files: List[Path]) -> Dict[str, List[str]]:
        """Organize files by artist using metadata"""
        try:
            from mutagen import File
        except ImportError:
            print("❌ mutagen required for artist-based organization")
            print("   Install with: pip install mutagen")
            return {}
        
        organized = {}
        unknown_artist = "Unknown Artist"
        
        for file_path in music_files:
            try:
                audio_file = File(str(file_path))
                artist = unknown_artist
                
                if audio_file is not None:
                    # Try different artist tags
                    for tag in ['TPE1', 'ARTIST', 'AlbumArtist']:
                        if tag in audio_file:
                            artist = str(audio_file[tag][0])
                            break
                
                # Clean up artist name for folder use
                safe_artist = self._make_safe_filename(artist)
                
                if safe_artist not in organized:
                    organized[safe_artist] = []
                
                organized[safe_artist].append(str(file_path))
                
            except Exception as e:
                print(f"⚠️  Could not read metadata from {file_path.name}: {e}")
                if unknown_artist not in organized:
                    organized[unknown_artist] = []
                organized[unknown_artist].append(str(file_path))
        
        return organized
    
    def _organize_by_folder(self, music_files: List[Path], base_path: Path) -> Dict[str, List[str]]:
        """Organize files by their current folder structure"""
        organized = {}
        
        for file_path in music_files:
            try:
                # Get relative path from base directory
                relative_path = file_path.relative_to(base_path)
                folder_name = relative_path.parent.name if relative_path.parent != Path('.') else "Mixed Music"
                
                if folder_name not in organized:
                    organized[folder_name] = []
                
                organized[folder_name].append(str(file_path))
                
            except ValueError:
                # File is not in base path
                folder_name = "External Files"
                if folder_name not in organized:
                    organized[folder_name] = []
                organized[folder_name].append(str(file_path))
        
        return organized
    
    def import_music(self, source_dir: str, organize_by_artist: bool = False, copy_files: bool = True):
        """Import music files and create playlists"""
        organized = self.scan_music_directory(source_dir, organize_by_artist)
        
        if not organized:
            return False
        
        print(f"\n📂 Creating {len(organized)} playlists...")
        
        for playlist_name, file_paths in organized.items():
            playlist_dir = self.playlists_dir / playlist_name
            playlist_dir.mkdir(parents=True, exist_ok=True)
            
            # Create or update descriptor
            descriptor_path = playlist_dir / "playlist.json"
            descriptor = self._load_or_create_descriptor(descriptor_path, playlist_name)
            
            print(f"\n📁 Processing playlist: {playlist_name}")
            
            for i, source_path in enumerate(file_paths, 1):
                source_file = Path(source_path)
                
                if copy_files:
                    # Copy file to playlist directory
                    dest_path = playlist_dir / source_file.name
                    
                    # Handle duplicate names
                    counter = 1
                    while dest_path.exists():
                        name_parts = source_file.stem, counter, source_file.suffix
                        dest_path = playlist_dir / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                        counter += 1
                    
                    shutil.copy2(source_path, dest_path)
                    relative_path = dest_path.name
                    print(f"   ✅ Copied: {source_file.name}")
                else:
                    # Use original path (symlink would be better but not cross-platform)
                    relative_path = str(source_file)
                    print(f"   🔗 Linked: {source_file.name}")
                
                # Add to descriptor
                if relative_path not in descriptor["tracks"]:
                    descriptor["tracks"][relative_path] = {
                        "display_name": source_file.stem,
                        "order": len(descriptor["tracks"]) + 1,
                        "added": self._get_timestamp()
                    }
            
            # Save updated descriptor
            with open(descriptor_path, 'w', encoding='utf-8') as f:
                json.dump(descriptor, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Created playlist with {len(file_paths)} tracks")
        
        print(f"\n🎉 Successfully imported music into {len(organized)} playlists!")
        return True
    
    def backup_playlists(self, backup_dir: str = None) -> bool:
        """Create a backup of all playlists and descriptors"""
        if backup_dir is None:
            backup_dir = f"playlist_backup_{int(time.time())}"
        
        backup_path = Path(backup_dir)
        
        try:
            print(f"💾 Creating playlist backup...")
            
            # Copy entire playlists directory
            shutil.copytree(self.playlists_dir, backup_path, dirs_exist_ok=True)
            
            # Create backup info file
            backup_info = {
                "created": self._get_timestamp(),
                "source": str(self.playlists_dir.absolute()),
                "playlist_count": len(list(self.playlists_dir.iterdir())),
                "total_size": self._get_directory_size(self.playlists_dir)
            }
            
            info_path = backup_path / "backup_info.json"
            with open(info_path, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Backup created: {backup_path}")
            print(f"   📊 {backup_info['playlist_count']} playlists")
            print(f"   💾 {backup_info['total_size']:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def restore_playlists(self, backup_dir: str) -> bool:
        """Restore playlists from backup"""
        backup_path = Path(backup_dir)
        
        if not backup_path.exists():
            print(f"❌ Backup directory not found: {backup_dir}")
            return False
        
        try:
            print(f"🔄 Restoring playlists from backup...")
            
            # Create backup of current playlists first
            if self.playlists_dir.exists():
                current_backup = f"current_backup_{int(time.time())}"
                shutil.copytree(self.playlists_dir, current_backup)
                print(f"✅ Current playlists backed up to: {current_backup}")
            
            # Remove current playlists directory
            if self.playlists_dir.exists():
                shutil.rmtree(self.playlists_dir)
            
            # Copy backup to playlists directory
            shutil.copytree(backup_path, self.playlists_dir)
            
            # Remove backup info file if it exists
            info_path = self.playlists_dir / "backup_info.json"
            if info_path.exists():
                info_path.unlink()
            
            print(f"✅ Playlists restored successfully")
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def analyze_playlists(self) -> Dict:
        """Analyze playlist structure and provide statistics"""
        if not self.playlists_dir.exists():
            return {"error": "Playlists directory not found"}
        
        stats = {
            "total_playlists": 0,
            "total_tracks": 0,
            "total_size_mb": 0.0,
            "formats": {},
            "empty_playlists": [],
            "large_playlists": [],
            "playlist_details": {}
        }
        
        print("📊 Analyzing playlists...")
        
        for playlist_dir in self.playlists_dir.iterdir():
            if not playlist_dir.is_dir():
                continue
            
            stats["total_playlists"] += 1
            playlist_name = playlist_dir.name
            
            # Count tracks and analyze
            tracks = list(playlist_dir.glob('*'))
            music_tracks = [t for t in tracks if t.suffix.lower() in self.supported_formats]
            
            playlist_size = sum(t.stat().st_size for t in music_tracks if t.exists())
            playlist_size_mb = playlist_size / (1024 * 1024)
            
            stats["total_tracks"] += len(music_tracks)
            stats["total_size_mb"] += playlist_size_mb
            
            # Track formats
            for track in music_tracks:
                ext = track.suffix.lower()
                stats["formats"][ext] = stats["formats"].get(ext, 0) + 1
            
            # Identify empty/large playlists
            if len(music_tracks) == 0:
                stats["empty_playlists"].append(playlist_name)
            elif len(music_tracks) > 50:
                stats["large_playlists"].append((playlist_name, len(music_tracks)))
            
            # Store playlist details
            stats["playlist_details"][playlist_name] = {
                "track_count": len(music_tracks),
                "size_mb": playlist_size_mb,
                "has_descriptor": (playlist_dir / "playlist.json").exists()
            }
        
        return stats
    
    def print_analysis(self, stats: Dict):
        """Print formatted playlist analysis"""
        print("\n" + "=" * 50)
        print("📊 PLAYLIST ANALYSIS REPORT")
        print("=" * 50)
        
        if "error" in stats:
            print(f"❌ {stats['error']}")
            return
        
        print(f"📁 Total Playlists: {stats['total_playlists']}")
        print(f"🎵 Total Tracks: {stats['total_tracks']}")
        print(f"💾 Total Size: {stats['total_size_mb']:.1f} MB")
        
        print(f"\n🎶 Format Distribution:")
        for fmt, count in sorted(stats['formats'].items()):
            percentage = (count / stats['total_tracks']) * 100 if stats['total_tracks'] > 0 else 0
            print(f"   {fmt}: {count} tracks ({percentage:.1f}%)")
        
        if stats['empty_playlists']:
            print(f"\n📭 Empty Playlists ({len(stats['empty_playlists'])}):")
            for playlist in stats['empty_playlists']:
                print(f"   - {playlist}")
        
        if stats['large_playlists']:
            print(f"\n📈 Large Playlists (>50 tracks):")
            for playlist, count in sorted(stats['large_playlists'], key=lambda x: x[1], reverse=True):
                print(f"   - {playlist}: {count} tracks")
        
        print(f"\n📋 Playlist Details:")
        for name, details in stats['playlist_details'].items():
            descriptor_status = "✅" if details['has_descriptor'] else "❌"
            print(f"   {name}: {details['track_count']} tracks, {details['size_mb']:.1f} MB {descriptor_status}")
    
    def clean_empty_playlists(self) -> int:
        """Remove empty playlist directories"""
        removed_count = 0
        
        for playlist_dir in self.playlists_dir.iterdir():
            if not playlist_dir.is_dir():
                continue
            
            # Check if playlist has any music files
            music_files = [f for f in playlist_dir.iterdir() 
                          if f.is_file() and f.suffix.lower() in self.supported_formats]
            
            if not music_files:
                print(f"🗑️  Removing empty playlist: {playlist_dir.name}")
                shutil.rmtree(playlist_dir)
                removed_count += 1
        
        return removed_count
    
    def _load_or_create_descriptor(self, descriptor_path: Path, playlist_name: str) -> Dict:
        """Load existing descriptor or create new one"""
        if descriptor_path.exists():
            try:
                with open(descriptor_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "display_name": playlist_name,
            "description": f"Auto-generated playlist for {playlist_name}",
            "created": self._get_timestamp(),
            "tracks": {}
        }
    
    def _make_safe_filename(self, name: str) -> str:
        """Make a string safe for use as filename"""
        invalid_chars = '<>:"/\\|?*'
        safe_name = ''.join(c for c in name if c not in invalid_chars)
        return safe_name.strip()[:100]  # Limit length
    
    def _get_directory_size(self, directory: Path) -> float:
        """Get directory size in MB"""
        total_size = sum(f.stat().st_size for f in directory.rglob('*') if f.is_file())
        return total_size / (1024 * 1024)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

def main():
    """Command-line interface for utilities"""
    parser = argparse.ArgumentParser(description="CustoMusic Utilities")
    parser.add_argument("--playlists-dir", default="playlists", 
                       help="Playlists directory (default: playlists)")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import music from directory')
    import_parser.add_argument('source', help='Source directory containing music')
    import_parser.add_argument('--by-artist', action='store_true',
                              help='Organize by artist instead of folder structure')
    import_parser.add_argument('--link', action='store_true',
                              help='Link files instead of copying')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup playlists')
    backup_parser.add_argument('--output', help='Backup directory name')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('backup_dir', help='Backup directory to restore from')
    
    # Analyze command
    subparsers.add_parser('analyze', help='Analyze playlist structure')
    
    # Clean command
    subparsers.add_parser('clean', help='Remove empty playlists')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan directory for music')
    scan_parser.add_argument('directory', help='Directory to scan')
    scan_parser.add_argument('--by-artist', action='store_true',
                            help='Organize by artist')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    utils = MusicPlayerUtils(args.playlists_dir)
    
    if args.command == 'import':
        utils.import_music(args.source, args.by_artist, not args.link)
    
    elif args.command == 'backup':
        utils.backup_playlists(args.output)
    
    elif args.command == 'restore':
        utils.restore_playlists(args.backup_dir)
    
    elif args.command == 'analyze':
        stats = utils.analyze_playlists()
        utils.print_analysis(stats)
    
    elif args.command == 'clean':
        removed = utils.clean_empty_playlists()
        print(f"✅ Removed {removed} empty playlists")
    
    elif args.command == 'scan':
        organized = utils.scan_music_directory(args.directory, args.by_artist)
        print(f"\n📋 Found {len(organized)} potential playlists:")
        for name, files in organized.items():
            print(f"   📁 {name}: {len(files)} files")

if __name__ == "__main__":
    main()