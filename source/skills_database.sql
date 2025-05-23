CREATE TABLE semestres (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE blocs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    semestre_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (semestre_id) REFERENCES semestres(id) ON DELETE CASCADE
);

CREATE TABLE competences (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    nom VARCHAR(255) NOT NULL,
    bloc_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (bloc_id) REFERENCES blocs(id) ON DELETE CASCADE
);

CREATE TABLE niveaux (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    niveau VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE competences_niveaux (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    competence_id INT UNSIGNED NOT NULL,
    niveau_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (competence_id) REFERENCES competences(id) ON DELETE CASCADE,
    FOREIGN KEY (niveau_id) REFERENCES niveaux(id)
);

-- Insertion des niveaux
INSERT INTO niveaux (niveau) VALUES
('Non acquis'),
('Acquisition en cours'),
('Presque acquis'),
('Acquis'),
('Expert');
