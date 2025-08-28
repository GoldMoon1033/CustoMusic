#!/usr/bin/env python3
"""
Settings Manager
Handles application settings including color themes and user preferences.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

class SettingsManager:
    def __init__(self, config_dir=None):
        # Set up configuration directory
        if config_dir is None:
            config_dir = Path.home() / '.music_player'
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.settings_file = self.config_dir / 'settings.json'
        
        # Default settings
        self.default_settings = {
            # Color theme
            'primary_color': '#4a90e2',      # Blue
            'secondary_color': '#2c3e50',    # Dark blue-gray
            'background_color': '#f8f9fa',   # Light gray
            'text_color': '#2c3e50',         # Dark text
            'accent_color': '#e74c3c',       # Red accent
            
            # Player settings
            'default_volume': 70,
            'default_speed': 1.0,
            'remember_position': True,
            'auto_advance': True,
            'shuffle_mode': False,
            'loop_playlist': False,
            'loop_single': False,
            
            # UI settings
            'window_width': 1000,
            'window_height': 700,
            'collapsed_playlists': False,
            'collapsed_tracks': False,
            'show_tooltips': True,
            'font_size': 10,
            
            # Playlist settings
            'auto_refresh': True,
            'show_file_extensions': False,
            'sort_playlists_alphabetically': True,
            'sort_tracks_by_order': True,
            
            # Advanced settings
            'buffer_size': 1024,
            'crossfade_duration': 0,
            'preload_next_track': False,
            'scan_subfolders': True,
            
            # Last session
            'last_playlist': '',
            'last_track': '',
            'last_position': 0.0,
            'last_volume': 70,
            'last_speed': 1.0
        }
        
        # Load settings
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        settings = self.default_settings.copy()
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                    settings.update(user_settings)
            except Exception as e:
                print(f"Error loading settings: {e}")
                # If there's an error, backup the corrupted file
                try:
                    backup_path = self.settings_file.with_suffix('.json.backup')
                    self.settings_file.rename(backup_path)
                    print(f"Corrupted settings backed up to {backup_path}")
                except:
                    pass
        
        return settings
    
    def save_settings(self) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key: str, default=None) -> Any:
        """Get a specific setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set a specific setting value"""
        self.settings[key] = value
    
    def reset_setting(self, key: str):
        """Reset a setting to its default value"""
        if key in self.default_settings:
            self.settings[key] = self.default_settings[key]
    
    def reset_all_settings(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
    
    def get_color_theme(self) -> Dict[str, str]:
        """Get the current color theme"""
        return {
            'primary': self.get_setting('primary_color'),
            'secondary': self.get_setting('secondary_color'),
            'background': self.get_setting('background_color'),
            'text': self.get_setting('text_color'),
            'accent': self.get_setting('accent_color')
        }
    
    def set_color_theme(self, theme: Dict[str, str]):
        """Set the color theme"""
        color_mappings = {
            'primary': 'primary_color',
            'secondary': 'secondary_color',
            'background': 'background_color',
            'text': 'text_color',
            'accent': 'accent_color'
        }
        
        for theme_key, setting_key in color_mappings.items():
            if theme_key in theme:
                self.set_setting(setting_key, theme[theme_key])
    
    def reset_colors(self):
        """Reset color theme to defaults"""
        color_keys = ['primary_color', 'secondary_color', 'background_color', 
                     'text_color', 'accent_color']
        for key in color_keys:
            self.reset_setting(key)
    
    def validate_hex_color(self, color: str) -> bool:
        """Validate hex color format"""
        if not color.startswith('#'):
            return False
        
        if len(color) not in [4, 7]:  # #RGB or #RRGGBB
            return False
        
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False
    
    def normalize_hex_color(self, color: str) -> str:
        """Normalize hex color to #RRGGBB format"""
        if not self.validate_hex_color(color):
            return self.default_settings['primary_color']
        
        if len(color) == 4:  # #RGB -> #RRGGBB
            r, g, b = color[1], color[2], color[3]
            return f"#{r}{r}{g}{g}{b}{b}"
        
        return color.upper()
    
    def get_preset_themes(self) -> Dict[str, Dict[str, str]]:
        """Get predefined color themes"""
        return {
            'Default': {
                'primary': '#4a90e2',
                'secondary': '#2c3e50',
                'background': '#f8f9fa',
                'text': '#2c3e50',
                'accent': '#e74c3c'
            },
            'Dark': {
                'primary': '#34495e',
                'secondary': '#2c3e50',
                'background': '#1e1e1e',
                'text': '#ecf0f1',
                'accent': '#e67e22'
            },
            'Ocean': {
                'primary': '#3498db',
                'secondary': '#2980b9',
                'background': '#ecf0f1',
                'text': '#2c3e50',
                'accent': '#1abc9c'
            },
            'Forest': {
                'primary': '#27ae60',
                'secondary': '#229954',
                'background': '#f8f9fa',
                'text': '#2c3e50',
                'accent': '#f39c12'
            },
            'Sunset': {
                'primary': '#e67e22',
                'secondary': '#d35400',
                'background': '#fdf2e9',
                'text': '#2c3e50',
                'accent': '#e74c3c'
            },
            'Purple': {
                'primary': '#9b59b6',
                'secondary': '#8e44ad',
                'background': '#f4f1f5',
                'text': '#2c3e50',
                'accent': '#e91e63'
            },
            'Monochrome': {
                'primary': '#5d6d7e',
                'secondary': '#34495e',
                'background': '#f8f9fa',
                'text': '#2c3e50',
                'accent': '#95a5a6'
            }
        }
    
    def apply_preset_theme(self, theme_name: str) -> bool:
        """Apply a preset theme"""
        presets = self.get_preset_themes()
        
        if theme_name in presets:
            self.set_color_theme(presets[theme_name])
            return True
        
        return False
    
    def save_window_state(self, width: int, height: int, x: int = None, y: int = None):
        """Save window dimensions and position"""
        self.set_setting('window_width', width)
        self.set_setting('window_height', height)
        
        if x is not None:
            self.set_setting('window_x', x)
        if y is not None:
            self.set_setting('window_y', y)
    
    def get_window_state(self) -> Dict[str, int]:
        """Get saved window state"""
        return {
            'width': self.get_setting('window_width', 1000),
            'height': self.get_setting('window_height', 700),
            'x': self.get_setting('window_x'),
            'y': self.get_setting('window_y')
        }
    
    def save_player_state(self, playlist: str = None, track: str = None, 
                         position: float = None, volume: int = None, speed: float = None):
        """Save current player state"""
        if playlist is not None:
            self.set_setting('last_playlist', playlist)
        if track is not None:
            self.set_setting('last_track', track)
        if position is not None:
            self.set_setting('last_position', position)
        if volume is not None:
            self.set_setting('last_volume', volume)
        if speed is not None:
            self.set_setting('last_speed', speed)
    
    def get_player_state(self) -> Dict[str, Any]:
        """Get saved player state"""
        return {
            'playlist': self.get_setting('last_playlist', ''),
            'track': self.get_setting('last_track', ''),
            'position': self.get_setting('last_position', 0.0),
            'volume': self.get_setting('last_volume', 70),
            'speed': self.get_setting('last_speed', 1.0)
        }
    
    def save_ui_state(self, collapsed_playlists: bool = None, collapsed_tracks: bool = None):
        """Save UI collapse states"""
        if collapsed_playlists is not None:
            self.set_setting('collapsed_playlists', collapsed_playlists)
        if collapsed_tracks is not None:
            self.set_setting('collapsed_tracks', collapsed_tracks)
    
    def get_ui_state(self) -> Dict[str, bool]:
        """Get saved UI state"""
        return {
            'collapsed_playlists': self.get_setting('collapsed_playlists', False),
            'collapsed_tracks': self.get_setting('collapsed_tracks', False)
        }
    
    def export_settings(self, export_path: str = None) -> bool:
        """Export settings to a file"""
        if export_path is None:
            export_path = self.config_dir / 'settings_export.json'
        else:
            export_path = Path(export_path)
        
        try:
            export_data = {
                'settings': self.settings,
                'export_version': '1.0',
                'export_timestamp': self._get_timestamp()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_path: str) -> bool:
        """Import settings from a file"""
        import_path = Path(import_path)
        
        if not import_path.exists():
            return False
        
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'settings' in import_data:
                # Validate imported settings against defaults
                imported_settings = {}
                for key, value in import_data['settings'].items():
                    if key in self.default_settings:
                        # Validate color values
                        if key.endswith('_color') and isinstance(value, str):
                            if self.validate_hex_color(value):
                                imported_settings[key] = self.normalize_hex_color(value)
                        else:
                            imported_settings[key] = value
                
                self.settings.update(imported_settings)
                return True
                
        except Exception as e:
            print(f"Error importing settings: {e}")
        
        return False
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get debug information about settings"""
        return {
            'config_dir': str(self.config_dir),
            'settings_file': str(self.settings_file),
            'settings_file_exists': self.settings_file.exists(),
            'total_settings': len(self.settings),
            'custom_settings': len([k for k in self.settings.keys() 
                                  if k not in self.default_settings]),
            'config_dir_writable': os.access(self.config_dir, os.W_OK)
        }