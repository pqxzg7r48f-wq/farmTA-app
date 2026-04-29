"""
FarmTA - Vaccination Tab
Tab quản lý tiêm chủng
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QDialog, QFormLayout, QDateEdit, QTextEdit, QMessageBox,
                             QComboBox)
from PyQt5.QtCore import Qt, QDate

from config.database import create_connection, fetch_query, execute_query

class VaccinationTab(QWidget):
    """Tab quản lý tiêm chủng"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_vaccinations()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        
        # Thanh công cụ
        toolbar = QHBoxLayout()
        
        search_label = QLabel("Tìm kiếm:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên vắc-xin hoặc ID vật nuôi...")
        self.search_input.textChanged.connect(self.search_vaccinations)
        
        self.add_btn = QPushButton("➕ Thêm lịch tiêm")
        self.add_btn.clicked.connect(self.add_vaccination)
        
        self.delete_btn = QPushButton("🗑️ Xóa")
        self.delete_btn.clicked.connect(self.delete_vaccination)
        
        self.refresh_btn = QPushButton("🔄 Làm mới")
        self.refresh_btn.clicked.connect(self.load_vaccinations)
        
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
        self.table.setHorizontalHeaderLabels(['ID', 'ID Vật nuôi', 'Vắc-xin', 'Ngày tiêm', 'Ngày tiêm tiếp', 'Bác sĩ', 'Ghi chú', 'Cần tiêm'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_vaccinations(self):
        """Tải danh sách tiêm chủng"""
        conn = create_connection()
        if conn:
            vaccinations = fetch_query(conn, """
                SELECT v.*, a.name as animal_name 
                FROM vaccinations v
                JOIN animals a ON v.animal_id = a.id
                ORDER BY v.vaccination_date DESC
            """)
            self.display_vaccinations(vaccinations)
            conn.close()
    
    def display_vaccinations(self, vaccinations):
        """Hiển thị lịch tiêm chủng trên bảng"""
        self.table.setRowCount(0)
        if vaccinations:
            for row, vac in enumerate(vaccinations):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(vac['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(vac['animal_id'])))
                self.table.setItem(row, 2, QTableWidgetItem(vac['vaccine_name']))
                self.table.setItem(row, 3, QTableWidgetItem(str(vac['vaccination_date'])))
                self.table.setItem(row, 4, QTableWidgetItem(str(vac['next_vaccination_date']) if vac['next_vaccination_date'] else ''))
                self.table.setItem(row, 5, QTableWidgetItem(vac['veterinarian'] or ''))
                self.table.setItem(row, 6, QTableWidgetItem(vac['notes'] or ''))
                
                # Kiểm tra cần tiêm không
                if vac['next_vaccination_date']:
                    from datetime import datetime
                    next_date = datetime.strptime(str(vac['next_vaccination_date']), '%Y-%m-%d').date()
                    if next_date <= datetime.now().date():
                        self.table.setItem(row, 7, QTableWidgetItem("⚠️ CẦN TIÊM"))
                    else:
                        self.table.setItem(row, 7, QTableWidgetItem("✓"))
    
    def add_vaccination(self):
        """Thêm lịch tiêm chủng mới"""
        dialog = VaccinationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            vac_data = dialog.get_data()
            conn = create_connection()
            if conn:
                query = """
                    INSERT INTO vaccinations (animal_id, vaccine_name, vaccination_date, 
                    next_vaccination_date, veterinarian, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (
                    vac_data['animal_id'],
                    vac_data['vaccine_name'],
                    vac_data['vaccination_date'],
                    vac_data['next_vaccination_date'],
                    vac_data['veterinarian'],
                    vac_data['notes']
                )
                execute_query(conn, query, params)
                conn.close()
                self.load_vaccinations()
                QMessageBox.information(self, "Thành công", "Thêm lịch tiêm thành công!")
    
    def delete_vaccination(self):
        """Xóa lịch tiêm"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn lịch tiêm!")
            return
        
        vac_id = int(self.table.item(current_row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Bạn chắc chắn muốn xóa?")
        if reply == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                execute_query(conn, "DELETE FROM vaccinations WHERE id = %s", (vac_id,))
                conn.close()
                self.load_vaccinations()
                QMessageBox.information(self, "Thành công", "Xóa thành công!")
    
    def search_vaccinations(self):
        """Tìm kiếm lịch tiêm"""
        search_text = self.search_input.text()
        if search_text:
            conn = create_connection()
            if conn:
                query = """
                    SELECT v.*, a.name as animal_name 
                    FROM vaccinations v
                    JOIN animals a ON v.animal_id = a.id
                    WHERE v.vaccine_name LIKE %s OR a.name LIKE %s
                """
                vaccinations = fetch_query(conn, query, (f"%{search_text}%", f"%{search_text}%"))
                self.display_vaccinations(vaccinations)
                conn.close()
        else:
            self.load_vaccinations()


class VaccinationDialog(QDialog):
    """Dialog thêm lịch tiêm chủng"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm lịch tiêm chủng")
        self.setGeometry(200, 200, 400, 350)
        self.init_ui()
        self.load_animals()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        form_layout = QFormLayout()
        
        self.animal_combo = QComboBox()
        self.vaccine_input = QLineEdit()
        self.vaccine_input.setPlaceholderText("VD: Vắc-xin A, Vắc-xin B...")
        
        self.vac_date = QDateEdit()
        self.vac_date.setDate(QDate.currentDate())
        
        self.next_vac_date = QDateEdit()
        self.next_vac_date.setDate(QDate.currentDate().addMonths(1))
        
        self.veterinarian_input = QLineEdit()
        self.veterinarian_input.setPlaceholderText("Tên bác sĩ thú y...")
        
        self.notes_input = QTextEdit()
        
        form_layout.addRow("Vật nuôi:", self.animal_combo)
        form_layout.addRow("Tên vắc-xin:", self.vaccine_input)
        form_layout.addRow("Ngày tiêm:", self.vac_date)
        form_layout.addRow("Ngày tiêm tiếp:", self.next_vac_date)
        form_layout.addRow("Bác sĩ:", self.veterinarian_input)
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
                    self.animal_combo.addItem(f"{animal['name']} (ID: {animal['id']})", animal['id'])
            conn.close()
    
    def get_data(self):
        """Lấy dữ liệu từ form"""
        return {
            'animal_id': self.animal_combo.currentData(),
            'vaccine_name': self.vaccine_input.text(),
            'vaccination_date': self.vac_date.date().toString('yyyy-MM-dd'),
            'next_vaccination_date': self.next_vac_date.date().toString('yyyy-MM-dd'),
            'veterinarian': self.veterinarian_input.text() or None,
            'notes': self.notes_input.toPlainText() or None
        }
