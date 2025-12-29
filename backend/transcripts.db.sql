
-- Crear tabla de transcripciones
DROP TABLE IF EXISTS transcriptions;
CREATE TABLE transcriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin TEXT,
    speaker INTEGER,
    start INTEGER,
    duration INTEGER,
    transcript TEXT,
    audio_url TEXT
);

-- Insertar datos de prueba en transcriptions
INSERT INTO transcriptions (pin, speaker, start, duration, transcript, audio_url)
VALUES 
('1234', 1, 0, 20, 'ya conseguí la papa', '/audios/p1.wav'),
('1234', 2, 20, 15, 'tenemos luz verde', '/audios/p2.wav'),
('1234', 1, 35, 25, 'lo van a levantar', '/audios/p3.wav');

-- Crear tabla de llamadas
DROP TABLE IF EXISTS calls;
CREATE TABLE calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_emitter TEXT,
    phone_number TEXT,
    date TEXT,
    duration INTEGER
);

-- Insertar datos de prueba en calls
INSERT INTO calls (pin_emitter, phone_number, date, duration)
VALUES
('1234', '5551001000', '2025-04-01', 120),
('1234', '5552002000', '2025-04-01', 90),
('1234', '5553003000', '2025-04-02', 200),
('5678', '5551001000', '2025-04-03', 180);
