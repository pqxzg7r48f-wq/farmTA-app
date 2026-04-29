"""
FarmTA - Animals Tab
Tab quản lý vật nuôi
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QDialog, QFormLayout, QComboBox, QDateEdit, QSpinBox,
                             QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QDate

from config.database import create_connection, fetch_query, execute_query
from models.animal import Animal

class AnimalsTab(QWidget):
    """Tab quản lý vật nuôi"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_animals()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        
        # Thanh công cụ
        toolbar = QHBoxLayout()
        
        search_label = QLabel("Tìm kiếm:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên hoặc loài...")
        self.search_input.textChanged.connect(self.search_animals)
        
        self.add_btn = QPushButton("➕ Thêm vật nuôi")
        self.add_btn.clicked.connect(self.add_animal)
        
        self.edit_btn = QPushButton("✏️ Sửa")
        self.edit_btn.clicked.connect(self.edit_animal)
        
        self.delete_btn = QPushButton("🗑️ Xóa")
        self.delete_btn.clicked.connect(self.delete_animal)
        
        toolbar.addWidget(search_label)
        toolbar.addWidget(self.search_input)
        toolbar.addStretch()
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.edit_btn)
        toolbar.addWidget(self.delete_btn)
        
        layout.addLayout(toolbar)
        
        # Bảng hiển thị
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', 'Tên', 'Loài', 'Giống', 'Giới tính', 'Ngày sinh', 'Cân nặng', 'Sức khỏe'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_animals(self):
        """Tải danh sách vật nuôi"""
        conn = create_connection()
        if conn:
            animals = fetch_query(conn, "SELECT * FROM animals ORDER BY id DESC")
            self.display_animals(animals)
            conn.close()
    
    def display_animals(self, animals):
        """Hiển thị vật nuôi trên bảng"""
        self.table.setRowCount(0)
        if animals:
            for row, animal in enumerate(animals):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(animal['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(animal['name']))
                self.table.setItem(row, 2, QTableWidgetItem(animal['species']))
                self.table.setItem(row, 3, QTableWidgetItem(animal['breed'] or ''))
                self.table.setItem(row, 4, QTableWidgetItem(animal['gender'] or ''))
                self.table.setItem(row, 5, QTableWidgetItem(str(animal['date_of_birth']) or ''))
                self.table.setItem(row, 6, QTableWidgetItem(str(animal['weight']) or ''))
                self.table.setItem(row, 7, QTableWidgetItem(animal['health_status']))
    
    def add_animal(self):
        """Thêm vật nuôi mới"""
        dialog = AnimalDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            animal_data = dialog.get_data()
            conn = create_connection()
            if conn:
                query = """
                    INSERT INTO animals (name, species, breed, gender, date_of_birth, weight, health_status, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    animal_data['name'],
                    animal_data['species'],
                    animal_data['breed'],
                    animal_data['gender'],
                    animal_data['date_of_birth'],
                    animal_data['weight'],
                    animal_data['health_status'],
                    animal_data['notes']
                )
                execute_query(conn, query, params)
                conn.close()
                self.load_animals()
                QMessageBox.information(self, "Thành công", "Thêm vật nuôi thành công!")
    
    def edit_animal(self):
        """Sửa thông tin vật nuôi"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn vật nuôi!")
            return
        
        animal_id = int(self.table.item(current_row, 0).text())
        QMessageBox.information(self, "Thông tin", "Tính năng sửa đang phát triển!")
    
    def delete_animal(self):
        """Xóa vật nuôi"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn vật nuôi!")
            return
        
        animal_id = int(self.table.item(current_row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Bạn chắc chắn muốn xóa?")
        if reply == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                execute_query(conn, "DELETE FROM animals WHERE id = %s", (animal_id,))
                conn.close()
                self.load_animals()
                QMessageBox.information(self, "Thành công", "Xóa thành công!")
    
    def search_animals(self):
        """Tìm kiếm vật nuôi"""
        search_text = self.search_input.text()
        if search_text:
            conn = create_connection()
            if conn:
                query = "SELECT * FROM animals WHERE name LIKE %s OR species LIKE %s"
                animals = fetch_query(conn, query, (f"%{search_text}%", f"%{search_text}%"))
                self.display_animals(animals)
                conn.close()
        else:
            self.load_animals()


class AnimalDialog(QDialog):
    """Dialog thêm/sửa vật nuôi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm vật nuôi mới")
        self.setGeometry(200, 200, 400, 400)
        self.init_ui()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.species_input = QLineEdit()
        self.breed_input = QLineEdit()
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(['Male', 'Female', 'Other'])
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        
        self.weight_input = QSpinBox()
        self.weight_input.setMaximum(1000)
        
        self.health_combo = QComboBox()
        self.health_combo.addItems(['Healthy', 'Sick', 'Recovering', 'Quarantine'])
        
        self.notes_input = QTextEdit()
        
        form_layout.addRow("Tên:", self.name_input)
        form_layout.addRow("Loài:", self.species_input)
        form_layout.addRow("Giống:", self.breed_input)
        form_layout.addRow("Giới tính:", self.gender_combo)
        form_layout.addRow("Ngày sinh:", self.date_input)
        form_layout.addRow("Cân nặng (kg):", self.weight_input)
        form_layout.addRow("Sức khỏe:", self.health_combo)
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
    
    def get_data(self):
        """Lấy dữ liệu từ form"""
        return {
            'name': self.name_input.text(),
            'species': self.species_input.text(),
            'breed': self.breed_input.text() or None,
            'gender': self.gender_combo.currentText(),
            'date_of_birth': self.date_input.date().toString('yyyy-MM-dd'),
            'weight': self.weight_input.value() or None,
            'health_status': self.health_combo.currentText(),
            'notes': self.notes_input.toPlainText() or None
        }
