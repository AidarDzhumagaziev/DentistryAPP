-- Тестовые данные для локальной разработки.
--
-- Запуск (из корня проекта, когда работает docker compose):
--   docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < backend/seed.sql
--
-- Скрипт можно запускать повторно: уже существующие записи не дублируются.
--
-- Тестовые пользователи (вход по email), пароль у всех: test-c9585b8d
--   admin@dentatime.ru  администратор
--   doctor1@dentatime.ru .. doctor4@dentatime.ru  врачи

BEGIN;

INSERT INTO roles (name)
SELECT r.name
FROM (VALUES ('patient'), ('doctor'), ('admin')) AS r(name)
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE roles.name = r.name);

INSERT INTO specializations (name)
SELECT s.name
FROM (VALUES ('Терапевт'), ('Гигиенист'), ('Хирург')) AS s(name)
WHERE NOT EXISTS (SELECT 1 FROM specializations WHERE specializations.name = s.name);

INSERT INTO services (name, specialization_id, description, price_from, duration_min, buffer_min, requires_consultation, cabinet_type)
SELECT v.name, sp.id, v.description, v.price_from, v.duration_min, v.buffer_min, v.requires_consultation, v.cabinet_type
FROM (VALUES
    ('Острая боль', 'Терапевт', 'Экстренный приём в день обращения.', 2000, 30, 10, false, 'general'),
    ('Осмотр и консультация', 'Терапевт', 'Осмотр, план лечения и расчёт стоимости.', 1000, 30, 10, false, 'general'),
    ('Лечение кариеса', 'Терапевт', 'Лечение и пломба, с анестезией.', 3500, 60, 15, false, 'general'),
    ('Профессиональная гигиена', 'Гигиенист', 'Чистка ультразвуком и Air Flow, полировка.', 4000, 60, 10, false, 'general'),
    ('Удаление зуба мудрости', 'Хирург', 'Проводится в хирургическом кабинете.', 5000, 60, 15, true, 'surgical'),
    ('Имплантация', 'Хирург', 'Установка импланта в хирургическом кабинете.', 30000, 90, 15, true, 'surgical')
) AS v(name, specialization, description, price_from, duration_min, buffer_min, requires_consultation, cabinet_type)
JOIN specializations sp ON sp.name = v.specialization
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (phone, email, password_hash, role_id, full_name)
SELECT u.phone, u.email, convert_to('$2b$12$vY4Ep3fADTOLvMU.8qFuhexKqhHf4IhRph.4Il.6qbemm1u5zGoMK', 'UTF8'), r.id, u.full_name
FROM (VALUES
    ('+79000000000', 'admin@dentatime.ru', 'admin', 'Администратор'),
    ('+79000000001', 'doctor1@dentatime.ru', 'doctor', 'Анна Иванова'),
    ('+79000000002', 'doctor2@dentatime.ru', 'doctor', 'Павел Смирнов'),
    ('+79000000003', 'doctor3@dentatime.ru', 'doctor', 'Мария Орлова'),
    ('+79000000004', 'doctor4@dentatime.ru', 'doctor', 'Дмитрий Лебедев')
) AS u(phone, email, role, full_name)
JOIN roles r ON r.name = u.role
ON CONFLICT (phone) DO UPDATE SET email = EXCLUDED.email;

INSERT INTO doctors (user_id, experience_years, bio, photo_url)
SELECT u.id, d.experience_years, d.bio, ''
FROM (VALUES
    ('+79000000001', 8, 'Лечит кариес и пульпит.'),
    ('+79000000002', 12, 'Удаляет сложные зубы и ставит импланты.'),
    ('+79000000003', 5, 'Проводит профессиональную чистку.'),
    ('+79000000004', 3, 'Лечит зубы у взрослых.')
) AS d(phone, experience_years, bio)
JOIN users u ON u.phone = d.phone
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO doctor_specializations (doctor_id, specialization_id)
SELECT u.id, sp.id
FROM (VALUES
    ('+79000000001', 'Терапевт'),
    ('+79000000002', 'Хирург'),
    ('+79000000003', 'Гигиенист'),
    ('+79000000004', 'Терапевт')
) AS ds(phone, specialization)
JOIN users u ON u.phone = ds.phone
JOIN specializations sp ON sp.name = ds.specialization
ON CONFLICT DO NOTHING;

INSERT INTO cabinets (number, type)
SELECT c.number, c.type
FROM (VALUES (101, 'general'), (102, 'general'), (103, 'general'), (201, 'surgical')) AS c(number, type)
WHERE NOT EXISTS (SELECT 1 FROM cabinets WHERE cabinets.number = c.number);

-- Врачи работают с понедельника по пятницу (weekday 1..5), каждый в своём кабинете.
INSERT INTO work_schedules (doctor_id, cabinet_id, weekday, start_time, end_time)
SELECT u.id, c.id, wd.weekday, ws.start_time::time, ws.end_time::time
FROM (VALUES
    ('+79000000001', 101, '09:00', '15:00'),
    ('+79000000002', 201, '10:00', '18:00'),
    ('+79000000003', 103, '09:00', '15:00'),
    ('+79000000004', 102, '14:00', '20:00')
) AS ws(phone, cabinet_number, start_time, end_time)
CROSS JOIN generate_series(1, 5) AS wd(weekday)
JOIN users u ON u.phone = ws.phone
JOIN cabinets c ON c.number = ws.cabinet_number
WHERE NOT EXISTS (
    SELECT 1 FROM work_schedules w WHERE w.doctor_id = u.id AND w.weekday = wd.weekday
);

COMMIT;
