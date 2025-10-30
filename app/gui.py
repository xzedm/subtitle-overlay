import sys
import time
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QDialog, 
                             QPushButton, QSlider, QColorDialog, QComboBox,
                             QSpinBox, QCheckBox, QFormLayout, QHBoxLayout,
                             QTabWidget, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QCursor

class SubtitleWindow(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.dragging = False
        self.drag_position = QPoint()
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.hide_subtitle)
        self.subtitle_history = []
        self.max_history = 100
        
        self.init_ui()
        self.load_window_settings()
    
    def init_ui(self):
        # Remove window frame and make it stay on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create subtitle label
        self.subtitle_label = QLabel("")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        
        # Apply text styling
        self.update_text_style()
        
        layout.addWidget(self.subtitle_label)
        self.setLayout(layout)
        
        # Set window properties
        self.setMinimumSize(400, 60)
        
        # Apply background styling
        self.update_background_style()
    
    def update_text_style(self):
        """Update subtitle text styling from config"""
        font_family = self.config.get('text', 'font_family')
        font_size = self.config.get('text', 'font_size')
        text_color = self.config.get('text', 'color')
        
        font = QFont(font_family, font_size)
        font.setBold(True)
        self.subtitle_label.setFont(font)
        
        # PyQt6 doesn't support text-shadow, use background and padding instead
        if self.config.get('text', 'outline'):
            outline_color = self.config.get('text', 'outline_color')
            # Use border and padding for outline effect
            self.subtitle_label.setStyleSheet(f"""
                QLabel {{
                color: {text_color};
                    background-color: {outline_color};
                    padding: 8px 16px;
                    border-radius: 4px;
                }}
            """)
        else:
            self.subtitle_label.setStyleSheet(f"""
                QLabel {{
                    color: {text_color};
                    background-color: transparent;
                    padding: 8px 16px;
                }}
            """)
    
    def update_background_style(self):
        """Update window background from config"""
        bg_color = self.config.get('background', 'color')
        bg_opacity = self.config.get('background', 'opacity')
        
        # Convert hex color and apply opacity
        color = QColor(bg_color)
        color.setAlphaF(bg_opacity)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        window_opacity = self.config.get('window', 'opacity')
        self.setWindowOpacity(window_opacity)
    
    def show_subtitle(self, text: str):
        """Display subtitle text and save to history"""
        self.subtitle_label.setText(text)
        self.show()
        
        # Add to history
        self.subtitle_history.append({
            'text': text,
            'timestamp': time.time()
        })
        
        # Limit history size
        if len(self.subtitle_history) > self.max_history:
            self.subtitle_history.pop(0)
        
        # Restart auto-hide timer if enabled
        if self.config.get('behavior', 'auto_hide'):
            delay = self.config.get('behavior', 'auto_hide_delay')
            self.auto_hide_timer.start(delay)
    
    def hide_subtitle(self):
        """Hide subtitle text"""
        self.subtitle_label.setText("")
        self.auto_hide_timer.stop()
    
    def load_window_settings(self):
        """Load window position and size from config"""
        x = self.config.get('window', 'x')
        y = self.config.get('window', 'y')
        width = self.config.get('window', 'width')
        height = self.config.get('window', 'height')
        
        self.setGeometry(x, y, width, height)
    
    def save_window_settings(self):
        """Save current window position and size"""
        geometry = self.geometry()
        self.config.set('window', 'x', value=geometry.x())
        self.config.set('window', 'y', value=geometry.y())
        self.config.set('window', 'width', value=geometry.width())
        self.config.set('window', 'height', value=geometry.height())
    
    # Mouse event handlers for dragging
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.save_window_settings()
            event.accept()
    
    def contextMenuEvent(self, event):
        """Right-click to open settings"""
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        settings_action = menu.addAction("Settings")
        reset_action = menu.addAction("Reset Position")
        quit_action = menu.addAction("Quit")
        
        action = menu.exec(event.globalPos())
        
        if action == settings_action:
            self.open_settings()
        elif action == reset_action:
            self.reset_position()
        elif action == quit_action:
            sys.exit(0)
    
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self.config, self)
        if dialog.exec():
            self.update_text_style()
            self.update_background_style()
            # Apply new window size
            self.resize(
                self.config.get('window', 'width'),
                self.config.get('window', 'height')
            )
    
    def reset_position(self):
        """Reset window to center of screen"""
        screen = self.screen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            screen.height() - self.height() - 100
        )
        self.save_window_settings()


class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Subtitle Overlay - Settings")
        self.setModal(True)
        self.setMinimumSize(500, 500)
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Text Settings Tab
        text_tab = self.create_text_tab()
        tabs.addTab(text_tab, "Text")
        
        # Window Settings Tab
        window_tab = self.create_window_tab()
        tabs.addTab(window_tab, "Window")
        
        # Behavior Settings Tab
        behavior_tab = self.create_behavior_tab()
        tabs.addTab(behavior_tab, "Behavior")
        
        # About Tab
        about_tab = self.create_about_tab()
        tabs.addTab(about_tab, "About")
        
        main_layout.addWidget(tabs)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save && Close")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setDefault(True)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_to_defaults)
        
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
    
    def create_text_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Font family
        font_group = QGroupBox("Font")
        font_layout = QFormLayout()
        
        self.font_combo = QComboBox()
        fonts = ['Arial', 'Helvetica', 'Verdana', 'Times New Roman', 'Courier New', 
                 'Georgia', 'Comic Sans MS', 'Trebuchet MS', 'Impact']
        self.font_combo.addItems(fonts)
        current_font = self.config.get('text', 'font_family')
        index = self.font_combo.findText(current_font)
        if index >= 0:
            self.font_combo.setCurrentIndex(index)
        font_layout.addRow("Font Family:", self.font_combo)
        
        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(self.config.get('text', 'font_size'))
        self.font_size_spin.setSuffix(" px")
        font_layout.addRow("Font Size:", self.font_size_spin)
        
        font_group.setLayout(font_layout)
        layout.addRow(font_group)
        
        # Colors
        color_group = QGroupBox("Colors")
        color_layout = QFormLayout()
        
        # Text color
        text_color_layout = QHBoxLayout()
        self.text_color_btn = QPushButton("Choose Color")
        self.text_color_btn.clicked.connect(self.choose_text_color)
        self.text_color_preview = QLabel("     ")
        current_color = self.config.get('text', 'color')
        self.text_color_preview.setStyleSheet(f"background-color: {current_color}; border: 1px solid black;")
        self.selected_text_color = current_color
        text_color_layout.addWidget(self.text_color_btn)
        text_color_layout.addWidget(self.text_color_preview)
        text_color_layout.addStretch()
        color_layout.addRow("Text Color:", text_color_layout)
        
        # Background color
        bg_color_layout = QHBoxLayout()
        self.bg_color_btn = QPushButton("Choose Color")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        self.bg_color_preview = QLabel("     ")
        current_bg = self.config.get('background', 'color')
        self.bg_color_preview.setStyleSheet(f"background-color: {current_bg}; border: 1px solid black;")
        self.selected_bg_color = current_bg
        bg_color_layout.addWidget(self.bg_color_btn)
        bg_color_layout.addWidget(self.bg_color_preview)
        bg_color_layout.addStretch()
        color_layout.addRow("Background Color:", bg_color_layout)
        
        color_group.setLayout(color_layout)
        layout.addRow(color_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_window_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Window size
        size_group = QGroupBox("Window Size")
        size_layout = QFormLayout()
        
        self.window_width = QSpinBox()
        self.window_width.setRange(200, 2000)
        self.window_width.setValue(self.config.get('window', 'width'))
        self.window_width.setSuffix(" px")
        size_layout.addRow("Width:", self.window_width)
        
        self.window_height = QSpinBox()
        self.window_height.setRange(50, 500)
        self.window_height.setValue(self.config.get('window', 'height'))
        self.window_height.setSuffix(" px")
        size_layout.addRow("Height:", self.window_height)
        
        size_group.setLayout(size_layout)
        layout.addRow(size_group)
        
        # Opacity
        opacity_group = QGroupBox("Transparency")
        opacity_layout = QFormLayout()
        
        self.window_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.window_opacity_slider.setRange(10, 100)
        self.window_opacity_slider.setValue(int(self.config.get('window', 'opacity') * 100))
        self.opacity_label = QLabel(f"{self.window_opacity_slider.value()}%")
        self.window_opacity_slider.valueChanged.connect(
            lambda v: self.opacity_label.setText(f"{v}%")
        )
        opacity_layout.addRow("Window Opacity:", self.window_opacity_slider)
        opacity_layout.addRow("", self.opacity_label)
        
        self.bg_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.bg_opacity_slider.setRange(0, 100)
        self.bg_opacity_slider.setValue(int(self.config.get('background', 'opacity') * 100))
        self.bg_opacity_label = QLabel(f"{self.bg_opacity_slider.value()}%")
        self.bg_opacity_slider.valueChanged.connect(
            lambda v: self.bg_opacity_label.setText(f"{v}%")
        )
        opacity_layout.addRow("Background Opacity:", self.bg_opacity_slider)
        opacity_layout.addRow("", self.bg_opacity_label)
        
        opacity_group.setLayout(opacity_layout)
        layout.addRow(opacity_group)
        
        # Always on top
        other_group = QGroupBox("Other")
        other_layout = QFormLayout()
        
        self.always_on_top = QCheckBox("Keep window above all others")
        self.always_on_top.setChecked(self.config.get('window', 'always_on_top'))
        other_layout.addRow(self.always_on_top)
        
        other_group.setLayout(other_layout)
        layout.addRow(other_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_behavior_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Auto-hide
        auto_hide_group = QGroupBox("Auto-Hide")
        auto_hide_layout = QFormLayout()
        
        self.auto_hide_check = QCheckBox("Hide subtitles when inactive")
        self.auto_hide_check.setChecked(self.config.get('behavior', 'auto_hide'))
        auto_hide_layout.addRow(self.auto_hide_check)
        
        self.auto_hide_delay = QSpinBox()
        self.auto_hide_delay.setRange(1, 10)
        self.auto_hide_delay.setValue(self.config.get('behavior', 'auto_hide_delay') // 1000)
        self.auto_hide_delay.setSuffix(" seconds")
        auto_hide_layout.addRow("Hide after:", self.auto_hide_delay)
        
        auto_hide_group.setLayout(auto_hide_layout)
        layout.addRow(auto_hide_group)
        
        # Max lines
        display_group = QGroupBox("Display")
        display_layout = QFormLayout()
        
        self.max_lines = QSpinBox()
        self.max_lines.setRange(1, 5)
        self.max_lines.setValue(self.config.get('behavior', 'max_lines'))
        display_layout.addRow("Maximum subtitle lines:", self.max_lines)
        
        display_group.setLayout(display_layout)
        layout.addRow(display_group)
        
        # Shortcuts info
        shortcuts_group = QGroupBox("Keyboard Shortcuts")
        shortcuts_layout = QVBoxLayout()
        
        shortcuts_text = QLabel(
            "<b>Available shortcuts:</b><br>"
            "• <b>Ctrl+Shift+S</b> - Show/hide subtitle window<br>"
            "• <b>Ctrl+Shift+R</b> - Reset window position<br>"
            "• <b>Ctrl+Shift+C</b> - Open settings<br>"
            "• <b>Ctrl+Shift+Q</b> - Quit application"
        )
        shortcuts_text.setWordWrap(True)
        shortcuts_layout.addWidget(shortcuts_text)
        
        note_label = QLabel("<i>Note: Shortcuts are currently fixed and cannot be customized.</i>")
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: gray; font-size: 10px;")
        shortcuts_layout.addWidget(note_label)
        
        shortcuts_group.setLayout(shortcuts_layout)
        layout.addRow(shortcuts_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_about_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("<h2>Subtitle Overlay</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        version = QLabel("<b>Version:</b> 1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        description = QLabel(
            "A desktop application that displays subtitles from streaming websites<br>"
            "in a floating, always-on-top window."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
        layout.addSpacing(20)
        
        features = QLabel(
            "<b>Supported Websites:</b><br>"
            "• Netflix<br>"
            "• YouTube<br>"
            "• Amazon Prime Video<br>"
            "• Disney+<br>"
            "• Hulu<br>"
            "• HBO Max<br>"
            "• Rezka (rezka.fi, rezka.ag)"
        )
        features.setWordWrap(True)
        layout.addWidget(features)
        
        layout.addSpacing(20)
        
        info = QLabel(
            "<b>WebSocket Server:</b> ws://127.0.0.1:8765<br>"
            "<b>Config Location:</b> ~/.subtitle_overlay/config.json"
        )
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def choose_text_color(self):
        color = QColorDialog.getColor(QColor(self.selected_text_color))
        if color.isValid():
            self.selected_text_color = color.name()
            self.text_color_preview.setStyleSheet(
                f"background-color: {self.selected_text_color}; border: 1px solid black;"
            )
    
    def choose_bg_color(self):
        color = QColorDialog.getColor(QColor(self.selected_bg_color))
        if color.isValid():
            self.selected_bg_color = color.name()
            self.bg_color_preview.setStyleSheet(
                f"background-color: {self.selected_bg_color}; border: 1px solid black;"
            )
    
    def reset_to_defaults(self):
        reply = QMessageBox.question(
            self,
            "Reset to Defaults",
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            defaults = self.config.get_default_settings()
            
            # Text settings
            self.font_combo.setCurrentText(defaults['text']['font_family'])
            self.font_size_spin.setValue(defaults['text']['font_size'])
            self.selected_text_color = defaults['text']['color']
            self.text_color_preview.setStyleSheet(
                f"background-color: {self.selected_text_color}; border: 1px solid black;"
            )
            self.selected_bg_color = defaults['background']['color']
            self.bg_color_preview.setStyleSheet(
                f"background-color: {self.selected_bg_color}; border: 1px solid black;"
            )
            
            # Window settings
            self.window_width.setValue(defaults['window']['width'])
            self.window_height.setValue(defaults['window']['height'])
            self.window_opacity_slider.setValue(int(defaults['window']['opacity'] * 100))
            self.bg_opacity_slider.setValue(int(defaults['background']['opacity'] * 100))
            self.always_on_top.setChecked(defaults['window']['always_on_top'])
            
            # Behavior settings
            self.auto_hide_check.setChecked(defaults['behavior']['auto_hide'])
            self.auto_hide_delay.setValue(defaults['behavior']['auto_hide_delay'] // 1000)
            self.max_lines.setValue(defaults['behavior']['max_lines'])
            
            QMessageBox.information(self, "Reset Complete", "Settings have been reset to defaults.")
    
    def save_settings(self):
        # Text settings
        self.config.set('text', 'font_size', value=self.font_size_spin.value())
        self.config.set('text', 'font_family', value=self.font_combo.currentText())
        self.config.set('text', 'color', value=self.selected_text_color)
        self.config.set('background', 'color', value=self.selected_bg_color)
        
        # Window settings
        self.config.set('window', 'width', value=self.window_width.value())
        self.config.set('window', 'height', value=self.window_height.value())
        self.config.set('window', 'opacity', value=self.window_opacity_slider.value() / 100)
        self.config.set('background', 'opacity', value=self.bg_opacity_slider.value() / 100)
        self.config.set('window', 'always_on_top', value=self.always_on_top.isChecked())
        
        # Behavior settings
        self.config.set('behavior', 'auto_hide', value=self.auto_hide_check.isChecked())
        self.config.set('behavior', 'auto_hide_delay', value=self.auto_hide_delay.value() * 1000)
        self.config.set('behavior', 'max_lines', value=self.max_lines.value())
        
        self.accept()