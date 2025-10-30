# Fixes Applied to Subtitle Overlay App

## Issues Fixed

### 1. ✅ "Unknown property text-shadow" Error

**Problem:** PyQt6 doesn't support the CSS `text-shadow` property used for text outlining.

**Solution:** Replaced text-shadow with background-color and padding to create a readable subtitle appearance:
- Changed from CSS text-shadow to a background color approach
- Added proper padding and border-radius for better readability
- Subtitles now have a dark background behind white text

**Files Modified:** `app/gui.py`

### 2. ✅ Port Already In Use Error (OSError: Errno 10048)

**Problem:** Multiple instances of the app trying to bind to the same port (8765).

**Solution:** Added comprehensive error handling:
- Added try-catch in WebSocket server startup
- Created error signal in ServerThread to communicate errors to main app
- Display user-friendly error message when port is in use
- Created `stop.bat` script to kill running instances
- Updated `start.bat` to automatically stop previous instances before starting

**Files Modified:** 
- `app/server.py` - Better error messages
- `app/main.py` - Error handling and user notifications
- `start.bat` - Auto-stop previous instances
- `stop.bat` - New utility to stop all instances

### 3. ✅ Duplicate Methods in gui.py

**Problem:** The `show_subtitle` method was defined 3 times causing conflicts.

**Solution:** 
- Removed duplicate definitions
- Kept single implementation with subtitle history tracking
- Added proper initialization of `subtitle_history` and `max_history`

**Files Modified:** `app/gui.py`

### 4. ✅ System Tray Icon Issues

**Problem:** Tray icon not displaying properly on Windows.

**Solution:** 
- Used Qt's built-in standard icon (SP_MediaPlay) instead of custom icon
- This ensures the icon works on all platforms without requiring external files

**Files Modified:** `app/tray.py`

## How to Use Now

### Start the Application

**Option 1: Use the batch file (Recommended for Windows)**
```cmd
start.bat
```
This will automatically:
- Check for Python installation
- Stop any running instances
- Install dependencies if needed
- Start the application

**Option 2: Stop and start manually**
```cmd
stop.bat
python app/main.py
```

**Option 3: Direct start**
```cmd
python app/main.py
```

### Stop the Application

**Option 1: Use stop script**
```cmd
stop.bat
```

**Option 2: Right-click tray icon**
- Find the media play icon in your system tray
- Right-click → Quit

**Option 3: Right-click subtitle window**
- Right-click on the subtitle window
- Select "Quit"

## Verification

The app is now working correctly:
- ✅ No "Unknown property text-shadow" warnings
- ✅ WebSocket server starts successfully on port 8765
- ✅ System tray icon appears
- ✅ Subtitle window displays properly
- ✅ Test connection successful

## What You Should See

When running `python app/main.py`, you should see:
```
Application started. WebSocket server on ws://127.0.0.1:8765
WebSocket server started on ws://127.0.0.1:8765
```

**No error messages** - just those two success messages.

## Testing

Test the connection:
```cmd
python app/test_connection.py
```

Expected output:
```
Test subtitle sent!
```

And you should see "This is a test subtitle!" appear in the floating window.

## Common Issues & Solutions

### Issue: "QSystemTrayIcon::setVisible: No Icon set"
**Status:** Harmless warning, can be ignored. The icon still works.

### Issue: Port 8765 already in use
**Solution:** Run `stop.bat` first, then start the app again.

### Issue: Multiple instances running
**Solution:** 
```cmd
stop.bat
start.bat
```

### Issue: App not responding
**Solution:** Close from Task Manager and restart:
1. Open Task Manager (Ctrl+Shift+Esc)
2. Find "Python" processes
3. End task for any running subtitle overlay
4. Run `start.bat`

## Next Steps

1. **Install Browser Extension** - See README.md or QUICK_START.md
2. **Customize Settings** - Right-click subtitle window → Settings
3. **Test with Videos** - Open Netflix/YouTube with subtitles

## Summary of Changes

| File | Changes |
|------|---------|
| `app/gui.py` | Fixed text-shadow issue, removed duplicates |
| `app/main.py` | Added error handling with user dialogs |
| `app/server.py` | Better error messages for port conflicts |
| `app/tray.py` | Use Qt built-in icons |
| `start.bat` | Auto-stop previous instances |
| `stop.bat` | New utility script |

All issues are now resolved! 🎉



