"""
FarmTA - Breeding Tab
Tab quản lý lai giống
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QDialog, QFormLayout, QDateEdit, QTextEdit, QMessageBox,
                             QComboBox, QSpinBox)
from PyQt5.QtCore import Qt, QDate

from config.database import create_connection, fetch_query, execute_query

class BreedingTab(QWidget):
    """Tab quản lý lai giống"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_breeding()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        
        # Thanh công cụ
        toolbar = QHBoxLayout()
        
        search_label = QLabel("Tìm kiếm:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên vật nuôi...")
        self.search_input.textChanged.connect(self.search_breeding)
        
        self.add_btn = QPushButton("➕ Ghi nhận lai giống")
        self.add_btn.clicked.connect(self.add_breeding)
        
        self.delete_btn = QPushButton("🗑️ Xóa")
        self.delete_btn.clicked.connect(self.delete_breeding)
        
        self.refresh_btn = QPushButton("🔄 Làm mới")
        self.refresh_btn.clicked.connect(self.load_breeding)
        
        toolbar.addWidget(search_label)
        toolbar.addWidget(self.search_input)
        toolbar.addStretch()
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.delete_btn)
        toolbar.addWidget(self.refresh_btn)
        
        layout.addLayout(toolbar)
        
        # Bảng hiển thị
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', 'Đực (ID)', 'Cái (ID)', 'Ngày lai', 'Dự kiến sinh', 'Số con', 'Ghi chú', 'Trạng thái'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_breeding(self):
        """Tải danh sách lai giống"""
        conn = create_connection()
        if conn:
            breeding = fetch_query(conn, """
                SELECT b.*, 
                       m.name as male_name, 
                       f.name as female_name
                FROM breeding_history b
                JOIN animals m ON b.male_id = m.id
                JOIN animals f ON b.female_id = f.id
                ORDER BY b.breeding_date DESC
            """)
            self.display_breeding(breeding)
            conn.close()
    
    def display_breeding(self, breeding_list):
        """Hiển thị lịch lai giống trên bảng"""
        self.table.setRowCount(0)
        if breeding_list:
            for row, breed in enumerate(breeding_list):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(breed['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(f"{breed['male_name']} ({breed['male_id']})"))
                self.table.setItem(row, 2, QTableWidgetItem(f"{breed['female_name']} ({breed['female_id']})"))
                self.table.setItem(row, 3, QTableWidgetItem(str(breed['breeding_date'])))
                self.table.setItem(row, 4, QTableWidgetItem(str(breed['expected_birth_date']) if breed['expected_birth_date'] else ''))
                self.table.setItem(row, 5, QTableWidgetItem(str(breed['number_of_offspring']) if breed['number_of_offspring'] else ''))
                self.table.setItem(row, 6, QTableWidgetItem(breed['notes'] or ''))
                
                # Trạng thái
                if breed['expected_birth_date']:
                    from datetime import datetime
                    expected = datetime.strptime(str(breed['expected_birth_date']), '%Y-%m-%d').date()
                    if expected <= datetime.now().date():
                        self.table.setItem(row, 7, QTableWidgetItem("🤰 Sắp sinh"))
                    else:
                        self.table.setItem(row, 7, QTableWidgetItem("⏳ Đang mang"))
    
    def add_breeding(self):
        """Ghi nhận lai giống mới"""
        dialog = BreedingDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            breed_data = dialog.get_data()
            conn = create_connection()
            if conn:
                query = """
                    INSERT INTO breeding_history (male_id, female_id, breeding_date, 
                    expected_birth_date, number_of_offspring, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (
                    breed_data['male_id'],
                    breed_data['female_id'],
                    breed_data['breeding_date'],
                    breed_data['expected_birth_date'],
                    breed_data['number_of_offspring'],
                    breed_data['notes']
                )
                execute_query(conn, query, params)
                
                # Cập nhật pedigree nếu cần
                self.update_pedigree(conn, breed_data)
                
                conn.close()
                self.load_breeding()
                QMessageBox.information(self, "Thành công", "Ghi nhận lai giống thành công!")
    
    def update_pedigree(self, conn, breed_data):
        """Cập nhật bảng pedigree"""
        # Lấy generation của cha mẹ
        parents = fetch_query(conn, """
            SELECT MAX(generation) as max_gen FROM pedigree 
            WHERE animal_id IN (%s, %s)
        """, (breed_data['male_id'], breed_data['female_id']))
        
        gen = (parents[0]['max_gen'] or 0) + 1 if parents else 1
        
        # Tạo pedigree cho con (nếu có)
        if breed_data['number_of_offspring']:
            for i in range(breed_data['number_of_offspring']):
                # Bạn có thể tạo con mới ở đây nếu muốn
                pass
    
    def delete_breeding(self):
        """Xóa lịch lai giống"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn lịch lai giống!")
            return
        
        breed_id = int(self.table.item(current_row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Bạn chắc chắn muốn xóa?")
        if reply == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                execute_query(conn, "DELETE FROM breeding_history WHERE id = %s", (breed_id,))
                conn.close()
                self.load_breeding()
                QMessageBox.information(self, "Thành công", "Xóa thành công!")
    
    def search_breeding(self):
        """Tìm kiếm lai giống"""
        search_text = self.search_input.text()
        if search_text:
            conn = create_connection()
            if conn:
                query = """
                    SELECT b.*, 
                           m.name as male_name, 
                           f.name as female_name
                    FROM breeding_history b
                    JOIN animals m ON b.male_id = m.id
                    JOIN animals f ON b.female_id = f.id
                    WHERE m.name LIKE %s OR f.name LIKE %s
                """
                breeding = fetch_query(conn, query, (f"%{search_text}%", f"%{search_text}%"))
                self.display_breeding(breeding)
                conn.close()
        else:
            self.load_breeding()


class BreedingDialog(QDialog):
    """Dialog ghi nhận lai giống"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ghi nhận lai giống")
        self.setGeometry(200, 200, 450, 380)
        self.init_ui()
        self.load_animals()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        form_layout = QFormLayout()
        
        self.male_combo = QComboBox()
        self.female_combo = QComboBox()
        
        self.breed_date = QDateEdit()
        self.breed_date.setDate(QDate.currentDate())
        
        self.expected_birth = QDateEdit()
        self.expected_birth.setDate(QDate.currentDate().addMonths(3))
        
        self.offspring_spin = QSpinBox()
        self.offspring_spin.setMaximum(100)
        self.offspring_spin.setValue(1)
        
        self.notes_input = QTextEdit()
        
        form_layout.addRow("Vật nuôi đực:", self.male_combo)
        form_layout.addRow("Vật nuôi cái:", self.female_combo)
        form_layout.addRow("Ngày lai:", self.breed_date)
        form_layout.addRow("Dự kiến sinh:", self.expected_birth)
        form_layout.addRow("Số lượng con:", self.offspring_spin)
        form_layout.addRow("Ghi chú:", self.notes_input)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Lưu")
        cancel_btn = QPushButton("Hủy")
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def load_animals(self):
        """Tải danh sách vật nuôi"""
        conn = create_connection()
        if conn:
            animals = fetch_query(conn, "SELECT id, name FROM animals ORDER BY name")
            if animals:
                for animal in animals:
                    self.male_combo.addItem(f"{animal['name']} (ID: {animal['id']})", animal['id'])
                    self.female_combo.addItem(f"{animal['name']} (ID: {animal['id']})", animal['id'])
            conn.close()
    
    def get_data(self):
        """Lấy dữ liệu từ form"""
        return {
            'male_id': self.male_combo.currentData(),
            'female_id': self.female_combo.currentData(),
            'breeding_date': self.breed_date.date().toString('yyyy-MM-dd'),
            'expected_birth_date': self.expected_birth.date().toString('yyyy-MM-dd'),
            'number_of_offspring': self.offspring_spin.value(),
            'notes': self.notes_input.toPlainText() or None
        }
