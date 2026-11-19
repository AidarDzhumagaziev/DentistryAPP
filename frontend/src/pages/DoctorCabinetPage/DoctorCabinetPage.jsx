import { statusNames } from '../../data/mockAppointments';
import { useState, useEffect } from 'react';
import { authFetch } from '../../api/client';

import styles from './DoctorCabinetPage.module.css';

function formatDate(d) {
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${month}-${day}`;
}
function isFilled(text) {
    const value = text.trim().toLowerCase();
    return value !== '' && value !== 'нет';
}
function loadAppointments() {
    return authFetch('/api/v1/doctors/me/appointments').then((response) => {
        if (!response.ok) {
            throw new Error('Сервер ответил ошибкой');
        }
        return response.json();
    });
}
function canMark(appointment) {
    const started = new Date(appointment.starts_at) <= Date.now();
    return appointment.status === 'confirmed' && started;
}

function DoctorCabinetPage() {
    const [appointments, setAppointments] = useState([]);
    const [day, setDay] = useState(formatDate(new Date()));
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadAppointments()
            .then((data) => setAppointments(data))
            .catch(() => setError('Не удалось загрузить приёмы'))
            .finally(() => setIsLoading(false));
    }, []);

    function shiftDay(offset) {
        const d = new Date(day);
        d.setDate(d.getDate() + offset);
        return setDay(formatDate(d));
    }

    const dayAppointments = appointments.filter((a) => a.starts_at.slice(0, 10) === day);
    dayAppointments.sort((a, b) => new Date(a.starts_at) - new Date(b.starts_at));

    function changeStatus(id, action) {
        authFetch(`/api/v1/appointments/${id}/${action}`, { method: 'PATCH' })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((updated) => {
                setAppointments(appointments.map((a) => (a.id === id ? updated : a)));
            })
            .catch(() => alert('Не удалось изменить статус'));
    }

    function markNoShow(id) {
        if (!confirm('Отметить, что пациент не пришёл? Отменить это будет нельзя.')) {
            return;
        }
        changeStatus(id, 'no-show');
    }
    if (isLoading) {
        return <p>Загрузка…</p>;
    }
    if (error) {
        return <p>{error}</p>;
    }
    return (
        <div>
            <div className={styles.top}>
                <h1>Приёмы на {new Date(day).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}</h1>
                <div className={styles.arrows}>
                    <button className={styles.arrow} onClick={() => shiftDay(-1)}>‹</button>
                    <input className={styles.dateInput} type="date" value={day} onChange={(e) => {
                        setDay(e.target.value);
                    }} />
                    <button className={styles.arrow} onClick={() => shiftDay(1)}>›</button>
                </div>
            </div>
            {dayAppointments.length === 0 && <p>Приёмов нет</p>}
            <div className={styles.list}>
                {dayAppointments.map((appointment) => (
                    <div key={appointment.id} className={styles.row}>
                        <div className={styles.timeBox}>
                            <span className={styles.time}>{appointment.starts_at.slice(11, 16)}</span>
                            <span className={styles.duration}>{appointment.service.duration_min} мин</span>
                        </div>
                        <div className={styles.info}>
                            <span className={styles.patient}>{appointment.patient.user.full_name}</span>
                            <span className={styles.service}>{appointment.service.name}</span>
                            <span className={styles.service}>кабинет {appointment.cabinet.number}</span>
                            <div className={styles.tags}>
                                <span className={`${styles.status} ${styles[appointment.status]}`}>{statusNames[appointment.status]}</span>
                                {isFilled(appointment.patient.allergies) && <span className={styles.alert}>Аллергии: {appointment.patient.allergies}</span>}
                                {isFilled(appointment.patient.chronic_diseas) && <span className={styles.alert}>Хронические болезни: {appointment.patient.chronic_diseas}</span>}
                            </div>


                        </div>
                        <div className={styles.actions}>
                            {canMark(appointment) && <button onClick={() => changeStatus(appointment.id, 'completed')}>Завершить</button>}
                            {canMark(appointment) && <button className="danger" onClick={() => markNoShow(appointment.id)}>Неявка</button>}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
export default DoctorCabinetPage;