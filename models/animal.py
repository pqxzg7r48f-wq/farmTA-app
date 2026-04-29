"""
FarmTA - Animal model
"""

class Animal:
    """Model quản lý vật nuôi"""
    
    def __init__(self, name, species, breed=None, gender=None, 
                 date_of_birth=None, weight=None, health_status="Healthy", 
                 notes=None, id=None):
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.weight = weight
        self.health_status = health_status
        self.notes = notes
    
    def to_dict(self):
        """Chuyển đổi thành dictionary"""
        return {
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'weight': self.weight,
            'health_status': self.health_status,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f"Animal(id={self.id}, name={self.name}, species={self.species})"
