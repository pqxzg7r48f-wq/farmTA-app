"""
FarmTA - Application Styles
Quản lý theme và style toàn cục cho ứng dụng
"""

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class AppStyles:
    """Class quản lý toàn bộ style của ứng dụng"""
    
    # Màu sắc chính
    PRIMARY_COLOR = "#2E7D32"      # Xanh lá
    PRIMARY_DARK = "#1B5E20"       # Xanh đậm
    PRIMARY_LIGHT = "#4CAF50"      # Xanh nhạt
    
    SECONDARY_COLOR = "#1976D2"    # Xanh dương
    SECONDARY_DARK = "#0D47A1"     # Xanh dương đậm
    
    ACCENT_COLOR = "#FF6F00"       # Cam
    
    DANGER_COLOR = "#D32F2F"       # Đỏ
    WARNING_COLOR = "#F57C00"      # Cam cảnh báo
    SUCCESS_COLOR = "#388E3C"      # Xanh thành công
    INFO_COLOR = "#1976D2"         # Xanh thông tin
    
    BACKGROUND_COLOR = "#F5F5F5"   # Xám nhạt
    CARD_COLOR = "#FFFFFF"         # Trắng
    TEXT_PRIMARY = "#212121"       # Đen
    TEXT_SECONDARY = "#757575"     # Xám
    
    BORDER_COLOR = "#BDBDBD"       # Viền xám
    
    # Font
    FONT_FAMILY = "Segoe UI, Arial, sans-serif"
    
    @staticmethod
    def get_main_stylesheet():
        """Lấy stylesheet chính cho ứng dụng"""
        return f"""
        * {{
            font-family: {AppStyles.FONT_FAMILY};
            color: {AppStyles.TEXT_PRIMARY};
        }}
        
        QMainWindow {{
            background-color: {AppStyles.BACKGROUND_COLOR};
        }}
        
        QWidget {{
            background-color: {AppStyles.BACKGROUND_COLOR};
        }}
        
        /* Header */
        QLabel {{
            color: {AppStyles.TEXT_PRIMARY};
        }}
        
        /* Tabs */
        QTabWidget::pane {{
            border: 1px solid {AppStyles.BORDER_COLOR};
            background-color: {AppStyles.CARD_COLOR};
        }}
        
        QTabBar::tab {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            color: {AppStyles.TEXT_PRIMARY};
            padding: 10px 20px;
            margin-right: 2px;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-bottom: none;
            border-radius: 4px 4px 0 0;
        }}
        
        QTabBar::tab:selected {{
            background-color: {AppStyles.CARD_COLOR};
            color: {AppStyles.PRIMARY_COLOR};
            font-weight: bold;
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-bottom: 2px solid {AppStyles.PRIMARY_COLOR};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: #EEEEEE;
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }}
        
        QPushButton:hover {{
            background-color: {AppStyles.PRIMARY_DARK};
        }}
        
        QPushButton:pressed {{
            background-color: #0D3D1F;
        }}
        
        QPushButton:disabled {{
            background-color: #CCCCCC;
            color: #999999;
        }}
        
        /* Secondary Button */
        QPushButton#secondaryBtn {{
            background-color: {AppStyles.SECONDARY_COLOR};
        }}
        
        QPushButton#secondaryBtn:hover {{
            background-color: {AppStyles.SECONDARY_DARK};
        }}
        
        /* Danger Button */
        QPushButton#dangerBtn {{
            background-color: {AppStyles.DANGER_COLOR};
        }}
        
        QPushButton#dangerBtn:hover {{
            background-color: #B71C1C;
        }}
        
        /* Input Fields */
        QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {{
            background-color: {AppStyles.CARD_COLOR};
            color: {AppStyles.TEXT_PRIMARY};
            border: 1px solid {AppStyles.BORDER_COLOR};
            padding: 8px;
            border-radius: 4px;
            font-size: 12px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, 
        QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus {{
            border: 2px solid {AppStyles.PRIMARY_COLOR};
            background-color: {AppStyles.CARD_COLOR};
        }}
        
        /* Tables */
        QTableWidget {{
            background-color: {AppStyles.CARD_COLOR};
            alternate-background-color: #F9F9F9;
            gridline-color: {AppStyles.BORDER_COLOR};
            border: 1px solid {AppStyles.BORDER_COLOR};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border: 1px solid {AppStyles.BORDER_COLOR};
        }}
        
        QTableWidget::item:selected {{
            background-color: {AppStyles.PRIMARY_LIGHT};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {AppStyles.PRIMARY_COLOR};
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            width: 12px;
            margin: 0px 0px 0px 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {AppStyles.TEXT_SECONDARY};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        
        /* Dialog */
        QDialog {{
            background-color: {AppStyles.BACKGROUND_COLOR};
        }}
        
        /* Message Box */
        QMessageBox {{
            background-color: {AppStyles.BACKGROUND_COLOR};
        }}
        
        QMessageBox QLabel {{
            color: {AppStyles.TEXT_PRIMARY};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {AppStyles.CARD_COLOR};
            color: {AppStyles.TEXT_PRIMARY};
            border-top: 1px solid {AppStyles.BORDER_COLOR};
        }}
        
        /* GroupBox */
        QGroupBox {{
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }}
        """
    
    @staticmethod
    def get_dialog_stylesheet():
        """Lấy stylesheet cho dialogs"""
        return f"""
        QDialog {{
            background-color: {AppStyles.BACKGROUND_COLOR};
        }}
        
        QDialog QLabel {{
            color: {AppStyles.TEXT_PRIMARY};
        }}
        
        QDialog QLineEdit, QDialog QTextEdit, QDialog QDateEdit, 
        QDialog QComboBox, QDialog QSpinBox {{
            background-color: {AppStyles.CARD_COLOR};
            color: {AppStyles.TEXT_PRIMARY};
            border: 1px solid {AppStyles.BORDER_COLOR};
            padding: 8px;
            border-radius: 4px;
            margin: 5px 0px;
        }}
        
        QDialog QPushButton {{
            min-width: 80px;
            min-height: 35px;
        }}
        """
    
    @staticmethod
    def get_font(size=12, bold=False):
        """Lấy font với kích thước và style"""
        font = QFont(AppStyles.FONT_FAMILY)
        font.setPointSize(size)
        if bold:
            font.setBold(True)
        return font
    
    @staticmethod
    def get_title_font():
        """Lấy font cho tiêu đề"""
        return AppStyles.get_font(size=16, bold=True)
    
    @staticmethod
    def get_header_font():
        """Lấy font cho header"""
        return AppStyles.get_font(size=14, bold=True)
    
    @staticmethod
    def get_button_style(button_type="primary"):
        """Lấy style cho button cụ thể"""
        styles = {
            "primary": f"QPushButton {{ background-color: {AppStyles.PRIMARY_COLOR}; }}",
            "secondary": f"QPushButton {{ background-color: {AppStyles.SECONDARY_COLOR}; }}",
            "danger": f"QPushButton {{ background-color: {AppStyles.DANGER_COLOR}; }}",
            "success": f"QPushButton {{ background-color: {AppStyles.SUCCESS_COLOR}; }}",
        }
        return styles.get(button_type, styles["primary"])


class ColorPalette:
    """Bảng màu cho ứng dụng"""
    
    @staticmethod
    def get_status_color(status):
        """Lấy màu dựa trên trạng thái"""
        status_lower = str(status).lower()
        
        if "healthy" in status_lower or "good" in status_lower or "yes" in status_lower:
            return QColor(AppStyles.SUCCESS_COLOR)
        elif "sick" in status_lower or "bad" in status_lower or "no" in status_lower:
            return QColor(AppStyles.DANGER_COLOR)
        elif "warning" in status_lower or "pending" in status_lower:
            return QColor(AppStyles.WARNING_COLOR)
        else:
            return QColor(AppStyles.INFO_COLOR)
    
    @staticmethod
    def get_breed_color(breed_status):
        """Lấy màu dựa trên trạng thái lai giống"""
        if "pregnant" in str(breed_status).lower():
            return QColor(AppStyles.PRIMARY_COLOR)
        elif "recovering" in str(breed_status).lower():
            return QColor(AppStyles.WARNING_COLOR)
        else:
            return QColor(AppStyles.INFO_COLOR)
