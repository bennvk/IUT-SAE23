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

-- Pour semestre 1
INSERT INTO blocs (code, nom, semestre_id) VALUES
('B1S1', 'Bloc 1 du semestre 1', 1),
('B2S1', 'Bloc 2 du semestre 1', 1),
('B3S1', 'Bloc 3 du semestre 1', 1);

-- Pour semestre 2
INSERT INTO blocs (code, nom, semestre_id) VALUES
('B1S2', 'Bloc 1 du semestre 2', 2),
('B2S2', 'Bloc 2 du semestre 2', 2),
('B3S2', 'Bloc 3 du semestre 2', 2);

-- Pour semestre 3
INSERT INTO blocs (code, nom, semestre_id) VALUES
('B1S3', 'Bloc 1 du semestre 3', 3),
('B2S3', 'Bloc 2 du semestre 3', 3),
('B3S3', 'Bloc 3 du semestre 3', 3);
