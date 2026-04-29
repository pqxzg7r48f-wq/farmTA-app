"""
FarmTA - Vaccination model
"""

from datetime import datetime, timedelta

class Vaccination:
    """Model quản lý tiêm chủng"""
    
    def __init__(self, animal_id, vaccine_name, vaccination_date, 
                 next_vaccination_date=None, veterinarian=None, 
                 notes=None, id=None):
        self.id = id
        self.animal_id = animal_id
        self.vaccine_name = vaccine_name
        self.vaccination_date = vaccination_date
        self.next_vaccination_date = next_vaccination_date
        self.veterinarian = veterinarian
        self.notes = notes
    
    def to_dict(self):
        """Chuyển đổi thành dictionary"""
        return {
            'animal_id': self.animal_id,
            'vaccine_name': self.vaccine_name,
            'vaccination_date': self.vaccination_date,
            'next_vaccination_date': self.next_vaccination_date,
            'veterinarian': self.veterinarian,
            'notes': self.notes
        }
    
    def is_due_for_next_vaccination(self):
        """Kiểm tra xem có cần tiêm lần tiếp theo không"""
        if self.next_vaccination_date:
            return datetime.strptime(str(self.next_vaccination_date), '%Y-%m-%d').date() <= datetime.now().date()
        return False
    
    def __repr__(self):
        return f"Vaccination(id={self.id}, vaccine={self.vaccine_name}, date={self.vaccination_date})"
