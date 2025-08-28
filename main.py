#!/usr/bin/env python3
"""
CustoMusic - Main Application
A feature-rich music player with playlist management and customizable UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import os
import sys
from pathlib import Path

# Import our custom modules
from music_player import MusicPlayerEngine
from playlist_manager import PlaylistManager
from settings_manager import SettingsManager
from ui_components import ScrollableFrame, CustomButton, PlaybackControls

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CustoMusic")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Initialize components
        self.settings = SettingsManager()
        self.playlist_manager = PlaylistManager()
        self.player = MusicPlayerEngine()
        
        # UI Variables
        self.current_playlist = tk.StringVar()
        self.current_track = tk.StringVar()
        self.position_var = tk.StringVar(value="00:00 / 00:00")
        self.volume_var = tk.DoubleVar(value=70)
        self.speed_var = tk.DoubleVar(value=1.0)
        
        # Playback state
        self.is_playing = False
        self.shuffle_mode = False
        self.loop_playlist = False
        self.loop_single = False
        self.current_playlist_name = ""
        self.current_track_index = 0
        
        # UI Elements
        self.playlist_frame = None
        self.track_frame = None
        self.collapsed_states = {'playlists': False, 'tracks': False}
        
        # Setup UI and callbacks
        self.setup_ui()
        self.setup_callbacks()
        self.apply_color_theme()
        
        # Load playlists
        self.load_playlists()
        
        # Setup update timer
        self.update_timer()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create main frames
        self.create_main_layout()
        self.create_menu_bar()
        self.create_playlist_section()
        self.create_track_section()
        self.create_player_controls()
        self.create_status_bar()
    
    def create_main_layout(self):
        """Create the main layout structure"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Top control panel
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        # Left panel (playlists)
        self.left_frame = ttk.LabelFrame(self.main_frame, text="Playlists", padding=5)
        self.left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(1, weight=1)
        
        # Right panel (tracks)
        self.right_frame = ttk.LabelFrame(self.main_frame, text="Tracks", padding=5)
        self.right_frame.grid(row=1, column=1, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)
        
        # Bottom control panel
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
    
    def create_menu_bar(self):
        """Create menu bar"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Playlists", command=self.load_playlists)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # View menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Playlists", command=lambda: self.toggle_section('playlists'))
        view_menu.add_command(label="Toggle Tracks", command=lambda: self.toggle_section('tracks'))
        
        # Playback menu
        playback_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Playback", menu=playback_menu)
        playback_menu.add_command(label="Play/Pause", command=self.toggle_playback)
        playback_menu.add_command(label="Next", command=self.next_track)
        playback_menu.add_command(label="Previous", command=self.previous_track)
        playback_menu.add_separator()
        playback_menu.add_checkbutton(label="Shuffle", variable=tk.BooleanVar(), 
                                     command=self.toggle_shuffle)
        playback_menu.add_checkbutton(label="Loop Playlist", variable=tk.BooleanVar(),
                                     command=self.toggle_playlist_loop)
        playback_menu.add_checkbutton(label="Loop Single", variable=tk.BooleanVar(),
                                     command=self.toggle_single_loop)
    
    def create_playlist_section(self):
        """Create playlist selection section"""
        # Header with collapse button
        header_frame = ttk.Frame(self.left_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header_frame.columnconfigure(1, weight=1)
        
        self.playlist_collapse_btn = CustomButton(header_frame, text="−", width=3,
                                                 command=lambda: self.toggle_section('playlists'))
        self.playlist_collapse_btn.grid(row=0, column=0, padx=(0, 5))
        
        ttk.Label(header_frame, text="Select Playlist:").grid(row=0, column=1, sticky="w")
        
        # Scrollable playlist listbox
        self.playlist_frame = ScrollableFrame(self.left_frame)
        self.playlist_frame.grid(row=1, column=0, sticky="nsew")
        
        self.playlist_listbox = tk.Listbox(self.playlist_frame.scrollable_frame,
                                          selectmode=tk.SINGLE, height=15)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True)
        self.playlist_listbox.bind('<<ListboxSelect>>', self.on_playlist_select)
    
    def create_track_section(self):
        """Create track selection section"""
        # Header with collapse button
        header_frame = ttk.Frame(self.right_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header_frame.columnconfigure(1, weight=1)
        
        self.track_collapse_btn = CustomButton(header_frame, text="−", width=3,
                                              command=lambda: self.toggle_section('tracks'))
        self.track_collapse_btn.grid(row=0, column=0, padx=(0, 5))
        
        ttk.Label(header_frame, text="Tracks:").grid(row=0, column=1, sticky="w")
        
        # Scrollable track listbox
        self.track_frame = ScrollableFrame(self.right_frame)
        self.track_frame.grid(row=1, column=0, sticky="nsew")
        
        self.track_listbox = tk.Listbox(self.track_frame.scrollable_frame,
                                       selectmode=tk.SINGLE, height=15)
        self.track_listbox.pack(fill=tk.BOTH, expand=True)
        self.track_listbox.bind('<Double-Button-1>', self.on_track_double_click)
        self.track_listbox.bind('<<ListboxSelect>>', self.on_track_select)
    
    def create_player_controls(self):
        """Create player control section"""
        # Playback controls frame
        controls_frame = PlaybackControls(self.bottom_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Main playback buttons
        btn_frame = ttk.Frame(controls_frame)
        btn_frame.pack(pady=5)
        
        self.prev_btn = CustomButton(btn_frame, text="⏮", command=self.previous_track)
        self.prev_btn.pack(side=tk.LEFT, padx=2)
        
        self.rewind_btn = CustomButton(btn_frame, text="⏪", command=self.rewind_track)
        self.rewind_btn.pack(side=tk.LEFT, padx=2)
        
        self.play_btn = CustomButton(btn_frame, text="▶", command=self.toggle_playback)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = CustomButton(btn_frame, text="⏭", command=self.next_track)
        self.next_btn.pack(side=tk.LEFT, padx=2)
        
        # Mode buttons
        mode_frame = ttk.Frame(btn_frame)
        mode_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        self.shuffle_btn = CustomButton(mode_frame, text="🔀", command=self.toggle_shuffle)
        self.shuffle_btn.pack(side=tk.LEFT, padx=2)
        
        self.loop_playlist_btn = CustomButton(mode_frame, text="🔁", command=self.toggle_playlist_loop)
        self.loop_playlist_btn.pack(side=tk.LEFT, padx=2)
        
        self.loop_single_btn = CustomButton(mode_frame, text="🔂", command=self.toggle_single_loop)
        self.loop_single_btn.pack(side=tk.LEFT, padx=2)
        
        # Progress and time
        progress_frame = ttk.Frame(controls_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        progress_frame.columnconfigure(1, weight=1)
        
        ttk.Label(progress_frame, text="Position:").grid(row=0, column=0, sticky="w")
        
        self.progress_scale = ttk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.progress_scale.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        self.progress_scale.bind("<Button-1>", self.on_progress_click)
        
        self.time_label = ttk.Label(progress_frame, textvariable=self.position_var)
        self.time_label.grid(row=0, column=2, sticky="e")
        
        # Volume and speed controls
        controls2_frame = ttk.Frame(controls_frame)
        controls2_frame.pack(fill=tk.X, pady=5)
        
        # Volume control
        vol_frame = ttk.Frame(controls2_frame)
        vol_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(vol_frame, text="Volume:").pack(side=tk.LEFT)
        self.volume_scale = ttk.Scale(vol_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                     variable=self.volume_var, command=self.on_volume_change)
        self.volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        # Speed control
        speed_frame = ttk.Frame(controls2_frame)
        speed_frame.pack(side=tk.RIGHT)
        
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(speed_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                                    variable=self.speed_var, command=self.on_speed_change)
        self.speed_scale.pack(side=tk.LEFT, padx=(5, 0))
        
        speed_label = ttk.Label(speed_frame, text="1.0x")
        speed_label.pack(side=tk.LEFT, padx=(5, 0))
        self.speed_var.trace('w', lambda *args: speed_label.config(text=f"{self.speed_var.get():.1f}x"))
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        self.status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Current track info
        self.track_info_var = tk.StringVar(value="No track selected")
        self.track_info_label = ttk.Label(self.status_frame, textvariable=self.track_info_var)
        self.track_info_label.grid(row=0, column=1, sticky="e")
    
    def setup_callbacks(self):
        """Setup player engine callbacks"""
        self.player.on_track_end = self.on_track_end
        self.player.on_position_update = self.on_position_update
        self.player.on_error = self.on_player_error
    
    def load_playlists(self):
        """Load all playlists from the playlists folder"""
        try:
            playlists = self.playlist_manager.get_playlists()
            
            self.playlist_listbox.delete(0, tk.END)
            for playlist_name in playlists:
                display_name = self.playlist_manager.get_playlist_display_name(playlist_name)
                self.playlist_listbox.insert(tk.END, display_name)
            
            if playlists:
                self.status_var.set(f"Loaded {len(playlists)} playlists")
            else:
                self.status_var.set("No playlists found - create folders in 'playlists' directory")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load playlists: {e}")
            self.status_var.set("Error loading playlists")
    
    def on_playlist_select(self, event):
        """Handle playlist selection"""
        selection = self.playlist_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        playlists = list(self.playlist_manager.get_playlists().keys())
        
        if index < len(playlists):
            playlist_name = playlists[index]
            self.load_playlist_tracks(playlist_name)
    
    def load_playlist_tracks(self, playlist_name):
        """Load tracks from selected playlist"""
        try:
            tracks = self.playlist_manager.get_playlist_tracks(playlist_name)
            
            self.track_listbox.delete(0, tk.END)
            for track_path in tracks:
                display_name = self.playlist_manager.get_track_display_name(playlist_name, track_path)
                self.track_listbox.insert(tk.END, display_name)
            
            self.current_playlist_name = playlist_name
            self.current_playlist.set(self.playlist_manager.get_playlist_display_name(playlist_name))
            self.status_var.set(f"Loaded {len(tracks)} tracks from playlist")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load playlist tracks: {e}")
    
    def on_track_select(self, event):
        """Handle track selection"""
        selection = self.track_listbox.curselection()
        if selection:
            self.current_track_index = selection[0]
    
    def on_track_double_click(self, event):
        """Handle track double-click to play"""
        self.on_track_select(event)
        self.play_selected_track()
    
    def play_selected_track(self):
        """Play the currently selected track"""
        if not self.current_playlist_name:
            return
        
        try:
            tracks = self.playlist_manager.get_playlist_tracks(self.current_playlist_name)
            if self.current_track_index < len(tracks):
                track_path = tracks[self.current_track_index]
                
                if self.player.load_track(track_path):
                    self.player.play()
                    self.is_playing = True
                    self.play_btn.config(text="⏸")
                    
                    track_name = self.playlist_manager.get_track_display_name(
                        self.current_playlist_name, track_path)
                    self.track_info_var.set(f"Playing: {track_name}")
                    self.status_var.set("Playing")
                else:
                    messagebox.showerror("Error", "Failed to load track")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play track: {e}")
    
    def toggle_playback(self):
        """Toggle play/pause"""
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
            self.play_btn.config(text="▶")
            self.status_var.set("Paused")
        else:
            if self.player.is_loaded():
                self.player.play()
                self.is_playing = True
                self.play_btn.config(text="⏸")
                self.status_var.set("Playing")
            else:
                self.play_selected_track()
    
    def next_track(self):
        """Play next track"""
        if not self.current_playlist_name:
            return
        
        tracks = self.playlist_manager.get_playlist_tracks(self.current_playlist_name)
        if not tracks:
            return
        
        if self.shuffle_mode:
            import random
            self.current_track_index = random.randint(0, len(tracks) - 1)
        else:
            self.current_track_index += 1
            if self.current_track_index >= len(tracks):
                if self.loop_playlist:
                    self.current_track_index = 0
                else:
                    self.status_var.set("End of playlist")
                    return
        
        self.track_listbox.selection_clear(0, tk.END)
        self.track_listbox.selection_set(self.current_track_index)
        self.track_listbox.see(self.current_track_index)
        self.play_selected_track()
    
    def previous_track(self):
        """Play previous track"""
        if not self.current_playlist_name:
            return
        
        tracks = self.playlist_manager.get_playlist_tracks(self.current_playlist_name)
        if not tracks:
            return
        
        self.current_track_index -= 1
        if self.current_track_index < 0:
            if self.loop_playlist:
                self.current_track_index = len(tracks) - 1
            else:
                self.current_track_index = 0
                return
        
        self.track_listbox.selection_clear(0, tk.END)
        self.track_listbox.selection_set(self.current_track_index)
        self.track_listbox.see(self.current_track_index)
        self.play_selected_track()
    
    def rewind_track(self):
        """Rewind current track by 10 seconds"""
        if self.player.is_loaded():
            current_pos = self.player.get_position()
            new_pos = max(0, current_pos - 10)
            self.player.set_position(new_pos)
    
    def toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.shuffle_mode = not self.shuffle_mode
        self.shuffle_btn.config(relief="sunken" if self.shuffle_mode else "raised")
        self.status_var.set(f"Shuffle {'ON' if self.shuffle_mode else 'OFF'}")
    
    def toggle_playlist_loop(self):
        """Toggle playlist loop mode"""
        self.loop_playlist = not self.loop_playlist
        self.loop_playlist_btn.config(relief="sunken" if self.loop_playlist else "raised")
        self.status_var.set(f"Playlist Loop {'ON' if self.loop_playlist else 'OFF'}")
    
    def toggle_single_loop(self):
        """Toggle single track loop mode"""
        self.loop_single = not self.loop_single
        self.loop_single_btn.config(relief="sunken" if self.loop_single else "raised")
        self.status_var.set(f"Single Loop {'ON' if self.loop_single else 'OFF'}")
    
    def toggle_section(self, section):
        """Toggle collapse/expand of sections"""
        if section == 'playlists':
            self.collapsed_states['playlists'] = not self.collapsed_states['playlists']
            if self.collapsed_states['playlists']:
                self.playlist_frame.grid_remove()
                self.playlist_collapse_btn.config(text="+")
            else:
                self.playlist_frame.grid()
                self.playlist_collapse_btn.config(text="−")
        
        elif section == 'tracks':
            self.collapsed_states['tracks'] = not self.collapsed_states['tracks']
            if self.collapsed_states['tracks']:
                self.track_frame.grid_remove()
                self.track_collapse_btn.config(text="+")
            else:
                self.track_frame.grid()
                self.track_collapse_btn.config(text="−")
    
    def on_volume_change(self, value):
        """Handle volume change"""
        volume = float(value) / 100.0
        self.player.set_volume(volume)
    
    def on_speed_change(self, value):
        """Handle playback speed change"""
        speed = float(value)
        self.player.set_speed(speed)
    
    def on_progress_click(self, event):
        """Handle progress bar click"""
        if self.player.is_loaded():
            # Calculate position based on click
            widget_width = self.progress_scale.winfo_width()
            click_pos = event.x / widget_width
            duration = self.player.get_duration()
            new_position = duration * click_pos
            self.player.set_position(new_position)
    
    def on_track_end(self):
        """Handle track end event"""
        if self.loop_single:
            # Replay current track
            self.player.set_position(0)
            self.player.play()
        else:
            # Move to next track
            self.next_track()
    
    def on_position_update(self, position, duration):
        """Handle position update from player"""
        if duration > 0:
            progress = (position / duration) * 100
            self.progress_scale.set(progress)
        
        # Format time display
        pos_min, pos_sec = divmod(int(position), 60)
        dur_min, dur_sec = divmod(int(duration), 60)
        time_str = f"{pos_min:02d}:{pos_sec:02d} / {dur_min:02d}:{dur_sec:02d}"
        self.position_var.set(time_str)
    
    def on_player_error(self, error_msg):
        """Handle player error"""
        messagebox.showerror("Playback Error", error_msg)
        self.status_var.set("Playback error occurred")
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Color theme settings
        ttk.Label(settings_window, text="Color Theme:", font=('TkDefaultFont', 10, 'bold')).pack(pady=10)
        
        color_frame = ttk.Frame(settings_window)
        color_frame.pack(pady=5)
        
        ttk.Button(color_frame, text="Choose Primary Color",
                  command=lambda: self.choose_color('primary')).pack(side=tk.LEFT, padx=5)
        ttk.Button(color_frame, text="Choose Secondary Color",
                  command=lambda: self.choose_color('secondary')).pack(side=tk.LEFT, padx=5)
        
        # Reset to defaults
        ttk.Button(settings_window, text="Reset to Default Colors",
                  command=self.reset_colors).pack(pady=10)
        
        # Apply button
        ttk.Button(settings_window, text="Apply & Close",
                  command=lambda: [self.apply_color_theme(), settings_window.destroy()]).pack(pady=20)
    
    def choose_color(self, color_type):
        """Open color chooser dialog"""
        current_color = self.settings.get_setting(f'{color_type}_color')
        color = colorchooser.askcolor(color=current_color, title=f"Choose {color_type.title()} Color")
        
        if color[1]:  # If a color was selected
            self.settings.set_setting(f'{color_type}_color', color[1])
    
    def reset_colors(self):
        """Reset colors to default"""
        self.settings.reset_colors()
        self.apply_color_theme()
    
    def apply_color_theme(self):
        """Apply the current color theme"""
        primary = self.settings.get_setting('primary_color')
        secondary = self.settings.get_setting('secondary_color')
        
        # Apply colors to custom components
        for widget in [self.play_btn, self.prev_btn, self.next_btn, self.rewind_btn,
                      self.shuffle_btn, self.loop_playlist_btn, self.loop_single_btn,
                      self.playlist_collapse_btn, self.track_collapse_btn]:
            widget.set_colors(primary, secondary)
    
    def update_timer(self):
        """Update timer for position tracking"""
        if self.is_playing and self.player.is_loaded():
            position = self.player.get_position()
            duration = self.player.get_duration()
            self.on_position_update(position, duration)
        
        # Schedule next update
        self.root.after(1000, self.update_timer)
    
    def on_closing(self):
        """Handle application closing"""
        self.player.stop()
        self.settings.save_settings()
        self.root.destroy()

def main():
    """Main application entry point"""
    # Check dependencies
    try:
        import pygame
    except ImportError:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        messagebox.showerror(
            "Missing Dependency",
            "This application requires pygame for audio playback.\n\n"
            "Install it using:\npip install pygame\n\n"
            "Additional dependencies:\npip install mutagen"
        )
        return
    
    # Create playlists directory if it doesn't exist
    playlists_dir = Path("playlists")
    if not playlists_dir.exists():
        playlists_dir.mkdir()
        example_playlist = playlists_dir / "Example Playlist"
        example_playlist.mkdir()
        
        # Create example descriptor
        example_desc = {
            "display_name": "My Example Playlist",
            "description": "An example playlist folder",
            "tracks": {}
        }
        
        with open(example_playlist / "playlist.json", 'w') as f:
            import json
            json.dump(example_desc, f, indent=2)
    
    # Start the application
    root = tk.Tk()
    app = MusicPlayerApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()