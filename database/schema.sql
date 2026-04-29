"""
FarmTA - Ứng dụng quản lý trang trại và lai giống vật nuôi
Database schema
"""

CREATE_DATABASE = """
CREATE DATABASE IF NOT EXISTS farmta_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

USE_DATABASE = "USE farmta_db;"

CREATE_TABLES = """
-- Bảng vật nuôi
CREATE TABLE IF NOT EXISTS animals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(100),
    gender ENUM('Male', 'Female', 'Other'),
    date_of_birth DATE,
    weight FLOAT,
    health_status VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng lịch tiêm chủng
CREATE TABLE IF NOT EXISTS vaccinations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    vaccine_name VARCHAR(100) NOT NULL,
    vaccination_date DATE NOT NULL,
    next_vaccination_date DATE,
    veterinarian VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE
);

-- Bảng lịch sử lai giống
CREATE TABLE IF NOT EXISTS breeding_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    male_id INT NOT NULL,
    female_id INT NOT NULL,
    breeding_date DATE NOT NULL,
    expected_birth_date DATE,
    number_of_offspring INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (male_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (female_id) REFERENCES animals(id) ON DELETE CASCADE
);

-- Bảng quan hệ huyết thống (pedigree)
CREATE TABLE IF NOT EXISTS pedigree (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    father_id INT,
    mother_id INT,
    generation INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (father_id) REFERENCES animals(id) ON DELETE SET NULL,
    FOREIGN KEY (mother_id) REFERENCES animals(id) ON DELETE SET NULL
);

-- Bảng sức khỏe
CREATE TABLE IF NOT EXISTS health_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    record_date DATE NOT NULL,
    disease_name VARCHAR(100),
    treatment VARCHAR(200),
    recovery_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE
);

-- Bảng lịch ăn
CREATE TABLE IF NOT EXISTS feed_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    feed_type VARCHAR(100),
    quantity FLOAT,
    feed_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE
);

-- Tạo chỉ mục
CREATE INDEX idx_animal_species ON animals(species);
CREATE INDEX idx_vaccination_animal ON vaccinations(animal_id);
CREATE INDEX idx_breeding_date ON breeding_history(breeding_date);
CREATE INDEX idx_pedigree_animal ON pedigree(animal_id);
CREATE INDEX idx_health_animal ON health_records(animal_id);
CREATE INDEX idx_feed_animal ON feed_logs(animal_id);
"""
