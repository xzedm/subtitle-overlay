# Rezka Setup Guide

## ✅ Rezka Support Added!

The extension now fully supports Rezka sites including:
- `rezka.fi` ✅
- `rezka.ag` ✅
- Any `*.rezka.*` domain ✅

## Quick Test

1. **Make sure the Python app is running:**
```cmd
python app/main.py
```

2. **Go to a Rezka film page:**
   - Example: https://rezka.fi/films/fantasy/107-hobbit-nezhdannoe-puteshestvie-2012-latest.html

3. **Reload the extension** (important!):
   - Go to `chrome://extensions/`
   - Find "Subtitle Overlay Connector"
   - Click the refresh button (⟳)

4. **Reload the Rezka page** (Ctrl+F5)

5. **Click the extension icon:**
   - Should show: "✓ Current page is supported"
   - Should show: "✓ Connected to desktop app"

6. **Start playing the video with subtitles enabled**

7. **Subtitles should appear in the floating window!** 🎬

## How It Works

The extension now has a **dedicated Rezka detector** that looks for subtitles using multiple methods:

### Method 1: Common Rezka Subtitle Selectors
The detector tries these CSS selectors in order:
- `.b-player__subtitle`
- `.pgs-subtitle`
- `.subtitle-text`
- `.vjs-text-track-display`
- `#subtitle-display`
- `.player-subs`
- `.rezka-subtitle`

### Method 2: HTML5 Text Tracks (Fallback)
If the above selectors don't work, it falls back to reading HTML5 video text tracks directly.

## Troubleshooting

### Extension shows "Not connected" on Rezka

**Check 1: Reload the extension**
```
chrome://extensions/ → Find extension → Click refresh (⟳)
```

**Check 2: Reload the Rezka page**
```
Press Ctrl+F5 on the Rezka page
```

**Check 3: Test the connection**
- Click extension icon
- Click "Test Connection" button
- Should show ✓ Connected

### No subtitles appearing on Rezka

**Step 1: Enable subtitles on the video player**
- Make sure subtitles/captions are turned ON in the Rezka player
- Look for a CC or subtitle button on the player

**Step 2: Check browser console for clues**
1. On the Rezka page, press F12 to open DevTools
2. Go to the "Console" tab
3. Look for messages like:
   - `"Rezka subtitle detector activated"` ✅ Good!
   - `"Rezka subtitle detected..."` ✅ Working!
   - `"WebSocket error"` ❌ Python app not running

**Step 3: Find the correct subtitle selector**

If the default selectors don't work, you can find the right one:

1. **On Rezka page with video playing and subtitles ON:**
   - Press F12 (open DevTools)
   - Click the "Elements" tab
   - Press Ctrl+F (search)
   - Look at the subtitle text on screen
   - Search for that text in the Elements tab

2. **Once you find the subtitle element:**
   - Right-click it → "Copy" → "Copy selector"
   - You'll get something like: `.some-subtitle-class`

3. **Report the selector:**
   - Let me know what selector you found
   - I can add it to the list of selectors to try

### Debug Mode

To see what's happening:

1. **Open DevTools on Rezka page (F12)**

2. **Go to Console tab**

3. **You should see:**
```
Rezka subtitle detector activated
Connected to subtitle overlay app
```

4. **When subtitles appear, you should see:**
```
Rezka subtitle detected (.some-selector): "Subtitle text here"
```

## Common Rezka Subtitle Formats

Rezka uses different subtitle formats depending on the video source:

### Format 1: Built-in Player Subtitles
- Usually appear as overlaid div elements
- Detected by CSS selectors

### Format 2: WebVTT/SRT Text Tracks
- Subtitles embedded in the video stream
- Detected by HTML5 text track API

### Format 3: Custom Player Subtitles
- Some Rezka players use custom subtitle rendering
- May need specific selectors

## Testing Checklist for Rezka

- [ ] Extension reloaded in `chrome://extensions/`
- [ ] Python app running (check system tray icon)
- [ ] Rezka page loaded/reloaded
- [ ] Extension popup shows "✓ Current page is supported"
- [ ] Extension popup shows "✓ Connected to desktop app"
- [ ] Video playing on Rezka
- [ ] Subtitles enabled on Rezka player
- [ ] Browser console shows "Rezka subtitle detector activated"
- [ ] Subtitles appear in floating window

## Advanced: Adding Custom Selectors

If the built-in selectors don't work for your Rezka site:

1. **Find the selector** (see "Find the correct subtitle selector" above)

2. **Edit `extension/content.js`:**

Find the `detectRezka()` method and add your selector to the array:

```javascript
const selectors = [
  ".b-player__subtitle",
  ".pgs-subtitle",
  ".subtitle-text",
  ".vjs-text-track-display",
  "#subtitle-display",
  ".player-subs",
  ".rezka-subtitle",
  ".your-custom-selector"  // <-- Add here
];
```

3. **Reload the extension** in `chrome://extensions/`

4. **Test again!**

## Example Rezka URLs to Test

Try these Rezka pages:
- https://rezka.fi/films/
- https://rezka.ag/films/
- https://rezka.fi/series/

## Need Help?

If subtitles still don't work:

1. **Collect this info:**
   - Rezka URL you're testing
   - What you see in browser console (F12 → Console)
   - Whether subtitles are visible on the Rezka player
   - Screenshot of the subtitle element in DevTools

2. **Try the generic detector as fallback:**
   - The extension automatically falls back to generic HTML5 detection
   - Works with most HTML5 video players

3. **Test with other sites:**
   - Try YouTube to confirm extension works
   - This helps isolate if it's a Rezka-specific issue

## Summary

✅ **Rezka is now supported!**
✅ **Multiple detection methods** (7 selectors + HTML5 fallback)
✅ **All Rezka domains** (rezka.fi, rezka.ag, *.rezka.*)
✅ **Debug logging** to console for troubleshooting

**Just reload the extension and the Rezka page, and it should work!** 🎉



