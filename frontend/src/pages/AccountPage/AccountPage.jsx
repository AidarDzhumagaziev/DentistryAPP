import { statusNames } from '../../data/mockAppointments';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { authFetch } from '../../api/client';
import styles from './AccountPage.module.css';
import HealthForm from '../../components/HealthForm/HealthForm';
import { CLINIC } from '../../data/clinic';

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

function isUpcoming(appointment) {
    const activeStatus = appointment.status === 'scheduled' || appointment.status === 'confirmed';
    return activeStatus && new Date(appointment.starts_at) > Date.now();
}
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
    const [profile, setProfile] = useState(null);
    const [isProfileLoading, setIsProfileLoading] = useState(true);
    const [profileMessage, setProfileMessage] = useState(null);

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
    useEffect(() => {
        authFetch('/api/v1/patients/me/')
            .then((response) => {
                if (response.status === 404) {
                    return null;
                }
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((data) => setProfile(data))
            .catch(() => setProfileMessage('Не удалось загрузить анкету'))
            .finally(() => setIsProfileLoading(false));
    }, []);

    function saveProfile(values) {
        setProfileMessage(null);
        authFetch('/api/v1/patients/me/', {
            method: profile ? 'PATCH' : 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(values),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((data) => {
                setProfile(data);
                setProfileMessage('Анкета сохранена');
            })
            .catch(() => setProfileMessage('Не удалось сохранить анкету'));
    }
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

    function renderAppointment(appointment) {
        return (
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
                    <span className={styles.cancelHint}>
                        Отменить можно по телефону <a href={CLINIC.phoneLink} className={styles.hintPhone}>{CLINIC.phone}</a>
                    </span>
                )}
                {!isUpcoming(appointment) && (
                    <Link
                        to="/booking"
                        state={{ serviceId: appointment.service.id, doctorId: appointment.doctor.user_id }}
                        className={styles.againLink}
                    >
                        Записаться снова
                    </Link>
                )}
            </div>
        );
    }

    if (isLoading) {
        return <p>Загрузка…</p>;
    }
    if (error) {
        return <p>{error}</p>;
    }
    const upcoming = appointments.filter((a) => isUpcoming(a));
    upcoming.sort((a, b) => new Date(a.starts_at) - new Date(b.starts_at));
    const others = appointments.filter((a) => !isUpcoming(a));
    others.sort((a, b) => new Date(b.starts_at) - new Date(a.starts_at));

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
            {tab === 'appointments' && (
                <div>
                    {appointments.length === 0 && <p>У вас пока нет записей.</p>}

                    {upcoming.length > 0 && (
                        <section className={styles.section}>
                            <h2 className={styles.sectionTitle}>Предстоящие</h2>
                            <div className={styles.list}>
                                {upcoming.map((appointment) => renderAppointment(appointment))}
                            </div>
                        </section>
                    )}

                    {others.length > 0 && (
                        <section className={styles.section}>
                            <h2 className={styles.sectionTitle}>Прошедшие и отменённые</h2>
                            <div className={styles.list}>
                                {others.map((appointment) => renderAppointment(appointment))}
                            </div>
                        </section>
                    )}
                </div>
            )}
            {tab === 'profile' && <p>Профиль появится скоро.</p>}
            {tab === 'health' && (
                <div>
                    {isProfileLoading && <p>Загрузка…</p>}
                    {!isProfileLoading && !profile && (
                        <p className={styles.profileNote}>Анкету видит врач перед приёмом. Её нужно заполнить один раз, перед первой записью.</p>
                    )}
                    {!isProfileLoading && (
                        <HealthForm initial={profile} submitLabel="Сохранить" onSave={saveProfile} />
                    )}
                    {profileMessage && <p className={styles.profileNote}>{profileMessage}</p>}
                </div>
            )}
        </div>
    );
}

export default AccountPage;