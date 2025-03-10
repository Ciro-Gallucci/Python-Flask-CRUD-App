-- Crea la tabella students
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL
);

-- Concedi tutti i privilegi all'utente 'user'
GRANT ALL PRIVILEGES ON students_db.* TO 'user'@'%';
FLUSH PRIVILEGES;
