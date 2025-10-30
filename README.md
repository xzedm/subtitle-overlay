# Floating Subtitle Overlay

A desktop application that displays subtitles from streaming websites in a floating, always-on-top window.

## Features

- ✨ Floating window that stays above all applications (even fullscreen)
- 🎬 Supports Netflix, YouTube, Amazon Prime, Disney+, Hulu, HBO Max, and more
- ⚙️ Customizable font, colors, size, and opacity
- 🖱️ Draggable and resizable window
- 💾 Settings persist between sessions
- 🔌 Real-time subtitle synchronization via WebSocket

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome or Firefox browser

### Step 1: Install Python Application

1. Clone or download this repository
2. Open terminal/command prompt in the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app/main.py
```

The app will start and minimize to the system tray.

### Step 2: Install Browser Extension

#### For Chrome/Edge:

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Select the `extension` folder from this project
5. The extension icon should appear in your toolbar

#### For Firefox:

1. Open Firefox and go to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Navigate to the `extension` folder and select `manifest.json`

### Step 3: Connect Everything

1. Make sure the Python desktop app is running (check system tray)
2. Open a streaming website (e.g., Netflix, YouTube)
3. Click the extension icon - it should show "Connected to desktop app"
4. Play a video with subtitles enabled
5. Subtitles should appear in the floating window!

## Usage

### Basic Controls

- **Drag window**: Click and drag anywhere on the subtitle window
- **Resize**: Drag the edges or corners (resize functionality depends on OS)
- **Right-click menu**: Access settings, reset position, or quit
- **System tray**: Right-click the tray icon for quick actions

### Keyboard Shortcuts

- `Ctrl+Shift+S` - Show/hide subtitle window
- `Ctrl+Shift+D` - Toggle draggable mode
- `Ctrl+Shift+R` - Reset window position to center
- `Ctrl+Shift+C` - Open settings
- `Ctrl+Shift+Q` - Quit application

### Settings

Access settings by:

- Right-clicking the subtitle window → "Settings"
- Right-clicking the system tray icon → "Settings"

Available settings:

- **Font Size**: 12-48px (default: 22px)
- **Font Family**: Arial, Helvetica, Verdana, etc.
- **Text Color**: Any color via color picker
- **Background Opacity**: 0-100% transparency
- **Auto-hide**: Automatically hide subtitles after 4 seconds of inactivity

## Troubleshooting

### Extension shows "Not connected"

1. Make sure the Python app is running (check system tray)
2. Check if port 8765 is available (not blocked by firewall)
3. Try restarting the Python application
4. Check console for errors: Right-click extension → "Inspect"

### No subtitles appearing

1. Make sure subtitles are enabled on the video player
2. Check if the website is supported (see list below)
3. Try refreshing the page
4. Check browser console (F12) for errors

### Subtitles appear delayed

- The delay should be < 300ms normally
- Close other applications to free up resources
- Check if your system is under heavy load

### Window not staying on top

- Restart the application
- Check "Always on top" setting is enabled
- Some fullscreen applications may override this behavior

## Supported Streaming Sites

Currently supported:

- ✅ Netflix
- ✅ YouTube
- ✅ Amazon Prime Video
- ✅ Disney+
- ✅ Hulu
- ✅ HBO Max
- ✅ Rezka
- ✅ Generic HTML5 video players with text tracks

## Configuration File

Settings are saved in:

- **Windows**: `C:\Users\<username>\.subtitle_overlay\config.json`
- **macOS**: `/Users/<username>/.subtitle_overlay/config.json`
- **Linux**: `/home/<username>/.subtitle_overlay/config.json`

You can manually edit this file if needed (app must be closed).

## Security

- All communication happens locally (localhost only)
- No data is sent to external servers
- WebSocket server only accepts connections from 127.0.0.1
- Extension only sends subtitle text, no personal data

## Building Executable (Optional)

To create a standalone executable:

### Windows:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico app/main.py
```

### macOS:

```bash
pip install py2app
python setup.py py2app
```

### Linux:

```bash
pip install pyinstaller
pyinstaller --onefile app/main.py
```

## Known Issues

- Some fullscreen applications may cover the subtitle window
- Browser extension needs to be reloaded after updating
- First connection may take a few seconds

## FAQ

**Q: Can I use this with downloaded videos?**
A: Currently, it only works with streaming websites via the browser extension.

**Q: Does this work with multiple monitors?**
A: Yes! The window position is saved per monitor.

**Q: Can I customize the keyboard shortcuts?**
A: Not yet, but this feature is planned for a future update.

**Q: Is this legal?**
A: Yes, this tool only displays subtitles locally on your device.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - Feel free to use and modify as needed.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
