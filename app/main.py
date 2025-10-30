import sys
import asyncio
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QThread

from config import ConfigManager
from gui import SubtitleWindow
from server import SubtitleServer
from tray import TrayIcon


class ServerThread(QThread):
    """Thread to run async WebSocket server"""
    error_occurred = pyqtSignal(str)
    
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.loop = None
    
    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.server.start())
        except OSError as e:
            if e.errno == 10048:
                self.error_occurred.emit("Port already in use")
            else:
                self.error_occurred.emit(str(e))
        except Exception as e:
            self.error_occurred.emit(str(e))


class SubtitleApp(QObject):
    subtitle_received = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        
        # Initialize server
        host = self.config.get('server', 'host')
        port = self.config.get('server', 'port')
        self.server = SubtitleServer(host, port)
        self.server.set_subtitle_callback(self.on_subtitle_received)
        
        # Start server in separate thread
        self.server_thread = ServerThread(self.server)
        self.server_thread.error_occurred.connect(self.on_server_error)
        self.server_thread.start()
        
        # Initialize GUI
        self.window = SubtitleWindow(self.config)
        self.subtitle_received.connect(self.window.show_subtitle)
        
        # Initialize tray icon
        self.tray = TrayIcon()
        self.tray.show_window_signal.connect(self.window.show)
        self.tray.hide_window_signal.connect(self.window.hide)
        self.tray.settings_signal.connect(self.window.open_settings)
        self.tray.quit_signal.connect(self.quit_app)
        self.tray.show()
        
        # Show window initially
        self.window.show()
        
        print(f"Application started. WebSocket server on ws://{host}:{port}")
    
    def on_subtitle_received(self, text: str):
        """Called when subtitle is received from browser"""
        # Emit signal to update GUI (thread-safe)
        self.subtitle_received.emit(text)
    
    def on_server_error(self, error_msg: str):
        """Handle server errors"""
        from PyQt6.QtWidgets import QMessageBox
        if "Port already in use" in error_msg:
            QMessageBox.critical(
                None,
                "Server Error",
                f"Port {self.config.get('server', 'port')} is already in use!\n\n"
                "Another instance of this application may be running.\n"
                "Please close it first, or change the port in settings.",
                QMessageBox.StandardButton.Ok
            )
        else:
            QMessageBox.critical(
                None,
                "Server Error",
                f"Failed to start WebSocket server:\n{error_msg}",
                QMessageBox.StandardButton.Ok
            )
        QApplication.quit()
    
    def quit_app(self):
        """Clean shutdown"""
        self.window.save_window_settings()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running when window is closed
    
    subtitle_app = SubtitleApp()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()