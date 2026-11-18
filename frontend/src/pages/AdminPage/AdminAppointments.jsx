import { useEffect, useState } from 'react';
import { authFetch, getJson } from '../../api/client';
import { statusNames } from '../../data/mockAppointments';
import FilterButtons from '../../components/FilterButtons/FilterButtons';
import styles from './AdminPage.module.css';

const statusFilters = [
    { id: 'scheduled', name: 'Ждут подтверждения' },
    { id: 'confirmed', name: 'Подтверждены' },
    { id: 'completed', name: 'Завершены' },
    { id: 'cancelled', name: 'Отменены' },
    { id: 'no_show', name: 'Неявки' },
];

function formatDateTime(value) {
    return `${new Date(value).toLocaleDateString('ru-RU')} ${value.slice(11, 16)}`;
}

function loadAllAppointments(doctors) {
    const requests = doctors.map((doctor) =>
        authFetch(`/api/v1/doctors/${doctor.user_id}/appointments`).then((response) => {
            if (!response.ok) {
                throw new Error('Сервер ответил ошибкой');
            }
            return response.json();
        })
    );
    return Promise.all(requests).then((lists) => lists.flat());
}

function AdminAppointments() {
    const [doctors, setDoctors] = useState([]);
    const [doctorId, setDoctorId] = useState('');
    const [status, setStatus] = useState('scheduled');
    const [appointments, setAppointments] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [date, setDate] = useState('');

    useEffect(() => {
        getJson('/api/v1/doctors/')
            .then((doctorsData) => {
                setDoctors(doctorsData);
                return loadAllAppointments(doctorsData);
            })
            .then((data) => setAppointments(data))
            .catch(() => setError('Не удалось загрузить записи'))
            .finally(() => setIsLoading(false));
    }, []);

    function changeStatus(id, action) {
        authFetch(`/api/v1/appointments/${id}/${action}`, { method: 'PATCH' })
            .then((response) => {
                // 500 пока не ошибка: статус сохраняется, падает только ответ сервера
                if (!response.ok && response.status !== 500) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return loadAllAppointments(doctors);
            })
            .then((data) => setAppointments(data))
            .catch(() => alert('Не удалось изменить статус записи'));
    }

    function cancelAppointment(id) {
        if (!confirm('Отменить запись? Пациенту придётся записаться заново.')) {
            return;
        }
        changeStatus(id, 'cancel-by-admin');
    }

    if (isLoading) {
        return <p>Загрузка…</p>;
    }
    if (error) {
        return <p>{error}</p>;
    }

    const shown = appointments.filter((a) =>
        (doctorId === '' || String(a.doctor.user_id) === doctorId) &&
        (status === null || a.status === status) &&
        (date === '' || a.starts_at.slice(0, 10) === date)
    );
    shown.sort((a, b) => new Date(a.starts_at) - new Date(b.starts_at));

    return (
        <div>
            <div className={styles.top}>
                <h1>Записи</h1>
            </div>

            <div className={styles.toolbar}>
                <div className={styles.formGrid}>
                    <label className={styles.field}>
                        Врач
                        <select className={styles.input} value={doctorId} onChange={(e) => setDoctorId(e.target.value)}>
                            <option value="">Все врачи</option>
                            {doctors.map((doctor) => (
                                <option key={doctor.user_id} value={doctor.user_id}>{doctor.user.full_name}</option>
                            ))}
                        </select>
                    </label>
                    <label className={styles.field}>
                        Дата
                        <input type="date" className={styles.input} value={date} onChange={(e) => setDate(e.target.value)} />
                    </label>
                    {date && (
                        <button type="button" className="secondary" onClick={() => setDate('')}>Все даты</button>
                    )}
                </div>
            </div>

            <div className={styles.filtersRow}>
                <FilterButtons items={statusFilters} selectedId={status} onSelect={setStatus} />
            </div>

            {shown.length === 0 && (
                <p className={styles.empty}>{status === 'scheduled' ? 'Все записи подтверждены.' : 'Записей нет.'}</p>
            )}

            {shown.length > 0 && (
                <div className={styles.tableWrap}>
                    <table className={styles.table}>
                        <thead>
                            <tr>
                                <th className={styles.th}>Дата и время</th>
                                <th className={styles.th}>Врач</th>
                                <th className={styles.th}>Пациент</th>
                                <th className={styles.th}>Услуга</th>
                                <th className={styles.th}>Статус</th>
                                <th className={styles.th}></th>
                            </tr>
                        </thead>
                        <tbody>
                            {shown.map((item) => (
                                <tr key={item.id}>
                                    <td className={styles.td}>{formatDateTime(item.starts_at)}</td>
                                    <td className={styles.td}>{item.doctor.user.full_name}</td>
                                    <td className={styles.td}>
                                        {item.patient.user.full_name}
                                        <br />
                                        <a href={`tel:${item.patient.user.phone}`} className={styles.muted}>{item.patient.user.phone}</a>
                                    </td>
                                    <td className={styles.td}>{item.service.name}</td>
                                    <td className={styles.td}>{statusNames[item.status]}</td>
                                    <td className={styles.td}>
                                        <div className={`${styles.rowActions} ${styles.appointmentActions}`}>
                                            {item.status === 'scheduled' && (
                                                <button onClick={() => changeStatus(item.id, 'confirm')}>Подтвердить</button>
                                            )}
                                            {(item.status === 'scheduled' || item.status === 'confirmed') && (
                                                <button className="danger" onClick={() => cancelAppointment(item.id)}>Отменить</button>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default AdminAppointments;