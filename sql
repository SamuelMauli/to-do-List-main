CREATE DATABASE task_manager;
USE task_manager;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    deadline DATE,
    status ENUM('Em Aberto', 'Em Andamento', 'Concluída') DEFAULT 'Em Aberto',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE tasks ADD COLUMN assignee_id INT, ADD FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL;

INSERT INTO users (username, password)
VALUES ('root', '$2b$12$seuHashAqui');

select * from users;

