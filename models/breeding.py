"""
FarmTA - Breeding model
"""

class Breeding:
    """Model quản lý lai giống"""
    
    def __init__(self, male_id, female_id, breeding_date, 
                 expected_birth_date=None, number_of_offspring=None, 
                 notes=None, id=None):
        self.id = id
        self.male_id = male_id
        self.female_id = female_id
        self.breeding_date = breeding_date
        self.expected_birth_date = expected_birth_date
        self.number_of_offspring = number_of_offspring
        self.notes = notes
    
    def to_dict(self):
        """Chuyển đổi thành dictionary"""
        return {
            'male_id': self.male_id,
            'female_id': self.female_id,
            'breeding_date': self.breeding_date,
            'expected_birth_date': self.expected_birth_date,
            'number_of_offspring': self.number_of_offspring,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f"Breeding(id={self.id}, male={self.male_id}, female={self.female_id})"


class Pedigree:
    """Model quản lý huyết thống"""
    
    def __init__(self, animal_id, father_id=None, mother_id=None, 
                 generation=0, id=None):
        self.id = id
        self.animal_id = animal_id
        self.father_id = father_id
        self.mother_id = mother_id
        self.generation = generation
    
    def to_dict(self):
        """Chuyển đổi thành dictionary"""
        return {
            'animal_id': self.animal_id,
            'father_id': self.father_id,
            'mother_id': self.mother_id,
            'generation': self.generation
        }
    
    def __repr__(self):
        return f"Pedigree(animal={self.animal_id}, father={self.father_id}, mother={self.mother_id})"
