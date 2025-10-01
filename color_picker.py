import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import webcolors
import threading
import time
from PIL import Image, ImageTk
from PIL.Image import Resampling
import numpy as np

class ColorPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")
        self.root.geometry("300x240")
        self.root.resizable(False, False)
        
        # Variables
        self.picking = False
        self.current_color = None
        self.magnifier = None
        self.dual_mode = False
        self.dual_pick_stage = 1  # 1 for first pick, 2 for second pick
        self.current_color_2 = None
        
        # Create GUI
        self.create_widgets()
        
        # Bind escape key to cancel picking
        self.root.bind('<Escape>', self.cancel_picking)
        self.root.focus_set()
        
    def create_widgets(self):
        # Main container that will expand for dual mode
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        # Left panel (always visible)
        self.left_panel = tk.Frame(self.main_container)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Right panel (only visible in dual mode)
        self.right_panel = tk.Frame(self.main_container)
        # Initially not packed - will be shown in dual mode
        
        # Create widgets for left panel
        self.create_panel_widgets(self.left_panel, is_primary=True)
        
        # Create widgets for right panel (but don't show yet)
        self.create_panel_widgets(self.right_panel, is_primary=False)
        
        # Bottom buttons frame - use grid layout for proper alignment
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x", pady=3)
        
        # Configure grid columns to match the panel layout
        bottom_frame.grid_columnconfigure(0, weight=0)  # Mode button column
        bottom_frame.grid_columnconfigure(1, weight=1)  # Left panel column  
        bottom_frame.grid_columnconfigure(2, weight=1)  # Right panel column
        
        # Dual mode toggle button (leftmost, always stays in position)
        self.dual_mode_btn = tk.Button(bottom_frame, text="2", 
                                     command=self.toggle_dual_mode,
                                     width=2, height=1, font=("Arial", 8),
                                     bg="#666666", fg="white")
        self.dual_mode_btn.grid(row=0, column=0, sticky="w", padx=(5, 15))
        
        # Left copy buttons frame (aligned under Color 1 panel)
        left_copy_frame = tk.Frame(bottom_frame)
        left_copy_frame.grid(row=0, column=1, sticky="")
        
        self.copy_rgb_btn = tk.Button(left_copy_frame, text="RGB", 
                                    command=self.copy_rgb,
                                    state="disabled", width=6, font=("Arial", 8))
        self.copy_rgb_btn.pack(side="left", padx=2)
        
        self.copy_hex_btn = tk.Button(left_copy_frame, text="HEX", 
                                    command=self.copy_hex,
                                    state="disabled", width=6, font=("Arial", 8))
        self.copy_hex_btn.pack(side="left", padx=2)
        
        # Right copy buttons frame (aligned under Color 2 panel, initially hidden)
        self.right_copy_frame = tk.Frame(bottom_frame)
        # Will be shown in dual mode at grid position (0, 2)
        
        self.copy_rgb_btn_2 = tk.Button(self.right_copy_frame, text="RGB", 
                                      command=self.copy_rgb_2,
                                      state="disabled", width=6, font=("Arial", 8))
        self.copy_rgb_btn_2.pack(side="left", padx=2)
        
        self.copy_hex_btn_2 = tk.Button(self.right_copy_frame, text="HEX", 
                                      command=self.copy_hex_2,
                                      state="disabled", width=6, font=("Arial", 8))
        self.copy_hex_btn_2.pack(side="left", padx=2)
    
    def create_panel_widgets(self, parent, is_primary=True):
        """Create the color picker widgets for a panel"""
        # Top row: Pick button and Color preview side by side
        top_frame = tk.Frame(parent)
        top_frame.pack(pady=8, padx=5, fill="x")
        
        if is_primary:
            # Pick Color Button (only in primary panel) - reduced height
            self.pick_button = tk.Button(top_frame, text="Pick", 
                                       command=self.start_picking,
                                       bg="#4CAF50", fg="white",
                                       font=("Arial", 10, "bold"),
                                       width=8, height=1)
            self.pick_button.pack(side="left", padx=(0, 8))
            
            # Color Preview (primary)
            self.color_preview = tk.Label(top_frame, width=15, height=2, 
                                        relief="sunken", bd=2, bg="white")
            self.color_preview.pack(side="right", fill="x", expand=True)
        else:
            # Label for second color panel - same height as pick button
            panel_label = tk.Label(top_frame, text="Color 2", 
                                 font=("Arial", 10, "bold"),
                                 width=8, height=1, relief="raised", bd=1)
            panel_label.pack(side="left", padx=(0, 8))
            
            # Color Preview (secondary)
            self.color_preview_2 = tk.Label(top_frame, width=15, height=2, 
                                          relief="sunken", bd=2, bg="white")
            self.color_preview_2.pack(side="right", fill="x", expand=True)
        
        # Status Label - add to both panels
        if is_primary:
            self.status_label = tk.Label(parent, text="Ready",
                                       font=("Arial", 8), height=1)
            self.status_label.pack(pady=2)
        else:
            # Status label for second panel
            self.status_label_2 = tk.Label(parent, text="Waiting...",
                                         font=("Arial", 8), height=1, fg="gray")
            self.status_label_2.pack(pady=2)
        
        # Color Information Frame
        info_frame = tk.Frame(parent)
        info_frame.pack(pady=5, padx=5, fill="x")
        
        if is_primary:
            # RGB Values (primary)
            self.rgb_label = tk.Label(info_frame, text="RGB: -, -, -", 
                                    font=("Arial", 8), bg="#f0f0f0", relief="sunken", bd=1)
            self.rgb_label.pack(fill="x", pady=1)
            
            # Hex Value (primary)
            self.hex_label = tk.Label(info_frame, text="#------", 
                                    font=("Arial", 8), bg="#f0f0f0", relief="sunken", bd=1)
            self.hex_label.pack(fill="x", pady=1)
            
            # Color names (primary)
            self.color_name_frame = tk.Frame(info_frame)
            self.color_name_frame.pack(fill="x", pady=2)
            
            self.color_name_labels = []
            for i in range(3):
                label = tk.Label(self.color_name_frame, text="None", 
                               font=("Arial", 8, "bold"),
                               fg="blue" if i == 0 else "darkblue", 
                               bg="#f0f0f0", relief="sunken", bd=1, wraplength=280)
                label.pack(fill="x", pady=1)
                self.color_name_labels.append(label)
        else:
            # RGB Values (secondary)
            self.rgb_label_2 = tk.Label(info_frame, text="RGB: -, -, -", 
                                      font=("Arial", 8), bg="#f0f0f0", relief="sunken", bd=1)
            self.rgb_label_2.pack(fill="x", pady=1)
            
            # Hex Value (secondary)
            self.hex_label_2 = tk.Label(info_frame, text="#------", 
                                      font=("Arial", 8), bg="#f0f0f0", relief="sunken", bd=1)
            self.hex_label_2.pack(fill="x", pady=1)
            
            # Color names (secondary)
            self.color_name_frame_2 = tk.Frame(info_frame)
            self.color_name_frame_2.pack(fill="x", pady=2)
            
            self.color_name_labels_2 = []
            for i in range(3):
                label = tk.Label(self.color_name_frame_2, text="None", 
                               font=("Arial", 8, "bold"),
                               fg="blue" if i == 0 else "darkblue", 
                               bg="#f0f0f0", relief="sunken", bd=1, wraplength=280)
                label.pack(fill="x", pady=1)
                self.color_name_labels_2.append(label)
        
    def get_simple_color_name(self, rgb):
        """Convert RGB to simple color name using scientific CSS3 color matching"""
        r, g, b = rgb
        
        try:
            # Find the closest CSS3 colors and return top 3
            return self.get_top_color_matches(rgb)
        except Exception:
            # Fallback to basic detection
            return ["unknown"]
    
    def get_top_color_matches(self, rgb, top_n=3):
        """Get top N closest color matches using CSS3 colors"""
        target_r, target_g, target_b = rgb
        distances = []
        
        # Get all CSS3 color names
        css3_names = webcolors.names('css3')
        
        for name in css3_names:
            try:
                css_rgb = webcolors.name_to_rgb(name, spec='css3')
                css_r, css_g, css_b = css_rgb
                
                # Calculate Euclidean distance
                distance = ((target_r - css_r) ** 2 + 
                           (target_g - css_g) ** 2 + 
                           (target_b - css_b) ** 2) ** 0.5
                
                # Map to simple color name
                simple_name = self.map_css_to_simple(name)
                distances.append((distance, simple_name, name, css_rgb))
                
            except ValueError:
                continue
        
        # Sort by distance and return top matches
        distances.sort()
        return [(simple_name, css_name, distance) for distance, simple_name, css_name, css_rgb in distances[:top_n]]
    
    def map_css_to_simple(self, css_name):
        """Map CSS3 color names to simple color names"""
        css_name = css_name.lower()
        
        # Comprehensive mapping from CSS colors to simple names
        color_mapping = {
            # Reds
            'red': 'red', 'darkred': 'red', 'crimson': 'red', 'firebrick': 'red',
            'indianred': 'red', 'lightcoral': 'red', 'salmon': 'red', 'darksalmon': 'red',
            'lightsalmon': 'red', 'tomato': 'red', 'orangered': 'red',
            
            # Oranges
            'orange': 'orange', 'darkorange': 'orange', 'coral': 'orange', 
            'chocolate': 'orange', 'sandybrown': 'orange', 'peru': 'orange',
            'sienna': 'orange', 'saddlebrown': 'orange',
            
            # Yellows
            'yellow': 'yellow', 'gold': 'yellow', 'khaki': 'yellow', 'darkkhaki': 'yellow',
            'palegoldenrod': 'yellow', 'goldenrod': 'yellow', 'darkgoldenrod': 'yellow',
            'lightyellow': 'yellow', 'lemonchiffon': 'yellow', 'lightgoldenrodyellow': 'yellow',
            'papayawhip': 'yellow', 'moccasin': 'yellow', 'peachpuff': 'yellow',
            'wheat': 'yellow', 'navajowhite': 'yellow',
            
            # Yellow-Greens (the key ones!)
            'burlywood': 'yellow-green', 'tan': 'yellow-green', 'greenyellow': 'yellow-green', 
            'yellowgreen': 'yellow-green', 'olivedrab': 'yellow-green',
            'darkolivegreen': 'yellow-green', 'olive': 'yellow-green',
            
            # Greens
            'green': 'green', 'darkgreen': 'green', 'forestgreen': 'green', 'limegreen': 'green',
            'lime': 'green', 'seagreen': 'green', 'mediumseagreen': 'green', 'springgreen': 'green',
            'mediumspringgreen': 'green', 'darkseagreen': 'green', 'lightgreen': 'green',
            'palegreen': 'green', 'lawngreen': 'green', 'chartreuse': 'green',
            
            # Blues
            'blue': 'blue', 'darkblue': 'blue', 'mediumblue': 'blue', 'navy': 'blue',
            'midnightblue': 'blue', 'royalblue': 'blue', 'steelblue': 'blue',
            'dodgerblue': 'blue', 'deepskyblue': 'blue', 'cornflowerblue': 'blue',
            'skyblue': 'blue', 'lightskyblue': 'blue', 'lightsteelblue': 'blue',
            'lightblue': 'blue', 'powderblue': 'blue', 'cadetblue': 'blue',
            'aqua': 'blue', 'cyan': 'blue', 'lightcyan': 'blue', 'paleturquoise': 'blue',
            'aquamarine': 'blue-green', 'turquoise': 'blue-green', 'mediumturquoise': 'blue-green',
            'darkturquoise': 'blue-green', 'lightseagreen': 'blue-green', 'teal': 'blue-green',
            'darkcyan': 'blue-green',
            
            # Purples and Magentas
            'purple': 'purple', 'indigo': 'purple', 'darkviolet': 'purple', 'darkorchid': 'purple',
            'darkmagenta': 'magenta', 'violet': 'purple', 'plum': 'purple', 'thistle': 'purple',
            'orchid': 'purple', 'mediumorchid': 'purple', 'mediumpurple': 'purple',
            'blueviolet': 'purple', 'slateblue': 'purple', 'darkslateblue': 'purple',
            'mediumslateblue': 'purple', 'magenta': 'magenta', 'fuchsia': 'magenta',
            'deeppink': 'magenta', 'hotpink': 'pink', 'lightpink': 'pink', 'pink': 'pink',
            'mistyrose': 'pink', 'lavenderblush': 'pink',
            
            # Browns
            'brown': 'brown', 'maroon': 'brown', 'rosybrown': 'brown',
            
            # Grays and Whites
            'white': 'white', 'snow': 'white', 'honeydew': 'white', 'mintcream': 'white',
            'azure': 'white', 'aliceblue': 'white', 'ghostwhite': 'white', 'whitesmoke': 'white',
            'seashell': 'white', 'beige': 'white', 'oldlace': 'white', 'floralwhite': 'white',
            'ivory': 'white', 'antiquewhite': 'white', 'linen': 'white', 'lavender': 'white',
            'black': 'black', 'dimgray': 'gray', 'dimgrey': 'gray', 'gray': 'gray', 'grey': 'gray',
            'darkgray': 'gray', 'darkgrey': 'gray', 'silver': 'gray', 'lightgray': 'gray',
            'lightgrey': 'gray', 'gainsboro': 'gray', 'slategray': 'gray', 'slategrey': 'gray',
            'lightslategray': 'gray', 'lightslategrey': 'gray', 'darkslategray': 'gray',
            'darkslategrey': 'gray',
        }
        
        return color_mapping.get(css_name, css_name)
    
    def calculate_color_similarity(self, color1, color2):
        """Calculate similarity between two RGB colors and return detailed assessment"""
        if not color1 or not color2:
            return "No comparison available", "gray"
        
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        # Calculate Euclidean distance in RGB space
        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        
        # Get basic color categories for both colors
        color1_matches = self.get_simple_color_name(color1)
        color2_matches = self.get_simple_color_name(color2)
        
        basic_color1 = color1_matches[0][0] if color1_matches else "unknown"
        basic_color2 = color2_matches[0][0] if color2_matches else "unknown"
        
        # Provide meaningful similarity assessment
        if distance == 0:
            assessment = "Identical colors"
            color = "purple"
        elif distance < 10:
            assessment = "Nearly identical"
            color = "darkgreen"
        elif distance < 25:
            assessment = "Very similar"
            color = "green"
        elif distance < 50:
            assessment = "Similar"
            color = "olive"
        elif distance < 100:
            assessment = "Somewhat different"
            color = "orange"
        elif distance < 150:
            assessment = "Different"
            color = "darkorange"
        else:
            assessment = "Very different"
            color = "red"
        
        # Add component analysis if colors are in the same basic category
        component_analysis = ""
        if basic_color1 == basic_color2 and distance > 5:  # Only if same category and noticeably different
            component_analysis = self.analyze_color_components(color1, color2)
            if component_analysis:
                assessment += f" ({component_analysis})"
        
        return f"{assessment} (Δ{distance:.1f})", color
    
    def analyze_color_components(self, color1, color2):
        """Analyze which color has more of each component (red, green, blue)"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        # Calculate differences in each component
        red_diff = r2 - r1
        green_diff = g2 - g1
        blue_diff = b2 - b1
        
        # Find the most significant difference (threshold of 10 to avoid noise)
        threshold = 10
        components = []
        
        if abs(red_diff) > threshold:
            if red_diff > 0:
                components.append("more red")
            else:
                components.append("less red")
        
        if abs(green_diff) > threshold:
            if green_diff > 0:
                components.append("more green")
            else:
                components.append("less green")
        
        if abs(blue_diff) > threshold:
            if blue_diff > 0:
                components.append("more blue")
            else:
                components.append("less blue")
        
        # Return the most significant differences (max 2 to keep it readable)
        if components:
            return "Color 2: " + ", ".join(components[:2])
        return ""
    
    def toggle_dual_mode(self):
        """Toggle between single and dual color picker mode"""
        if not self.dual_mode:
            # Switch to dual mode
            self.dual_mode = True
            self.dual_pick_stage = 1
            self.dual_mode_btn.config(text="1")
            
            # Show right panel
            self.right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
            
            # Show right copy buttons aligned with the second panel
            self.right_copy_frame.grid(row=0, column=2, sticky="")
            
            # Resize window to accommodate both panels
            self.root.geometry("600x240")
            
            # Update pick button text
            self.pick_button.config(text="Pick 1")
            
            # Update status
            self.status_label.config(text="Dual mode: Pick first color (SPACE)", fg="blue")
            if hasattr(self, 'status_label_2'):
                # If both colors are already available, show similarity
                if hasattr(self, 'current_color') and hasattr(self, 'current_color_2') and self.current_color and self.current_color_2:
                    similarity_text, similarity_color = self.calculate_color_similarity(self.current_color, self.current_color_2)
                    self.status_label_2.config(text=similarity_text, fg=similarity_color)
                else:
                    self.status_label_2.config(text="Waiting...", fg="gray")
            
        else:
            # Switch to single mode
            self.dual_mode = False
            self.dual_pick_stage = 1
            self.dual_mode_btn.config(text="2")
            
            # Hide right panel
            self.right_panel.pack_forget()
            
            # Hide right copy buttons
            self.right_copy_frame.grid_remove()
            
            # Resize window back to single mode
            self.root.geometry("300x240")
            
            # Reset pick button text
            self.pick_button.config(text="Pick")
            
            # Reset status
            self.status_label.config(text="Single mode", fg="green")
            
            # Clear second color data
            self.current_color_2 = None
            self.clear_color_display_2()
    
    def update_color_display_2(self, rgb_color):
        """Update the second color display in dual mode"""
        self.picking = False
        self.current_color_2 = rgb_color
        r, g, b = rgb_color
        
        # Destroy magnifier
        self.destroy_magnifier()
        
        # Unbind the spacebar
        self.root.unbind('<space>')
        self.root.unbind('<KeyPress-space>')
        
        # Update color preview 2
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_preview_2.config(bg=hex_color)
        
        # Update RGB values 2
        self.rgb_label_2.config(text=f"RGB: {r}, {g}, {b}")
        
        # Update hex value 2
        self.hex_label_2.config(text=hex_color.upper())
        
        # Get color matches (top 3)
        color_matches = self.get_simple_color_name(rgb_color)
        
        # Update the 3 color name labels for second color
        for i, label in enumerate(self.color_name_labels_2):
            if i < len(color_matches):
                simple_name, css_name, distance = color_matches[i]
                if i == 0:
                    display_text = f"{css_name.title()} ({simple_name})"
                    label.config(text=display_text)
                else:
                    display_text = f"{css_name.title()} ({simple_name}, {distance:.0f})"
                    label.config(text=display_text)
            else:
                label.config(text="")
        
        # Reset cursor
        self.root.config(cursor="")
        
        # Enable copy buttons for second color
        self.copy_rgb_btn_2.config(state="normal")
        self.copy_hex_btn_2.config(state="normal")
    
    def clear_color_display_2(self):
        """Clear the second color display"""
        if hasattr(self, 'color_preview_2'):
            self.color_preview_2.config(bg="white")
            self.rgb_label_2.config(text="RGB: -, -, -")
            self.hex_label_2.config(text="#------")
            for label in self.color_name_labels_2:
                label.config(text="None")
        if hasattr(self, 'status_label_2'):
            self.status_label_2.config(text="Waiting...", fg="gray")

    
    def create_magnifier(self):
        """Create a magnifier window that follows the mouse"""
        self.magnifier = tk.Toplevel(self.root)
        self.magnifier.title("Magnifier")
        self.magnifier.geometry("120x120")
        self.magnifier.resizable(False, False)
        self.magnifier.attributes('-topmost', True)
        self.magnifier.overrideredirect(True)  # Remove window decorations
        
        # Create canvas for magnified view
        self.mag_canvas = tk.Canvas(self.magnifier, width=120, height=120, bg="black", highlightthickness=2, highlightbackground="red")
        self.mag_canvas.pack()
        
        # Add crosshair lines
        self.mag_canvas.create_line(60, 0, 60, 120, fill="red", width=1, tags="crosshair")
        self.mag_canvas.create_line(0, 60, 120, 60, fill="red", width=1, tags="crosshair")
        
        # Add center pixel highlight
        self.mag_canvas.create_rectangle(55, 55, 65, 65, outline="yellow", width=2, tags="center")
        
        # Position magnifier initially
        self.update_magnifier_position()
    
    def update_magnifier_position(self):
        """Update magnifier position and content"""
        if not self.picking or not self.magnifier:
            return
            
        try:
            # Get mouse position
            x, y = pyautogui.position()
            
            # Position magnifier window offset from mouse
            mag_x = x + 30
            mag_y = y - 150
            
            # Simple positioning - avoid complex screen calculations
            if mag_x + 120 > x + 400:  # If would go too far right
                mag_x = x - 150
            if mag_y < 50:  # If would go too high
                mag_y = y + 30
                
            # Try multiple positioning methods for multi-monitor compatibility
            try:
                self.magnifier.wm_geometry(f"120x120+{mag_x}+{mag_y}")
            except:
                try:
                    self.magnifier.geometry(f"120x120+{mag_x}+{mag_y}")
                except:
                    pass
            
            # Multi-monitor screenshot approach
            capture_size = 15
            half_size = capture_size // 2
            
            try:
                # Method 1: Try Windows-specific screen capture
                import win32gui
                import win32ui
                import win32con
                
                # Get device context for the entire virtual screen
                hdesktop = win32gui.GetDesktopWindow()
                desktop_dc = win32gui.GetWindowDC(hdesktop)
                img_dc = win32ui.CreateDCFromHandle(desktop_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot_bmp = win32ui.CreateBitmap()
                screenshot_bmp.CreateCompatibleBitmap(img_dc, capture_size, capture_size)
                mem_dc.SelectObject(screenshot_bmp)
                
                # Copy screen area to bitmap
                mem_dc.BitBlt((0, 0), (capture_size, capture_size), img_dc, (x - half_size, y - half_size), win32con.SRCCOPY)
                
                # Convert to PIL Image
                bmpinfo = screenshot_bmp.GetInfo()
                bmpstr = screenshot_bmp.GetBitmapBits(True)
                screenshot = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
                
                # Clean up
                mem_dc.DeleteDC()
                img_dc.DeleteDC()
                win32gui.ReleaseDC(hdesktop, desktop_dc)
                win32gui.DeleteObject(screenshot_bmp.GetHandle())
                
            except (ImportError, Exception):
                try:
                    # Method 2: PIL ImageGrab with all monitors
                    import PIL.ImageGrab as ImageGrab
                    bbox = (x - half_size, y - half_size, x + half_size, y + half_size)
                    screenshot = ImageGrab.grab(bbox=bbox, all_screens=True)
                    
                except Exception:
                    try:
                        # Method 3: MSS (Multi-Screen Screenshot) if available
                        import mss
                        with mss.mss() as sct:
                            monitor = {
                                "top": y - half_size,
                                "left": x - half_size,
                                "width": capture_size,
                                "height": capture_size
                            }
                            screenshot_mss = sct.grab(monitor)
                            screenshot = Image.frombytes("RGB", screenshot_mss.size, screenshot_mss.bgra, "raw", "BGRX")
                            
                    except (ImportError, Exception):
                        # Method 4: Fallback to pyautogui with full desktop
                        full_screenshot = pyautogui.screenshot()
                        img_width, img_height = full_screenshot.size
                        
                        start_x = max(0, min(x - half_size, img_width - capture_size))
                        start_y = max(0, min(y - half_size, img_height - capture_size))
                        end_x = min(img_width, start_x + capture_size)
                        end_y = min(img_height, start_y + capture_size)
                        
                        screenshot = full_screenshot.crop((start_x, start_y, end_x, end_y))
            
            # Resize and display
            screenshot = screenshot.resize((120, 120), Resampling.NEAREST)
            self.mag_photo = ImageTk.PhotoImage(screenshot)
            
            # Update canvas
            self.mag_canvas.delete("image")
            self.mag_canvas.create_image(60, 60, image=self.mag_photo, tags="image")
            
            # Bring crosshair and center to front
            self.mag_canvas.tag_raise("crosshair")
            self.mag_canvas.tag_raise("center")
            
        except Exception as e:
            pass  # Ignore errors during magnifier update
    
    def destroy_magnifier(self):
        """Destroy the magnifier window"""
        if self.magnifier:
            self.magnifier.destroy()
            self.magnifier = None
    
    def start_picking(self):
        """Start the color picking process"""
        self.picking = True
        
        # Clear second panel in dual mode when starting a new picking cycle
        if self.dual_mode:
            self.clear_color_display_2()
        
        if self.dual_mode:
            # In dual mode, always start with stage 1 and expect two consecutive picks
            self.dual_pick_stage = 1
            self.pick_button.config(state="disabled", text="SPACE x2")
            self.status_label.config(text="Pick first color (SPACE)", fg="red")
            if hasattr(self, 'status_label_2'):
                self.status_label_2.config(text="Waiting for second pick...", fg="gray")
        else:
            self.pick_button.config(state="disabled", text="SPACE")
            self.status_label.config(text="Move mouse, press SPACE", fg="red")
        
        # Create magnifier window
        self.create_magnifier()
        
        # Start monitoring for spacebar press
        self.root.focus_set()
        self.root.bind('<space>', self.pick_color_at_mouse)
        self.root.bind('<KeyPress-space>', self.pick_color_at_mouse)
        
        # Start a thread to show current mouse position color preview
        thread = threading.Thread(target=self.show_live_preview, daemon=True)
        thread.start()
        
    def show_live_preview(self):
        """Show live preview of color under mouse"""
        while self.picking:
            try:
                x, y = pyautogui.position()
                pixel_color = pyautogui.pixel(x, y)
                
                # Update status with current position
                self.root.after(0, self.update_preview_status, x, y, pixel_color)
                
                # Update magnifier
                self.root.after(0, self.update_magnifier_position)
                
                time.sleep(0.05)  # Update 20 times per second for smooth magnifier
                
            except Exception as e:
                break
                
    def update_preview_status(self, x, y, rgb_color):
        """Update status with preview information"""
        if self.picking:
            r, g, b = rgb_color
            color_matches = self.get_simple_color_name(rgb_color)
            if color_matches and len(color_matches) > 0:
                css_name = color_matches[0][1]  # Get the CSS name from first match
                simple_name = color_matches[0][0]  # Get the simple name
                preview_text = f"{css_name.title()} ({simple_name}) - ({r},{g},{b})"
                
                if self.dual_mode:
                    if self.dual_pick_stage == 1:
                        self.status_label.config(text=preview_text, fg="blue")
                    else:
                        self.status_label_2.config(text=preview_text, fg="blue")
                else:
                    self.status_label.config(text=preview_text, fg="blue")
        
    def pick_color_at_mouse(self, event=None):
        """Pick color at current mouse position when spacebar is pressed"""
        if self.picking:
            try:
                x, y = pyautogui.position()
                pixel_color = pyautogui.pixel(x, y)
                
                if self.dual_mode:
                    if self.dual_pick_stage == 1:
                        # First pick - update first color and prepare for second
                        self.update_color_display(pixel_color)
                        self.dual_pick_stage = 2
                        self.status_label.config(text="First color picked!", fg="green")
                        self.status_label_2.config(text="Pick second color (SPACE)", fg="red")
                        # Keep picking active and recreate magnifier for second color
                        self.picking = True
                        # Recreate magnifier for second pick since update_color_display destroyed it
                        if not self.magnifier:
                            self.create_magnifier()
                    elif self.dual_pick_stage == 2:
                        # Second pick - update second color and finish
                        self.update_color_display_2(pixel_color)
                        self.dual_pick_stage = 1
                        self.picking = False
                        self.destroy_magnifier()
                        self.root.unbind('<space>')
                        self.root.unbind('<KeyPress-space>')
                        self.pick_button.config(state="normal", text="Pick")
                        # Calculate and display color similarity
                        similarity_text, similarity_color = self.calculate_color_similarity(self.current_color, self.current_color_2)
                        self.status_label.config(text="Both colors picked!", fg="green")
                        self.status_label_2.config(text=similarity_text, fg=similarity_color)
                else:
                    self.update_color_display(pixel_color)
                    
            except Exception as e:
                self.show_error(f"Error picking color: {str(e)}")
                
    def setup_click_capture(self):
        """Setup click capture after a brief delay"""
        # This method is no longer needed with the spacebar approach
        pass
        
    def monitor_mouse_click(self):
        """Monitor for mouse click to pick color using a simpler approach"""
        # This method is no longer needed with the spacebar approach
        pass
            
    def restore_window(self):
        """Restore the window after picking"""
        # This method is no longer needed with the spacebar approach
        pass
    
    def update_color_display(self, rgb_color):
        """Update the GUI with the picked color"""
        # Only stop picking if we're not in dual mode or if this is not the first pick
        if not self.dual_mode or self.dual_pick_stage != 1:
            self.picking = False
            # Destroy magnifier
            self.destroy_magnifier()
            # Unbind the spacebar
            self.root.unbind('<space>')
            self.root.unbind('<KeyPress-space>')
        
        self.current_color = rgb_color
        r, g, b = rgb_color
        
        # Update color preview
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_preview.config(bg=hex_color)
        
        # Update RGB values
        self.rgb_label.config(text=f"RGB: {r}, {g}, {b}")
        
        # Update hex value
        self.hex_label.config(text=hex_color.upper())
        
        # Get color matches (top 3)
        color_matches = self.get_simple_color_name(rgb_color)
        
        # Update the 3 color name labels
        for i, label in enumerate(self.color_name_labels):
            if i < len(color_matches):
                simple_name, css_name, distance = color_matches[i]
                if i == 0:
                    # Primary match - show CSS name with simple name in brackets
                    display_text = f"{css_name.title()} ({simple_name})"
                    label.config(text=display_text)
                else:
                    # Secondary matches - show CSS name with simple name and distance
                    display_text = f"{css_name.title()} ({simple_name}, {distance:.0f})"
                    label.config(text=display_text)
            else:
                label.config(text="")
        
        # Reset button and cursor
        self.pick_button.config(state="normal", text="Pick")
        self.root.config(cursor="")
        self.status_label.config(text="Picked!", fg="green")
        
        # Enable copy buttons
        self.copy_rgb_btn.config(state="normal")
        self.copy_hex_btn.config(state="normal")
    
    def cancel_picking(self, event=None):
        """Cancel the color picking process"""
        if self.picking:
            self.picking = False
            
            # Destroy magnifier
            self.destroy_magnifier()
            
            # Unbind the spacebar
            self.root.unbind('<space>')
            self.root.unbind('<KeyPress-space>')
            
            self.pick_button.config(state="normal", text="Pick")
            self.root.config(cursor="")
            self.status_label.config(text="Cancelled", fg="orange")
    
    def copy_rgb(self):
        """Copy RGB values to clipboard"""
        if self.current_color:
            r, g, b = self.current_color
            rgb_text = f"rgb({r}, {g}, {b})"
            self.root.clipboard_clear()
            self.root.clipboard_append(rgb_text)
            self.status_label.config(text="RGB copied!", fg="blue")
    
    def copy_hex(self):
        """Copy hex value to clipboard"""
        if self.current_color:
            r, g, b = self.current_color
            hex_text = f"#{r:02x}{g:02x}{b:02x}".upper()
            self.root.clipboard_clear()
            self.root.clipboard_append(hex_text)
            self.status_label.config(text="HEX copied!", fg="blue")
    
    def copy_rgb_2(self):
        """Copy RGB values from second color to clipboard"""
        if self.current_color_2:
            r, g, b = self.current_color_2
            rgb_text = f"rgb({r}, {g}, {b})"
            self.root.clipboard_clear()
            self.root.clipboard_append(rgb_text)
            if hasattr(self, 'status_label_2'):
                self.status_label_2.config(text="RGB copied!", fg="blue")
    
    def copy_hex_2(self):
        """Copy hex value from second color to clipboard"""
        if self.current_color_2:
            r, g, b = self.current_color_2
            hex_text = f"#{r:02x}{g:02x}{b:02x}".upper()
            self.root.clipboard_clear()
            self.root.clipboard_append(hex_text)
            if hasattr(self, 'status_label_2'):
                self.status_label_2.config(text="HEX copied!", fg="blue")
    
    def show_error(self, message):
        """Show error message"""
        self.picking = False
        self.pick_button.config(state="normal", text="Pick")
        self.root.config(cursor="")
        self.status_label.config(text="Error", fg="red")
        messagebox.showerror("Error", message)

def main():
    # Disable pyautogui fail-safe (optional)
    pyautogui.FAILSAFE = False
    
    root = tk.Tk()
    app = ColorPicker(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()