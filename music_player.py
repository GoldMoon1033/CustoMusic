#!/usr/bin/env python3
"""
Music Player Engine
Handles audio playback using pygame with support for multiple formats.
"""

import pygame
import threading
import time
import os
from pathlib import Path

class MusicPlayerEngine:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        
        # Player state
        self.current_track = None
        self.is_loaded_flag = False
        self.is_playing = False
        self.is_paused = False
        self.position = 0.0
        self.duration = 0.0
        self.volume = 0.7
        self.speed = 1.0
        
        # Threading
        self.position_thread = None
        self.stop_thread = False
        
        # Callbacks
        self.on_track_end = None
        self.on_position_update = None
        self.on_error = None
        
        # Supported formats
        self.supported_formats = {'.mp3', '.wav', '.ogg', '.flac', '.aiff', '.wma', '.agg'}
        
        # Start position tracking thread
        self.start_position_tracking()
    
    def load_track(self, track_path):
        """Load a music track for playback"""
        try:
            track_path = Path(track_path)
            
            # Check if file exists
            if not track_path.exists():
                self._handle_error(f"File not found: {track_path}")
                return False
            
            # Check if format is supported
            if track_path.suffix.lower() not in self.supported_formats:
                self._handle_error(f"Unsupported format: {track_path.suffix}")
                return False
            
            # Stop current playback
            self.stop()
            
            # Load the track
            pygame.mixer.music.load(str(track_path))
            
            self.current_track = str(track_path)
            self.is_loaded_flag = True
            self.position = 0.0
            
            # Try to get duration (this is approximate for some formats)
            self.duration = self._get_track_duration(track_path)
            
            return True
            
        except pygame.error as e:
            self._handle_error(f"Failed to load track: {e}")
            return False
        except Exception as e:
            self._handle_error(f"Unexpected error loading track: {e}")
            return False
    
    def play(self):
        """Start playback"""
        try:
            if not self.is_loaded_flag:
                return False
            
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play(start=self.position)
            
            self.is_playing = True
            pygame.mixer.music.set_volume(self.volume)
            
            return True
            
        except pygame.error as e:
            self._handle_error(f"Failed to start playback: {e}")
            return False
    
    def pause(self):
        """Pause playback"""
        try:
            if self.is_playing and not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                return True
            return False
        except pygame.error as e:
            self._handle_error(f"Failed to pause: {e}")
            return False
    
    def stop(self):
        """Stop playback"""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.position = 0.0
            return True
        except pygame.error as e:
            self._handle_error(f"Failed to stop: {e}")
            return False
    
    def set_volume(self, volume):
        """Set playback volume (0.0 to 1.0)"""
        try:
            self.volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(self.volume)
        except pygame.error as e:
            self._handle_error(f"Failed to set volume: {e}")
    
    def set_speed(self, speed):
        """Set playback speed (0.5 to 2.0)"""
        # Note: pygame doesn't natively support speed control
        # This is a placeholder for future implementation with other libraries
        self.speed = max(0.5, min(2.0, speed))
        
        # For now, we'll just store the speed value
        # In a full implementation, you might use pydub or another library
        # that supports speed/pitch control
    
    def set_position(self, position):
        """Set playback position in seconds"""
        try:
            if not self.is_loaded_flag:
                return False
            
            # pygame.mixer.music doesn't support seeking directly
            # This is a limitation - in a full implementation you'd use
            # a library like python-vlc or implement with pydub
            
            # For now, we'll restart from the beginning if position is 0
            if position == 0:
                was_playing = self.is_playing
                self.stop()
                if was_playing:
                    self.play()
                return True
            
            # Store position for tracking
            self.position = max(0.0, min(self.duration, position))
            return True
            
        except Exception as e:
            self._handle_error(f"Failed to set position: {e}")
            return False
    
    def get_position(self):
        """Get current playback position in seconds"""
        return self.position
    
    def get_duration(self):
        """Get track duration in seconds"""
        return self.duration
    
    def is_loaded(self):
        """Check if a track is loaded"""
        return self.is_loaded_flag
    
    def is_playing_status(self):
        """Check if currently playing"""
        return self.is_playing and not self.is_paused
    
    def get_track_info(self):
        """Get information about current track"""
        if not self.current_track:
            return None
        
        track_path = Path(self.current_track)
        
        info = {
            'filename': track_path.name,
            'path': str(track_path),
            'format': track_path.suffix.lower(),
            'duration': self.duration,
            'position': self.position
        }
        
        # Try to get additional metadata using mutagen
        try:
            from mutagen import File
            
            audio_file = File(self.current_track)
            if audio_file is not None:
                info['title'] = str(audio_file.get('TIT2', [track_path.stem])[0]) if 'TIT2' in audio_file else track_path.stem
                info['artist'] = str(audio_file.get('TPE1', ['Unknown'])[0]) if 'TPE1' in audio_file else 'Unknown'
                info['album'] = str(audio_file.get('TALB', ['Unknown'])[0]) if 'TALB' in audio_file else 'Unknown'
            else:
                info['title'] = track_path.stem
                info['artist'] = 'Unknown'
                info['album'] = 'Unknown'
                
        except ImportError:
            # mutagen not available
            info['title'] = track_path.stem
            info['artist'] = 'Unknown'
            info['album'] = 'Unknown'
        except Exception:
            # Error reading metadata
            info['title'] = track_path.stem
            info['artist'] = 'Unknown'
            info['album'] = 'Unknown'
        
        return info
    
    def _get_track_duration(self, track_path):
        """Get track duration using mutagen if available"""
        try:
            from mutagen import File
            
            audio_file = File(str(track_path))
            if audio_file is not None and hasattr(audio_file, 'info'):
                return float(audio_file.info.length)
            
        except ImportError:
            pass  # mutagen not available
        except Exception:
            pass  # Error reading file
        
        # Fallback: estimate based on file size (very rough)
        try:
            file_size = track_path.stat().st_size
            # Very rough estimate: assume 128kbps MP3 equivalent
            estimated_duration = file_size / (128 * 1024 / 8)  # bytes per second
            return min(estimated_duration, 3600)  # Cap at 1 hour
        except:
            return 180.0  # Default to 3 minutes if all else fails
    
    def start_position_tracking(self):
        """Start the position tracking thread"""
        def position_tracker():
            while not self.stop_thread:
                try:
                    if self.is_playing and not self.is_paused:
                        # Check if music is still playing
                        if not pygame.mixer.music.get_busy():
                            # Track has ended
                            self.is_playing = False
                            self.is_paused = False
                            if self.on_track_end:
                                self.on_track_end()
                        else:
                            # Update position (approximate)
                            self.position += 1.0
                            if self.position >= self.duration:
                                self.position = self.duration
                        
                        # Notify position update
                        if self.on_position_update:
                            self.on_position_update(self.position, self.duration)
                    
                    time.sleep(1.0)  # Update every second
                    
                except Exception as e:
                    if not self.stop_thread:  # Only log if we're not shutting down
                        print(f"Position tracking error: {e}")
                    time.sleep(1.0)
        
        self.position_thread = threading.Thread(target=position_tracker, daemon=True)
        self.position_thread.start()
    
    def _handle_error(self, error_msg):
        """Handle errors and notify callback"""
        print(f"Player Error: {error_msg}")
        if self.on_error:
            self.on_error(error_msg)
    
    def get_supported_formats(self):
        """Get list of supported audio formats"""
        return list(self.supported_formats)
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_thread = True
        self.stop()
        
        # Wait for position thread to finish
        if self.position_thread and self.position_thread.is_alive():
            self.position_thread.join(timeout=2.0)
        
        try:
            pygame.mixer.quit()
        except:
            pass
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()