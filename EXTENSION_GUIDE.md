# Browser Extension Setup & Testing Guide

## ✅ All Fixed!

The extension is now updated with:
- **Auto-testing** connection when popup opens
- **Test Connection button** to manually test
- **Better status indicators** (green = connected, red = disconnected)
- **Page detection** - shows if you're on a supported streaming site
- **Helpful notifications** - tells you what's wrong if not connected

## Quick Test (Without Going to Netflix/YouTube)

### Option 1: Use test.html (Easiest)

1. Make sure the Python app is running:
```cmd
python app/main.py
```

2. Open `test.html` in your browser (double-click the file)

3. The page will auto-connect and show you the connection status

4. Click "Send Test Subtitle" to send a subtitle to the floating window

5. You should see the test subtitle appear in the floating window!

### Option 2: Use Extension Popup Test Button

1. Make sure the Python app is running

2. Click the extension icon (anywhere, any page)

3. Click the **"Test Connection"** button in the popup

4. If connected, you'll see:
   - ✓ Green indicator
   - "Connected to desktop app"
   - A test message will appear in the floating window!

## Installing the Extension

### For Chrome/Edge:

1. Open Chrome/Edge and go to: `chrome://extensions/`

2. Enable **"Developer mode"** (toggle in top-right corner)

3. Click **"Load unpacked"**

4. Navigate to your project folder and select the `extension` folder

5. The extension should now appear in your extensions list

6. Pin it to toolbar for easy access (click the puzzle piece icon → pin)

### For Firefox:

1. Open Firefox and go to: `about:debugging#/runtime/this-firefox`

2. Click **"Load Temporary Add-on..."**

3. Navigate to the `extension` folder and select `manifest.json`

4. The extension will load (note: it's temporary and will be removed when you close Firefox)

## Using the Extension

### Understanding the Status Messages

When you click the extension icon, you'll see:

**✓ Connected to desktop app** (Green dot)
- Desktop app is running
- WebSocket connection is active
- Ready to send subtitles

**❌ Desktop app not running** (Red dot)
- Can't connect to port 8765
- Make sure Python app is running: `python app/main.py`

**⚠ Navigate to a streaming site** (Orange text)
- You're not on a supported website
- The content script only runs on Netflix, YouTube, etc.

### Supported Websites

The extension automatically detects subtitles on:
- ✅ Netflix (`netflix.com`)
- ✅ YouTube (`youtube.com`)
- ✅ Amazon Prime Video (`amazon.com`)
- ✅ Disney+ (`disneyplus.com`)
- ✅ Hulu (`hulu.com`)
- ✅ HBO Max (`hbomax.com`)
- ✅ **Rezka** (`rezka.fi`, `rezka.ag`, and all `*.rezka.*` domains) - **NEW!**
  - Dedicated detector with 7+ subtitle selectors
  - HTML5 text track fallback
  - See [REZKA_SETUP.md](REZKA_SETUP.md) for details

### Testing on a Real Streaming Site

1. **Start the Python app:**
```cmd
python app/main.py
```

2. **Go to YouTube:**
   - Open https://youtube.com
   - Play any video with subtitles
   - Enable closed captions (CC button)

3. **Check extension:**
   - Click the extension icon
   - Should show: "✓ Connected to desktop app"
   - Should show: "✓ Current page is supported"

4. **Watch the magic:**
   - Subtitles from the video will appear in the floating window!
   - The floating window stays on top of everything

## Troubleshooting

### Extension shows "Not connected"

**Check 1: Is the Python app running?**
```cmd
# Start it if not running
python app/main.py

# You should see:
# Application started. WebSocket server on ws://127.0.0.1:8765
```

**Check 2: Click "Test Connection" button**
- Open extension popup
- Click "Test Connection"
- If it fails, the desktop app isn't running

**Check 3: Try test.html**
- Open `test.html` in browser
- If it connects, extension might need to be reloaded

**Check 4: Reload the extension**
1. Go to `chrome://extensions/`
2. Find "Subtitle Overlay Connector"
3. Click the refresh icon (⟳)
4. Try again

### Extension works but no subtitles appear

**On YouTube:**
- Make sure CC (Closed Captions) is enabled
- Click the CC button on the video player
- Refresh the page if needed

**On Netflix:**
- Turn on subtitles in the Netflix player
- Make sure you're watching a video (not browsing)

**General:**
- Check if the floating window is hidden behind other windows
- Right-click system tray icon → "Show Window"
- Try sending a test subtitle from `test.html`

### "Current page is not supported"

- This is normal if you're not on a streaming site
- Navigate to YouTube, Netflix, etc.
- The extension will work automatically once you're on a supported site

### Permission errors when installing

- Make sure you enabled "Developer mode" in `chrome://extensions/`
- Try removing and re-adding the extension
- Check that all files in the `extension` folder are present

## Testing Checklist

Use this checklist to verify everything works:

- [ ] Python app starts without errors
- [ ] System tray icon appears
- [ ] Floating subtitle window is visible
- [ ] Extension installed in browser
- [ ] Extension popup shows "Test Connection" button
- [ ] Test Connection button works (shows ✓ Connected)
- [ ] `test.html` connects and sends subtitles successfully
- [ ] Test subtitle appears in floating window
- [ ] On YouTube with CC enabled, subtitles appear in floating window
- [ ] Can drag the floating window around
- [ ] Can right-click floating window for settings

## Advanced: Debugging

### Check Browser Console

1. Right-click extension icon → "Inspect"
2. Look for console messages:
   - ✅ "Connected to subtitle overlay app"
   - ❌ "WebSocket error" (means app not running)

### Check Python Console

Look for these messages:
```
Application started. WebSocket server on ws://127.0.0.1:8765
WebSocket server started on ws://127.0.0.1:8765
Client connected. Total clients: 1
```

### Network Tab

1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter: "WS" (WebSocket)
4. You should see a WebSocket connection to `127.0.0.1:8765`

## Extension Version

Current version: **1.0.0**

To update the extension after changes:
1. Go to `chrome://extensions/`
2. Click the refresh button (⟳) on the extension card
3. No need to reload pages - just reload the extension

## Need Help?

1. **Check Python app is running:** Look for system tray icon
2. **Test with test.html:** Confirms WebSocket works
3. **Click "Test Connection":** In extension popup
4. **Check console:** F12 → Console for error messages
5. **Reload extension:** `chrome://extensions/` → refresh button

---

**Quick Start:**
1. Run: `python app/main.py`
2. Open: `test.html` in browser
3. Click: "Send Test Subtitle"
4. See: Subtitle in floating window ✅

Everything working? Head to YouTube and turn on CC to see live subtitles! 🎉

