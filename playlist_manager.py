#!/usr/bin/env python3
"""
Playlist Manager
Handles playlist folder structure and descriptor files for custom naming and ordering.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

class PlaylistManager:
    def __init__(self, playlists_dir="playlists"):
        self.playlists_dir = Path(playlists_dir)
        self.descriptor_filename = "playlist.json"
        
        # Supported audio formats
        self.audio_extensions = {
            '.mp3', '.wav', '.flac', '.ogg', '.wma', '.aiff', '.agg'
        }
        
        # Ensure playlists directory exists
        self.playlists_dir.mkdir(exist_ok=True)
        
        # Initialize descriptors for all playlists
        self.initialize_descriptors()
    
    def initialize_descriptors(self):
        """Initialize descriptor files for all playlist folders"""
        for item in self.playlists_dir.iterdir():
            if item.is_dir():
                self._ensure_descriptor_exists(item)
    
    def _ensure_descriptor_exists(self, playlist_dir: Path):
        """Ensure a descriptor file exists for a playlist directory"""
        descriptor_path = playlist_dir / self.descriptor_filename
        
        if not descriptor_path.exists():
            # Get all audio files in the directory
            audio_files = self._get_audio_files(playlist_dir)
            
            # Create default descriptor
            descriptor = {
                "display_name": playlist_dir.name,
                "description": f"Auto-generated playlist for {playlist_dir.name}",
                "created": self._get_timestamp(),
                "tracks": {}
            }
            
            # Add track entries with default display names
            for i, audio_file in enumerate(audio_files, 1):
                relative_path = audio_file.relative_to(playlist_dir)
                descriptor["tracks"][str(relative_path)] = {
                    "display_name": audio_file.stem,
                    "order": i,
                    "added": self._get_timestamp()
                }
            
            # Save descriptor
            try:
                with open(descriptor_path, 'w', encoding='utf-8') as f:
                    json.dump(descriptor, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Failed to create descriptor for {playlist_dir.name}: {e}")
    
    def _get_audio_files(self, directory: Path) -> List[Path]:
        """Get all audio files in a directory, sorted by name"""
        audio_files = []
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.audio_extensions:
                audio_files.append(file_path)
        
        # Sort by name
        audio_files.sort(key=lambda x: x.name.lower())
        return audio_files
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def get_playlists(self) -> Dict[str, Dict]:
        """Get all available playlists with their metadata"""
        playlists = {}
        
        for item in self.playlists_dir.iterdir():
            if item.is_dir():
                descriptor = self._load_descriptor(item)
                if descriptor:
                    playlists[item.name] = descriptor
        
        return playlists
    
    def _load_descriptor(self, playlist_dir: Path) -> Optional[Dict]:
        """Load descriptor file for a playlist"""
        descriptor_path = playlist_dir / self.descriptor_filename
        
        try:
            if descriptor_path.exists():
                with open(descriptor_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load descriptor for {playlist_dir.name}: {e}")
        
        return None
    
    def get_playlist_display_name(self, playlist_name: str) -> str:
        """Get display name for a playlist"""
        playlist_dir = self.playlists_dir / playlist_name
        descriptor = self._load_descriptor(playlist_dir)
        
        if descriptor and 'display_name' in descriptor:
            return descriptor['display_name']
        
        return playlist_name
    
    def get_playlist_tracks(self, playlist_name: str) -> List[Path]:
        """Get ordered list of tracks in a playlist"""
        playlist_dir = self.playlists_dir / playlist_name
        
        if not playlist_dir.exists():
            return []
        
        descriptor = self._load_descriptor(playlist_dir)
        
        if descriptor and 'tracks' in descriptor:
            # Get tracks from descriptor with ordering
            track_entries = []
            
            for relative_path, track_info in descriptor['tracks'].items():
                full_path = playlist_dir / relative_path
                if full_path.exists():
                    order = track_info.get('order', 999)
                    track_entries.append((order, full_path))
            
            # Sort by order
            track_entries.sort(key=lambda x: x[0])
            return [track[1] for track in track_entries]
        
        else:
            # Fallback: return all audio files in directory
            return self._get_audio_files(playlist_dir)
    
    def get_track_display_name(self, playlist_name: str, track_path: Path) -> str:
        """Get display name for a track"""
        playlist_dir = self.playlists_dir / playlist_name
        descriptor = self._load_descriptor(playlist_dir)
        
        if descriptor and 'tracks' in descriptor:
            # Get relative path from playlist directory
            try:
                relative_path = track_path.relative_to(playlist_dir)
                track_info = descriptor['tracks'].get(str(relative_path))
                
                if track_info and 'display_name' in track_info:
                    return track_info['display_name']
            except ValueError:
                pass  # track_path is not relative to playlist_dir
        
        # Fallback to filename without extension
        return track_path.stem
    
    def update_playlist_descriptor(self, playlist_name: str, **kwargs):
        """Update playlist descriptor with new information"""
        playlist_dir = self.playlists_dir / playlist_name
        descriptor_path = playlist_dir / self.descriptor_filename
        
        if not playlist_dir.exists():
            return False
        
        # Load existing descriptor or create new one
        descriptor = self._load_descriptor(playlist_dir) or {
            "display_name": playlist_name,
            "description": "",
            "created": self._get_timestamp(),
            "tracks": {}
        }
        
        # Update with provided values
        for key, value in kwargs.items():
            if key in ['display_name', 'description']:
                descriptor[key] = value
        
        descriptor['modified'] = self._get_timestamp()
        
        try:
            with open(descriptor_path, 'w', encoding='utf-8') as f:
                json.dump(descriptor, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to update descriptor for {playlist_name}: {e}")
            return False
    
    def update_track_info(self, playlist_name: str, track_path: Path, **kwargs):
        """Update track information in playlist descriptor"""
        playlist_dir = self.playlists_dir / playlist_name
        descriptor_path = playlist_dir / self.descriptor_filename
        
        if not playlist_dir.exists():
            return False
        
        descriptor = self._load_descriptor(playlist_dir)
        if not descriptor:
            return False
        
        try:
            relative_path = track_path.relative_to(playlist_dir)
            relative_path_str = str(relative_path)
            
            if 'tracks' not in descriptor:
                descriptor['tracks'] = {}
            
            if relative_path_str not in descriptor['tracks']:
                descriptor['tracks'][relative_path_str] = {
                    'display_name': track_path.stem,
                    'order': len(descriptor['tracks']) + 1,
                    'added': self._get_timestamp()
                }
            
            # Update with provided values
            track_info = descriptor['tracks'][relative_path_str]
            for key, value in kwargs.items():
                if key in ['display_name', 'order']:
                    track_info[key] = value
            
            track_info['modified'] = self._get_timestamp()
            descriptor['modified'] = self._get_timestamp()
            
            with open(descriptor_path, 'w', encoding='utf-8') as f:
                json.dump(descriptor, f, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            print(f"Failed to update track info: {e}")
            return False
    
    def refresh_playlist(self, playlist_name: str):
        """Refresh playlist by scanning for new files and updating descriptor"""
        playlist_dir = self.playlists_dir / playlist_name
        
        if not playlist_dir.exists():
            return False
        
        # Get current audio files
        current_files = self._get_audio_files(playlist_dir)
        
        # Load existing descriptor
        descriptor = self._load_descriptor(playlist_dir) or {
            "display_name": playlist_name,
            "description": f"Playlist for {playlist_name}",
            "created": self._get_timestamp(),
            "tracks": {}
        }
        
        # Get existing tracks
        existing_tracks = set(descriptor.get('tracks', {}).keys())
        
        # Find new files
        current_relative_paths = set()
        for file_path in current_files:
            relative_path = str(file_path.relative_to(playlist_dir))
            current_relative_paths.add(relative_path)
            
            # Add new tracks
            if relative_path not in existing_tracks:
                descriptor['tracks'][relative_path] = {
                    'display_name': file_path.stem,
                    'order': len(descriptor['tracks']) + 1,
                    'added': self._get_timestamp()
                }
        
        # Remove tracks for files that no longer exist
        tracks_to_remove = existing_tracks - current_relative_paths
        for track_path in tracks_to_remove:
            del descriptor['tracks'][track_path]
        
        # Update timestamp
        descriptor['modified'] = self._get_timestamp()
        
        # Save updated descriptor
        descriptor_path = playlist_dir / self.descriptor_filename
        try:
            with open(descriptor_path, 'w', encoding='utf-8') as f:
                json.dump(descriptor, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to refresh playlist {playlist_name}: {e}")
            return False
    
    def create_playlist(self, playlist_name: str, display_name: str = None, description: str = ""):
        """Create a new playlist folder with descriptor"""
        playlist_dir = self.playlists_dir / playlist_name
        
        if playlist_dir.exists():
            return False  # Playlist already exists
        
        try:
            playlist_dir.mkdir()
            
            descriptor = {
                "display_name": display_name or playlist_name,
                "description": description,
                "created": self._get_timestamp(),
                "tracks": {}
            }
            
            descriptor_path = playlist_dir / self.descriptor_filename
            with open(descriptor_path, 'w', encoding='utf-8') as f:
                json.dump(descriptor, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Failed to create playlist {playlist_name}: {e}")
            return False
    
    def get_playlist_stats(self, playlist_name: str) -> Dict:
        """Get statistics about a playlist"""
        playlist_dir = self.playlists_dir / playlist_name
        
        if not playlist_dir.exists():
            return {}
        
        tracks = self.get_playlist_tracks(playlist_name)
        descriptor = self._load_descriptor(playlist_dir)
        
        stats = {
            'track_count': len(tracks),
            'total_size': 0,
            'formats': set(),
            'created': descriptor.get('created') if descriptor else None,
            'modified': descriptor.get('modified') if descriptor else None
        }
        
        for track_path in tracks:
            try:
                if track_path.exists():
                    stats['total_size'] += track_path.stat().st_size
                    stats['formats'].add(track_path.suffix.lower())
            except:
                continue
        
        stats['formats'] = list(stats['formats'])
        stats['total_size_mb'] = round(stats['total_size'] / (1024 * 1024), 2)
        
        return stats
    
    def reorder_tracks(self, playlist_name: str, track_order: List[str]):
        """Reorder tracks in a playlist"""
        playlist_dir = self.playlists_dir / playlist_name
        descriptor = self._load_descriptor(playlist_dir)
        
        if not descriptor or 'tracks' not in descriptor:
            return False
        
        try:
            # Update order for each track
            for i, relative_path in enumerate(track_order, 1):
                if relative_path in descriptor['tracks']:
                    descriptor['tracks'][relative_path]['order'] = i
            
            descriptor['modified'] = self._get_timestamp()
            
            # Save updated descriptor
            descriptor_path = playlist_dir / self.descriptor_filename
            with open(descriptor_path, 'w', encoding='utf-8') as f:
                json.dump(descriptor, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Failed to reorder tracks in {playlist_name}: {e}")
            return False
    
    def export_playlist(self, playlist_name: str, format='m3u') -> Optional[str]:
        """Export playlist to standard format"""
        if format not in ['m3u', 'pls']:
            return None
        
        tracks = self.get_playlist_tracks(playlist_name)
        if not tracks:
            return None
        
        playlist_dir = self.playlists_dir / playlist_name
        export_path = playlist_dir / f"{playlist_name}.{format}"
        
        try:
            if format == 'm3u':
                with open(export_path, 'w', encoding='utf-8') as f:
                    f.write("#EXTM3U\n")
                    for track_path in tracks:
                        display_name = self.get_track_display_name(playlist_name, track_path)
                        f.write(f"#EXTINF:-1,{display_name}\n")
                        f.write(f"{track_path.absolute()}\n")
            
            elif format == 'pls':
                with open(export_path, 'w', encoding='utf-8') as f:
                    f.write("[playlist]\n")
                    for i, track_path in enumerate(tracks, 1):
                        f.write(f"File{i}={track_path.absolute()}\n")
                        display_name = self.get_track_display_name(playlist_name, track_path)
                        f.write(f"Title{i}={display_name}\n")
                        f.write(f"Length{i}=-1\n")
                    f.write(f"NumberOfEntries={len(tracks)}\n")
                    f.write("Version=2\n")
            
            return str(export_path)
            
        except Exception as e:
            print(f"Failed to export playlist {playlist_name}: {e}")
            return None