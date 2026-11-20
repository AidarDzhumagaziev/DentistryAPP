-- Тестовые данные для локальной разработки.
--
-- Загружается сам: при старте бэкенда seed.py запускает этот файл, если база пустая.
-- Вручную (из корня проекта, когда работает docker compose):
--   docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < backend/seed.sql
--
-- Скрипт можно запускать повторно: уже существующие записи не дублируются.
--
-- Тестовые пользователи (вход по email), пароль у всех: test-c9585b8d
--   admin@dentatime.ru  администратор
--   doctor1@dentatime.ru .. doctor4@dentatime.ru  врачи
--   patient1@dentatime.ru, patient2@dentatime.ru  пациенты (см. ниже)

BEGIN;

INSERT INTO roles (name)
SELECT r.name
FROM (VALUES ('patient'), ('doctor'), ('admin')) AS r(name)
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE roles.name = r.name);

INSERT INTO specializations (name)
SELECT s.name
FROM (VALUES ('Терапевт'), ('Гигиенист'), ('Хирург')) AS s(name)
WHERE NOT EXISTS (SELECT 1 FROM specializations WHERE specializations.name = s.name);

-- is_consultation: консультация своей специализации. Услуги с requires_consultation
-- сервер разрешает только после консультации той же специализации.
INSERT INTO services (name, specialization_id, description, price_from, duration_min, buffer_min, requires_consultation, is_consultation, cabinet_type)
SELECT v.name, sp.id, v.description, v.price_from, v.duration_min, v.buffer_min, v.requires_consultation, v.is_consultation, v.cabinet_type
FROM (VALUES
    ('Острая боль', 'Терапевт', 'Экстренный приём в день обращения.', 2000, 30, 10, false, false, 'general'),
    ('Осмотр и консультация', 'Терапевт', 'Осмотр, план лечения и расчёт стоимости.', 1000, 30, 10, false, true, 'general'),
    ('Лечение кариеса', 'Терапевт', 'Лечение и пломба, с анестезией.', 3500, 60, 15, false, false, 'general'),
    ('Лечение каналов', 'Терапевт', 'Лечение пульпита и периодонтита под микроскопом.', 7000, 90, 15, true, false, 'general'),
    ('Художественная реставрация', 'Терапевт', 'Восстановление формы и цвета зуба композитом.', 6000, 60, 15, true, false, 'general'),
    ('Профессиональная гигиена', 'Гигиенист', 'Чистка ультразвуком и Air Flow, полировка.', 4000, 60, 10, false, false, 'general'),
    ('Консультация хирурга', 'Хирург', 'Осмотр, снимок и план операции.', 1500, 30, 10, false, true, 'surgical'),
    ('Удаление зуба мудрости', 'Хирург', 'Проводится в хирургическом кабинете.', 5000, 60, 15, true, false, 'surgical'),
    ('Имплантация', 'Хирург', 'Установка импланта в хирургическом кабинете.', 30000, 90, 15, true, false, 'surgical')
) AS v(name, specialization, description, price_from, duration_min, buffer_min, requires_consultation, is_consultation, cabinet_type)
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
SELECT u.id, d.experience_years, d.bio, d.photo_url
FROM (VALUES
    ('+79000000001', 8, 'Лечит кариес и пульпит.', '/images/doctors/anna.png'),
    ('+79000000002', 12, 'Удаляет сложные зубы и ставит импланты.', '/images/doctors/pavel.png'),
    ('+79000000003', 5, 'Проводит профессиональную чистку.', '/images/doctors/maria.png'),
    ('+79000000004', 3, 'Лечит зубы у взрослых.', '/images/doctors/dmitry.png')
) AS d(phone, experience_years, bio, photo_url)
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

-- Тестовые пациенты с анкетой и записями в разных статусах.
-- Даты считаются от дня запуска скрипта, поэтому записи всегда «свежие».
-- Если дата попала на выходной, запись переносится на ближайший будний день.
--   patient1@dentatime.ru  Иван Петров    — прошёл осмотр терапевта и консультацию хирурга (может записаться на имплантацию)
--   patient2@dentatime.ru  Ольга Сидорова — вчерашняя подтверждённая запись к Анне (в кабинете врача видны
--                          кнопки «Завершить» и «Неявка») и одна запись, которая ждёт подтверждения админом
INSERT INTO users (phone, email, password_hash, role_id, full_name)
SELECT p.phone, p.email, (SELECT password_hash FROM users WHERE phone = '+79000000000'), r.id, p.full_name
FROM (VALUES
    ('+79000000010', 'patient1@dentatime.ru', 'Иван Петров'),
    ('+79000000011', 'patient2@dentatime.ru', 'Ольга Сидорова')
) AS p(phone, email, full_name)
JOIN roles r ON r.name = 'patient'
ON CONFLICT (phone) DO UPDATE SET email = EXCLUDED.email;

INSERT INTO patients (user_id, birth_date, allergies, chronic_diseas, no_show_count, notes)
SELECT u.id, p.birth_date::date, p.allergies, p.chronic, 0, NULL
FROM (VALUES
    ('+79000000010', '1990-04-12', 'Лидокаин', 'Нет'),
    ('+79000000011', '1985-09-03', 'Нет', 'Гипертония')
) AS p(phone, birth_date, allergies, chronic)
JOIN users u ON u.phone = p.phone
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO appointments (doctor_id, patient_id, service_id, cabinet_id, starts_at, ends_at, status)
SELECT d.id, pt.id, s.id, c.id,
       (w.day + a.start_time::time) AT TIME ZONE 'Europe/Moscow',
       (w.day + a.start_time::time + make_interval(mins => s.duration_min)) AT TIME ZONE 'Europe/Moscow',
       a.status
FROM (VALUES
    ('+79000000010', '+79000000001', 'Осмотр и консультация',    101, -30, '10:00', 'completed'),
    ('+79000000010', '+79000000002', 'Консультация хирурга',     201, -20, '11:00', 'completed'),
    ('+79000000010', '+79000000004', 'Лечение кариеса',          102, -10, '15:00', 'cancelled'),
    ('+79000000011', '+79000000001', 'Лечение кариеса',          101,  -1, '15:00', 'confirmed'),
    ('+79000000010', '+79000000001', 'Лечение кариеса',          101,   2, '11:00', 'confirmed'),
    ('+79000000010', '+79000000003', 'Профессиональная гигиена', 103,   4, '10:00', 'scheduled'),
    ('+79000000011', '+79000000001', 'Осмотр и консультация',    101,   2, '12:30', 'scheduled')
) AS a(patient_phone, doctor_phone, service_name, cabinet_number, day_offset, start_time, status)
-- Суббота и воскресенье: будущие записи переносятся на понедельник, прошлые — на пятницу.
CROSS JOIN LATERAL (
    SELECT (current_date + a.day_offset) + CASE extract(isodow FROM current_date + a.day_offset)
        WHEN 6 THEN CASE WHEN a.day_offset >= 0 THEN 2 ELSE -1 END
        WHEN 7 THEN CASE WHEN a.day_offset >= 0 THEN 1 ELSE -2 END
        ELSE 0
    END AS day
) w
JOIN users pt ON pt.phone = a.patient_phone
JOIN users d ON d.phone = a.doctor_phone
JOIN services s ON s.name = a.service_name
JOIN cabinets c ON c.number = a.cabinet_number
WHERE NOT EXISTS (
    SELECT 1 FROM appointments x
    WHERE x.patient_id = pt.id AND x.service_id = s.id AND x.status = a.status
);

COMMIT;
