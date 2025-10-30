from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject, pyqtSignal

class TrayIcon(QObject):
    show_window_signal = pyqtSignal()
    hide_window_signal = pyqtSignal()
    quit_signal = pyqtSignal()
    settings_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tray = QSystemTrayIcon(parent)
        
        # Use a built-in Qt icon so it works on all platforms
        style = QApplication.style()
        icon = style.standardIcon(style.StandardPixmap.SP_MediaPlay)
        self.tray.setIcon(icon)
        
        self.tray.setToolTip("Subtitle Overlay")
        
        # Create menu
        self.menu = QMenu()
        
        self.show_action = QAction("Show Window", self)
        self.show_action.triggered.connect(self.show_window_signal.emit)
        self.menu.addAction(self.show_action)
        
        self.hide_action = QAction("Hide Window", self)
        self.hide_action.triggered.connect(self.hide_window_signal.emit)
        self.menu.addAction(self.hide_action)
        
        self.menu.addSeparator()
        
        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.settings_signal.emit)
        self.menu.addAction(self.settings_action)
        
        self.menu.addSeparator()
        
        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(self.quit_signal.emit)
        self.menu.addAction(self.quit_action)
        
        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.on_tray_activated)
    
    def show(self):
        self.tray.show()
    
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window_signal.emit()
    
    def show_message(self, title, message):
        self.tray.showMessage(title, message)