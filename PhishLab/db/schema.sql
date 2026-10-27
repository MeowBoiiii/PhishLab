-- Wstępny schemat bazy danych

-- 1. Administratorzy (logowanie do Dashboardu)
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Użytkownicy / Odbiorcy kampanii (zanonimizowani - brak danych osobowych)
CREATE TABLE target_users (
    id SERIAL PRIMARY KEY,
    user_hash VARCHAR(64) UNIQUE NOT NULL, -- Hash zamiast imienia/maila
    department VARCHAR(100) NOT NULL,      -- Grupa docelowa (np. "HR", "IT", "Finanse")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Szablony wiadomości i strony edukacyjne
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,            -- Nazwa szablonu (np. "Fałszywa faktura")
    email_subject VARCHAR(200) NOT NULL,   -- Temat maila phishingowego
    email_body TEXT NOT NULL,              -- Treść maila
    edu_page_content TEXT NOT NULL         -- Tekst edukacyjny wyświetlany po kliknięciu w link
);

-- 4. Kampanie phishingowe
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    admin_id INTEGER REFERENCES admins(id) ON DELETE SET NULL,
    template_id INTEGER REFERENCES templates(id) ON DELETE CASCADE,
    target_department VARCHAR(100) NOT NULL, -- Grupa docelowa kampanii
    status VARCHAR(20) DEFAULT 'DRAFT',      -- DRAFT, ACTIVE, FINISHED
    scheduled_at TIMESTAMP,                  -- Harmonogram wysyłki
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tracking i wyniki (łączy użytkownika z kampanią i zapisuje jego reakcje)
CREATE TABLE campaign_tracking (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES target_users(id) ON DELETE CASCADE,
    tracking_token VARCHAR(64) UNIQUE NOT NULL, -- Unikalny kod w linku phishingowym
    is_opened BOOLEAN DEFAULT FALSE,            -- Czy otwarto wiadomość?
    is_clicked BOOLEAN DEFAULT FALSE,           -- Czy kliknięto link?
    reaction_time_sec INTEGER,                  -- Czas reakcji w sekundach
    quiz_score INTEGER                          -- Wynik z quizu (np. liczba punktów)
);

-- 6. Pytania do quizu (powiązane z szablonem edukacyjnym)
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES templates(id) ON DELETE CASCADE,
    question VARCHAR(255) NOT NULL,
    option_a VARCHAR(150) NOT NULL,
    option_b VARCHAR(150) NOT NULL,
    option_c VARCHAR(150) NOT NULL,
    correct_answer CHAR(1) NOT NULL             -- 'A', 'B' lub 'C'
);