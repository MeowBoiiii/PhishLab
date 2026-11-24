-- 1. Administratorzy (konta osób zarządzających kampaniami w Dashboardzie)
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,                          -- Unikalny identyfikator administratora
    username VARCHAR(50) UNIQUE NOT NULL,           -- Unikalna nazwa użytkownika
    email VARCHAR(100) UNIQUE NOT NULL,             -- Unikalny adres email (używany do logowania)
    password_hash VARCHAR(255) NOT NULL,            -- Zahashowane hasło (bcrypt, nigdy otwarty tekst)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data utworzenia konta
);

-- 2. Użytkownicy / Odbiorcy kampanii (zanonimizowani - brak danych osobowych RODO)
CREATE TABLE target_users (
    id SERIAL PRIMARY KEY,                          -- Unikalny identyfikator rekordu
    user_hash VARCHAR(64) UNIQUE NOT NULL,          -- Zanonimizowany hash zamiast imienia/maila
    department VARCHAR(100) NOT NULL,               -- Dział firmy (np. "HR", "IT", "Finanse")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data dodania odbiorcy
);

-- 3. Szablony wiadomości phishingowych i powiązane z nimi strony edukacyjne
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,                          -- Unikalny identyfikator szablonu
    name VARCHAR(100) NOT NULL,                     -- Nazwa szablonu widoczna w panelu (np. "Fałszywa faktura")
    email_subject VARCHAR(200) NOT NULL,            -- Temat wysyłanej wiadomości email
    email_body TEXT NOT NULL,                       -- Treść wiadomości (HTML lub tekst)
    edu_page_content TEXT NOT NULL                  -- Treść strony edukacyjnej po kliknięciu w link
);

-- 4. Kampanie phishingowe tworzone przez administratorów
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,                          -- Unikalny identyfikator kampanii
    name VARCHAR(100) NOT NULL,                     -- Nazwa kampanii
    admin_id INTEGER REFERENCES admins(id) ON DELETE SET NULL, -- Twórca kampanii (po usunięciu admina pole staje się NULL)
    template_id INTEGER NOT NULL REFERENCES templates(id) ON DELETE CASCADE, -- Szablon użyty w kampanii
    target_department VARCHAR(100) NOT NULL,        -- Docelowy dział objęty kampanią
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT'     -- Status kampanii (domyślnie szkic)
        CHECK (status IN ('DRAFT', 'ACTIVE', 'FINISHED')), -- Dozwolone wyłącznie 3 wartości statusu
    scheduled_at TIMESTAMP,                         -- Planowana data wysyłki kampanii
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data utworzenia kampanii
);

-- 5. Tracking i wyniki (łączy odbiorcę z kampanią i zapisuje jego reakcje)
CREATE TABLE campaign_tracking (
    id SERIAL PRIMARY KEY,                          -- Unikalny identyfikator wpisu śledzenia
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE, -- Powiązana kampania
    user_id INTEGER NOT NULL REFERENCES target_users(id) ON DELETE CASCADE,  -- Powiązany odbiorca
    tracking_token VARCHAR(64) UNIQUE NOT NULL,     -- Unikalny token wstawiany do piksela i linku w mailu
    is_opened BOOLEAN NOT NULL DEFAULT FALSE,       -- Czy odbiorca otworzył wiadomość (piksel 1x1)
    is_clicked BOOLEAN NOT NULL DEFAULT FALSE,      -- Czy odbiorca kliknął w link phishingowy
    reaction_time_sec INTEGER,                      -- Czas reakcji w sekundach
    quiz_score INTEGER,                             -- Wynik z quizu edukacyjnego
    UNIQUE (campaign_id, user_id)                   -- Zabezpieczenie: ten sam użytkownik raz w danej kampanii
);

-- 6. Pytania do quizu weryfikującego wiedzę (powiązane z szablonem)
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,                          -- Unikalny identyfikator pytania
    template_id INTEGER NOT NULL REFERENCES templates(id) ON DELETE CASCADE, -- Szablon, którego dotyczy pytanie
    question VARCHAR(255) NOT NULL,                 -- Treść pytania
    option_a VARCHAR(150) NOT NULL,                 -- Odpowiedź A
    option_b VARCHAR(150) NOT NULL,                 -- Odpowiedź B
    option_c VARCHAR(150) NOT NULL,                 -- Odpowiedź C
    correct_answer CHAR(1) NOT NULL                 -- Poprawna odpowiedź
        CHECK (correct_answer IN ('A', 'B', 'C'))   -- Walidacja: dopuszczalne tylko A, B lub C
);

-- Indeksy przyspieszające częste zapytania (filtrowanie i złączenia JOIN)
CREATE INDEX idx_target_users_department ON target_users(department);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaign_tracking_campaign_id ON campaign_tracking(campaign_id);
CREATE INDEX idx_campaign_tracking_user_id ON campaign_tracking(user_id);

-- DANE POCZĄTKOWE DLA DEMO (SEED DATA)

-- 1. Gotowe szablony phishingowe
INSERT INTO templates (name, email_subject, email_body, edu_page_content) VALUES 
(
    'Nieopłacona faktura VAT (Pilne)', 
    'Ostateczne wezwanie do zapłaty: Faktura VAT 10/2026', 
    'Dzień dobry, w załączniku przesyłamy zaległą fakturę. Prosimy o pilną wpłatę, aby uniknąć blokady usług.', 
    'Zwróć uwagę na nagłość sytuacji i presję czasu! Oszuści podszywają się pod kontrahentów, wysyłając fałszywe wezwania do zapłaty.'
),
(
    'Wymagany reset hasła firmowego', 
    'Ważne: Twoje hasło wygasa w ciągu 2 godzin', 
    'Dział IT informuje: Twoje hasło domenowe wygasa dzisiaj. Kliknij poniższy link, aby zachować ciągłość dostępu.', 
    'Nigdy nie klikaj w bezpośrednie linki resetujące hasło przesyłane w wiadomościach e-mail bez potwierdzenia z działem IT!'
),
(
    'Niedoręczona paczka kurierska', 
    'Paczka nr PL892193 nie mogła zostać doręczona', 
    'Kurier nie zastał nikogo pod wskazanym adresem. Kliknij link, aby zmienić termin doręczenia lub podać poprawny adres.', 
    'Phishing kurierski bazuje na ciekawości. Zawsze sprawdzaj status przesyłki bezpośrednio na oficjalnej stronie firmy kurierskiej.'
);

-- 2. Pracownicy w działach (zanonimizowane identyfikatory SHA-256)
INSERT INTO target_users (user_hash, department) VALUES 
('usr_fin_a1b2c3d4e5f67890', 'Finanse'),
('usr_fin_b2c3d4e5f67890a1', 'Finanse'),
('usr_fin_c3d4e5f67890a1b2', 'Finanse'),
('usr_it_d4e5f67890a1b2c3', 'IT'),
('usr_it_e5f67890a1b2c3d4', 'IT'),
('usr_hr_f67890a1b2c3d4e5', 'HR'),
('usr_hr_0a1b2c3d4e5f6789', 'HR');

-- 3. Pytania quizowe do szablonu 1 (Faktura)
INSERT INTO quiz_questions (template_id, question, option_a, option_b, option_c, correct_answer) VALUES 
(
    1, 
    'Jaki element wiadomości powinien od razu wzbudzić Twoją czujność?', 
    'Dokładny adres siedziby nadawcy', 
    'Ogromna presja czasu i groźba blokady usług', 
    'Obecność stopki z numerem telefonu', 
    'B'
),
(
    1, 
    'Co należy zrobić przed opłaceniem nieznanej faktury z maila?', 
    'Natychmiast kliknąć link i zapłacić BLIKiem', 
    'Przesłać maila do wszystkich znajomych', 
    'Zweryfikować wydatek telefonicznie ze swoim przełożonym lub działem księgowości', 
    'C'
);
