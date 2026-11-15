import { statusNames } from '../../data/mockAppointments';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { authFetch } from '../../api/client';
import styles from './AccountPage.module.css';
import HealthForm from '../../components/HealthForm/HealthForm';

function getDay(start) {
    return new Date(start).getDate();
}

function getMonth(start) {
    return new Date(start).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' }).split(' ')[1];
}
function getTime(start) {
    return new Date(start).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
}
const DAY_MS = 24 * 60 * 60 * 1000;

function canCancel(appointment) {
    const activeStatus = appointment.status === 'scheduled' || appointment.status === 'confirmed';
    const moreThanDay = new Date(appointment.starts_at) - Date.now() > DAY_MS;
    return activeStatus && moreThanDay;
}

const tabs = [
    { id: 'appointments', label: 'Мои записи' },
    { id: 'profile', label: 'Профиль' },
    { id: 'health', label: 'Анкета здоровья' },
];

function AccountPage() {
    const [tab, setTab] = useState('appointments');
    const [appointments, setAppointments] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        authFetch('/api/v1/appointments/me/')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((data) => setAppointments(data))
            .catch(() => setError('Не удалось загрузить записи'))
            .finally(() => setIsLoading(false));
    }, []);

    function cancel(id) {
        if (!confirm('Отменить запись?')) return;

        authFetch(`/api/v1/appointments/${id}/cancel-by-patient`, { method: 'PATCH' })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((updated) => {
                setAppointments(appointments.map((a) => (a.id === id ? updated : a)));
            })
            .catch(() => alert('Не удалось отменить запись'));
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
                <h1>Личный кабинет</h1>
                <Link to="/booking" className={styles.newButton}>Новая запись</Link>
            </div>
            <div className={styles.tabs}>
                {tabs.map((t) => (
                    <button
                        key={t.id}
                        className={t.id === tab ? `${styles.tab} ${styles.tabActive}` : styles.tab}
                        onClick={() => setTab(t.id)}
                    >
                        {t.label}
                    </button>
                ))}
            </div>
            {appointments.length === 0 && <p>У вас пока нет записей.</p>}
            {tab === 'appointments' && (
            <div className={styles.list}>
                {appointments.map((appointment) => (
                    <div key={appointment.id} className={styles.row}>
                        <div className={styles.dateBox}>
                            <span className={styles.day}>{getDay(appointment.starts_at)}</span>
                            <span className={styles.month}>{getMonth(appointment.starts_at)}</span>
                            <span className={styles.time}>{getTime(appointment.starts_at)}</span>
                        </div>

                        <div className={styles.info}>
                            <span className={styles.service}>{appointment.service.name}</span>
                            <span className={styles.doctor}>{appointment.doctor.user.full_name} · кабинет {appointment.cabinet.number}</span>
                            <span className={`${styles.status} ${styles[appointment.status]}`}>
                                {statusNames[appointment.status]}
                            </span>
                        </div>
                            {canCancel(appointment) && (
                                <button onClick={() => cancel(appointment.id)} className="danger">Отменить</button>
                            )}
                            {(appointment.status === 'scheduled' || appointment.status === 'confirmed') && !canCancel(appointment) && (
                                <span className={styles.cancelHint}>Отменить можно по телефону клиники</span>
                            )}
                    </div>
                ))}
            </div>
            )}
            {tab === 'profile' && <p>Профиль появится скоро.</p>}
            {tab === 'health' && (
                <HealthForm
                    submitLabel="Сохранить"
                    onSave={(values) => alert('Сохранение появится, когда сервер будет готов: ' + JSON.stringify(values))}
                />
            )}
        </div>
    );
}

export default AccountPage;