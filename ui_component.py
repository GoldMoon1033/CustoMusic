#!/usr/bin/env python3
"""
Custom UI Components
Provides scrollable frames, custom buttons, and other specialized UI elements.
"""

import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    """A scrollable frame widget with both vertical and horizontal scrollbars"""
    
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create canvas and scrollbars
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        # Create the scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)
        
        # Grid layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        
        # Bind events
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Bind mouse events for scrolling
        self._bind_mouse_events(self.canvas)
        self._bind_mouse_events(self.scrollable_frame)
    
    def _bind_mouse_events(self, widget):
        """Bind mouse events to a widget for scrolling"""
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)  # Linux
        widget.bind("<Button-5>", self._on_mousewheel)  # Linux
        
        # Bind to all child widgets
        for child in widget.winfo_children():
            self._bind_mouse_events(child)
    
    def _on_frame_configure(self, event):
        """Update canvas scroll region when frame changes size"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Update scrollable frame width when canvas changes size"""
        canvas_width = event.width
        canvas_height = event.height
        
        # Update the window size to match canvas width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        # If the scrollable frame is smaller than canvas, center it
        frame_width = self.scrollable_frame.winfo_reqwidth()
        frame_height = self.scrollable_frame.winfo_reqheight()
        
        if frame_width < canvas_width:
            # Center horizontally
            x_offset = (canvas_width - frame_width) // 2
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        else:
            x_offset = 0
        
        if frame_height < canvas_height:
            # Center vertically
            y_offset = (canvas_height - frame_height) // 2
        else:
            y_offset = 0
        
        self.canvas.coords(self.canvas_window, x_offset, y_offset)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        # Determine scroll direction and amount
        if event.delta:
            delta = -1 * (event.delta / 120)
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        else:
            return
        
        # Check if we should scroll vertically or horizontally
        if event.state & 0x1:  # Shift key pressed
            self.canvas.xview_scroll(int(delta), "units")
        else:
            self.canvas.yview_scroll(int(delta), "units")
    
    def scroll_to_top(self):
        """Scroll to the top of the frame"""
        self.canvas.yview_moveto(0)
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the frame"""
        self.canvas.yview_moveto(1)
    
    def scroll_to_left(self):
        """Scroll to the left of the frame"""
        self.canvas.xview_moveto(0)
    
    def scroll_to_right(self):
        """Scroll to the right of the frame"""
        self.canvas.xview_moveto(1)


class CustomButton(tk.Button):
    """A custom button with enhanced styling and color support"""
    
    def __init__(self, parent, *args, **kwargs):
        # Extract custom options
        self.primary_color = kwargs.pop('primary_color', '#4a90e2')
        self.secondary_color = kwargs.pop('secondary_color', '#2c3e50')
        self.hover_color = kwargs.pop('hover_color', None)
        self.active_color = kwargs.pop('active_color', None)
        
        # Set default styling
        default_kwargs = {
            'relief': 'raised',
            'borderwidth': 1,
            'font': ('TkDefaultFont', 9),
            'cursor': 'hand2',
            'padx': 8,
            'pady': 4
        }
        
        # Merge with provided kwargs
        for key, value in default_kwargs.items():
            if key not in kwargs:
                kwargs[key] = value
        
        super().__init__(parent, *args, **kwargs)
        
        # Calculate derived colors
        if not self.hover_color:
            self.hover_color = self._lighten_color(self.primary_color, 0.1)
        if not self.active_color:
            self.active_color = self._darken_color(self.primary_color, 0.1)
        
        # Apply initial styling
        self.apply_styling()
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def apply_styling(self):
        """Apply the current color scheme to the button"""
        self.config(
            bg=self.primary_color,
            fg='white',
            activebackground=self.active_color,
            activeforeground='white'
        )
    
    def set_colors(self, primary_color, secondary_color):
        """Update button colors"""
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.hover_color = self._lighten_color(primary_color, 0.1)
        self.active_color = self._darken_color(primary_color, 0.1)
        self.apply_styling()
    
    def _on_enter(self, event):
        """Handle mouse enter event"""
        self.config(bg=self.hover_color)
    
    def _on_leave(self, event):
        """Handle mouse leave event"""
        self.config(bg=self.primary_color)
    
    def _on_press(self, event):
        """Handle button press event"""
        self.config(bg=self.active_color, relief='sunken')
    
    def _on_release(self, event):
        """Handle button release event"""
        self.config(bg=self.hover_color, relief='raised')
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def _lighten_color(self, hex_color, factor):
        """Lighten a hex color by a factor (0-1)"""
        try:
            rgb = self._hex_to_rgb(hex_color)
            new_rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
            return self._rgb_to_hex(new_rgb)
        except:
            return hex_color
    
    def _darken_color(self, hex_color, factor):
        """Darken a hex color by a factor (0-1)"""
        try:
            rgb = self._hex_to_rgb(hex_color)
            new_rgb = tuple(max(0, int(c * (1 - factor))) for c in rgb)
            return self._rgb_to_hex(new_rgb)
        except:
            return hex_color


class PlaybackControls(ttk.Frame):
    """A specialized frame for playback controls with enhanced layout"""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.configure(relief='raised', borderwidth=1, padding=10)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)


class ProgressBar(ttk.Frame):
    """A custom progress bar with click-to-seek functionality"""
    
    def __init__(self, parent, *args, **kwargs):
        # Extract custom options
        self.on_seek = kwargs.pop('on_seek', None)
        self.progress_color = kwargs.pop('progress_color', '#4a90e2')
        self.background_color = kwargs.pop('background_color', '#e0e0e0')
        
        super().__init__(parent, *args, **kwargs)
        
        # Progress variables
        self.position = 0.0
        self.duration = 1.0
        
        # Create canvas for custom drawing
        self.canvas = tk.Canvas(self, height=20, bg=self.background_color, 
                               highlightthickness=1, highlightbackground='#cccccc')
        self.canvas.pack(fill=tk.X, expand=True)
        
        # Bind events
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<Configure>", self._on_resize)
        
        # Draw initial state
        self.update_progress(0, 1)
    
    def update_progress(self, position, duration):
        """Update the progress bar"""
        self.position = position
        self.duration = max(duration, 1)  # Prevent division by zero
        self._redraw()
    
    def _redraw(self):
        """Redraw the progress bar"""
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1:
            return  # Canvas not ready
        
        # Calculate progress percentage
        progress_percent = min(1.0, max(0.0, self.position / self.duration))
        progress_width = int(width * progress_percent)
        
        # Draw background
        self.canvas.create_rectangle(0, 0, width, height, 
                                   fill=self.background_color, outline='')
        
        # Draw progress
        if progress_width > 0:
            self.canvas.create_rectangle(0, 0, progress_width, height, 
                                       fill=self.progress_color, outline='')
        
        # Draw position indicator
        if progress_width > 2:
            indicator_x = progress_width - 1
            self.canvas.create_line(indicator_x, 0, indicator_x, height, 
                                  fill='white', width=2)
    
    def _on_click(self, event):
        """Handle click for seeking"""
        self._seek_to_position(event.x)
    
    def _on_drag(self, event):
        """Handle drag for seeking"""
        self._seek_to_position(event.x)
    
    def _seek_to_position(self, x):
        """Seek to position based on x coordinate"""
        width = self.canvas.winfo_width()
        if width > 0 and self.on_seek:
            progress_percent = max(0.0, min(1.0, x / width))
            new_position = progress_percent * self.duration
            self.on_seek(new_position)
    
    def _on_resize(self, event):
        """Handle canvas resize"""
        self._redraw()
    
    def set_colors(self, progress_color, background_color):
        """Update colors"""
        self.progress_color = progress_color
        self.background_color = background_color
        self.canvas.config(bg=background_color)
        self._redraw()


class VolumeControl(ttk.Frame):
    """A specialized volume control with visual feedback"""
    
    def __init__(self, parent, *args, **kwargs):
        # Extract custom options
        self.on_volume_change = kwargs.pop('on_volume_change', None)
        self.initial_volume = kwargs.pop('initial_volume', 70)
        
        super().__init__(parent, *args, **kwargs)
        
        # Volume variable
        self.volume_var = tk.DoubleVar(value=self.initial_volume)
        
        # Create controls
        self.create_controls()
        
        # Bind volume change
        self.volume_var.trace('w', self._on_volume_change)
    
    def create_controls(self):
        """Create volume control elements"""
        # Volume icon
        self.volume_icon = tk.Label(self, text="🔊", font=('TkDefaultFont', 12))
        self.volume_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        # Volume scale
        self.volume_scale = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL,
                                     variable=self.volume_var, length=100)
        self.volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Volume label
        self.volume_label = tk.Label(self, text="70%", width=4, font=('TkDefaultFont', 9))
        self.volume_label.pack(side=tk.RIGHT)
    
    def _on_volume_change(self, *args):
        """Handle volume change"""
        volume = int(self.volume_var.get())
        
        # Update label
        self.volume_label.config(text=f"{volume}%")
        
        # Update icon
        if volume == 0:
            self.volume_icon.config(text="🔇")
        elif volume < 30:
            self.volume_icon.config(text="🔈")
        elif volume < 70:
            self.volume_icon.config(text="🔉")
        else:
            self.volume_icon.config(text="🔊")
        
        # Notify callback
        if self.on_volume_change:
            self.on_volume_change(volume)
    
    def set_volume(self, volume):
        """Set volume programmatically"""
        self.volume_var.set(max(0, min(100, volume)))
    
    def get_volume(self):
        """Get current volume"""
        return int(self.volume_var.get())


class ToolTip:
    """A simple tooltip implementation"""
    
    def __init__(self, widget, text=''):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        # Bind events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.on_motion)
    
    def show_tooltip(self, event=None):
        """Show the tooltip"""
        if not self.text:
            return
        
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip_window, text=self.text, 
                        background="#ffffe0", relief="solid", borderwidth=1,
                        font=("TkDefaultFont", 8), justify="left")
        label.pack()
    
    def hide_tooltip(self, event=None):
        """Hide the tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def on_motion(self, event=None):
        """Handle mouse motion - update tooltip position"""
        if self.tooltip_window:
            x = self.widget.winfo_rootx() + event.x + 25
            y = self.widget.winfo_rooty() + event.y + 25
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
    
    def set_text(self, text):
        """Update tooltip text"""
        self.text = text


def add_tooltip(widget, text):
    """Convenience function to add tooltip to a widget"""
    return ToolTip(widget, text)