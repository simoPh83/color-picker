# macOS Screen Recording Permission Guide

## The Issue
Your Color Picker is capturing the desktop wallpaper instead of actual screen content because macOS requires explicit permission for screen recording.

## Quick Fix Commands

### 1. Check current permission status:
```bash
cd "/Volumes/Marketing/Simone Morciano/python working folder/colour picker/color-picker"
source venv/bin/activate
python macos_permissions.py
```

### 2. Run the Color Picker:
```bash
cd "/Volumes/Marketing/Simone Morciano/python working folder/colour picker/color-picker"
source venv/bin/activate
python color_picker.py
```

## Manual Permission Setup

### Step 1: Open System Settings
- Click Apple menu → System Settings (or System Preferences on older macOS)

### Step 2: Navigate to Privacy & Security
- Go to "Privacy & Security" → "Screen & System Audio Recording"

### Step 3: Grant Permission
- Click the lock icon and enter your password
- Find "Terminal" in the list (or add it with the + button)
- Toggle the switch to ON for Terminal

### Step 4: Restart
- Close the Color Picker if it's running
- Run the command again

## Alternative: Use Different Terminal

If you're using a different terminal app (like iTerm2), grant permission to that app instead.

## Verification
The Color Picker window title will show:
- "Color Picker (Macos - MSS)" when working correctly
- The permission checker will show "✅ Screen recording permission is working"

## Troubleshooting
If it still shows wallpaper after granting permission:
1. Completely quit and restart your terminal application
2. Run the color picker again
3. The first time you run it, macOS might show a permission dialog - click "Allow"
