"""
FarmTA - Main window
Cửa sổ chính của ứng dụng
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from ui.animals_tab import AnimalsTab
from ui.vaccination_tab import VaccinationTab
from ui.breeding_tab import BreedingTab
from ui.pedigree_tab import PedigreeTab

class MainWindow(QMainWindow):
    """Cửa sổ chính ứng dụng"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FarmTA - Quản lý Trang trại & Lai giống")
        self.setGeometry(100, 100, 1200, 700)
        
        # Tạo widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("FarmTA - Ứng dụng Quản lý Trang trại & Lai giống Vật nuôi")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Tạo các tab
        self.animals_tab = AnimalsTab()
        self.vaccination_tab = VaccinationTab()
        self.breeding_tab = BreedingTab()
        self.pedigree_tab = PedigreeTab()
        
        # Thêm tab vào widget
        self.tabs.addTab(self.animals_tab, "🐄 Quản lý Vật nuôi")
        self.tabs.addTab(self.vaccination_tab, "💉 Tiêm chủng")
        self.tabs.addTab(self.breeding_tab, "👶 Lai giống")
        self.tabs.addTab(self.pedigree_tab, "🌳 Huyết thống")
        
        main_layout.addWidget(self.tabs)
        
        # Footer
        footer_layout = QHBoxLayout()
        status_label = QLabel("Ready")
        footer_layout.addWidget(status_label)
        footer_layout.addStretch()
        version_label = QLabel("v1.0.0")
        footer_layout.addWidget(version_label)
        
        main_layout.addLayout(footer_layout)
        
        # Thiết lập style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

def main():
    app = __import__('PyQt5.QtWidgets', fromlist=['QApplication']).QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
