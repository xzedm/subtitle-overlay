# Quick Start Guide

## What Was Fixed

The Python app had the following issues that have been resolved:

1. ✅ **"Unknown property text-shadow" Error**: PyQt6 doesn't support CSS text-shadow - replaced with background-based approach
2. ✅ **Port Already In Use Error**: Added error handling and auto-stop of previous instances
3. ✅ **Duplicate Methods in gui.py**: The `show_subtitle` method was defined 3 times - removed duplicates
4. ✅ **Missing Initialization**: Added `subtitle_history` and `max_history` attributes initialization
5. ✅ **System Tray Icon**: Now uses Qt built-in icons for cross-platform compatibility
6. ✅ **Dependencies**: PyQt6 and websockets packages installed automatically

See `FIXES_APPLIED.md` for detailed technical information about each fix.

## Running the Application

### Windows:
Simply double-click `start.bat` or run in terminal:
```cmd
start.bat
```

### Linux/macOS:
First make the script executable:
```bash
chmod +x start.sh
./start.sh
```

### Manual Start:
```bash
python app/main.py
```

### Stop the Application:
```cmd
stop.bat
```
Or right-click the system tray icon → Quit

## What to Expect

When you run the application:

1. **Floating Window**: A transparent subtitle window will appear on your screen
   - You can drag it anywhere
   - It stays on top of all other windows
   
2. **System Tray Icon**: Look for a small icon in your system tray (Windows: bottom-right corner)
   - Right-click the icon for options:
     - Show/Hide Window
     - Settings
     - Quit

3. **WebSocket Server**: The app starts a local WebSocket server on `ws://127.0.0.1:8765`
   - This is used by the browser extension to send subtitles
   - Check the console for confirmation message

## Next Steps

### Quick Test (No Browser Extension Needed):

1. Open `test.html` in your browser
2. Click "Send Test Subtitle"
3. See the subtitle appear in the floating window! ✅

### Install Browser Extension (For Real Streaming Sites):

The extension now has **auto-testing** and a **Test Connection button**!

**Chrome/Edge:**
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder from this project
5. Click the extension icon → Click "Test Connection"
6. Should show ✓ Connected!

**Firefox:**
1. Open `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Select `manifest.json` from the `extension` folder

📖 **For detailed extension setup and testing, see [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md)**

### Using with Real Videos:

1. Make sure the Python app is running (check system tray)
2. Go to YouTube and play any video
3. Enable subtitles/CC on the video player
4. Subtitles will automatically appear in the floating window! 🎬

## Customization

Right-click the subtitle window or tray icon → **Settings** to customize:
- Font size (12-48px)
- Font family
- Text color
- Background opacity
- Auto-hide behavior

## Troubleshooting

### "Port already in use" error:
**Solution:** Run `stop.bat` to close all instances, then start again:
```cmd
stop.bat
start.bat
```

### App doesn't start:
- Make sure Python 3.8+ is installed: `python --version`
- Install dependencies manually: `python -m pip install -r requirements.txt`
- Check if another instance is running: `stop.bat`

### No tray icon visible:
- The tray icon might be in the hidden icons area
- Click the up arrow in your system tray to see hidden icons
- Look for a media play icon (▶)

### "Unknown property text-shadow" warnings:
**Status:** Fixed! This warning should no longer appear.

### Extension shows "Not connected":
- Verify the Python app is running (check system tray)
- Check if port 8765 is available
- Try stopping and restarting: `stop.bat` then `start.bat`
- Check browser console (F12) for errors

### Subtitles not appearing:
- Enable subtitles on the video player
- Check if the website is supported (see README.md)
- Try refreshing the page
- Verify the app is connected (test with `python app/test_connection.py`)

### Multiple instances running:
**Solution:** Use the stop script to kill all instances:
```cmd
stop.bat
```

## Features

✓ Always-on-top floating window  
✓ Customizable appearance  
✓ Draggable and resizable  
✓ System tray integration  
✓ Subtitle history tracking  
✓ Auto-hide functionality  
✓ Works with multiple streaming sites  

## Files Modified

- `app/gui.py` - Fixed duplicate methods and added history initialization
- `app/tray.py` - Added proper system tray icon using Qt standard icons
- `start.bat` - Windows startup script with dependency checking
- `start.sh` - Linux/macOS startup script with dependency checking

Enjoy your subtitle overlay application! 🎬

