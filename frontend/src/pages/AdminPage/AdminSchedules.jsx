import { useEffect, useState } from 'react';
import { authFetch, getJson } from '../../api/client';
import styles from './AdminPage.module.css';

const weekdays = [
    { value: 1, label: 'Понедельник' },
    { value: 2, label: 'Вторник' },
    { value: 3, label: 'Среда' },
    { value: 4, label: 'Четверг' },
    { value: 5, label: 'Пятница' },
    { value: 6, label: 'Суббота' },
    { value: 7, label: 'Воскресенье' },
];

const reasons = [
    { value: 'vacation', label: 'Отпуск' },
    { value: 'sick_day', label: 'Больничный' },
];

function dayLabel(value) {
    const day = weekdays.find((item) => item.value === value);
    return day ? day.label : value;
}
function formatTime(value) {
    return value ? value.slice(0, 5) : '';
}

function formatDate(value) {
    return value ? new Date(value).toLocaleDateString('ru-RU') : '';
}

function reasonLabel(value) {
    const reason = reasons.find((item) => item.value === value);
    return reason ? reason.label : value;
}

function sendJson(url, method, body) {
    return authFetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
}

function AdminSchedules() {
    const [doctors, setDoctors] = useState([]);
    const [cabinets, setCabinets] = useState([]);
    const [doctorId, setDoctorId] = useState('');
    const [schedules, setSchedules] = useState([]);
    const [exceptions, setExceptions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isSchedulesLoading, setIsSchedulesLoading] = useState(false);
    const [error, setError] = useState(null);

    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [formError, setFormError] = useState(null);
    const [weekday, setWeekday] = useState('1');
    const [cabinetId, setCabinetId] = useState('');
    const [startTime, setStartTime] = useState('09:00');
    const [endTime, setEndTime] = useState('18:00');

    const [showExceptionForm, setShowExceptionForm] = useState(false);
    const [editingExceptionId, setEditingExceptionId] = useState(null);
    const [exceptionFormError, setExceptionFormError] = useState(null);
    const [dateFrom, setDateFrom] = useState('');
    const [dateTo, setDateTo] = useState('');
    const [reason, setReason] = useState('vacation');

    useEffect(() => {
        Promise.all([getJson('/api/v1/doctors/'), getJson('/api/v1/cabinets/')])
            .then(([doctorsData, cabinetsData]) => {
                setDoctors(doctorsData);
                setCabinets(cabinetsData);
            })
            .catch(() => setError('Не удалось загрузить врачей и кабинеты'))
            .finally(() => setIsLoading(false));
    }, []);

    const selectedDoctor = doctors.find((doctor) => String(doctor.user_id) === doctorId);
    const sortedSchedules = [...schedules].sort((a, b) => a.weekday - b.weekday);

    function loadSchedules(id) {
        setIsSchedulesLoading(true);
        Promise.all([
            getJson(`/api/v1/doctors/${id}/work_schedules`),
            getJson(`/api/v1/doctors/${id}/schedules_exception`),
        ])
            .then(([schedulesData, exceptionsData]) => {
                setSchedules(schedulesData);
                setExceptions(exceptionsData);
            })
            .catch(() => setError('Не удалось загрузить график врача'))
            .finally(() => setIsSchedulesLoading(false));
    }

    function cabinetNumber(currentCabinetId) {
        const cabinet = cabinets.find((item) => item.id === currentCabinetId);
        return cabinet ? `№${cabinet.number}` : '—';
    }

    function changeDoctor(value) {
        setDoctorId(value);
        setShowForm(false);
        setEditingId(null);
        setFormError(null);
        setShowExceptionForm(false);
        setEditingExceptionId(null);
        setExceptionFormError(null);
        if (value) {
            loadSchedules(value);
        }
    }

    function resetForm() {
        setWeekday('1');
        setCabinetId(cabinets.length > 0 ? String(cabinets[0].id) : '');
        setStartTime('09:00');
        setEndTime('18:00');
        setEditingId(null);
        setShowForm(false);
        setFormError(null);
    }

    function startCreate() {
        resetForm();
        setShowForm(true);
    }

    function startEdit(schedule) {
        setWeekday(String(schedule.weekday));
        setCabinetId(String(schedule.cabinet_id));
        setStartTime(formatTime(schedule.start_time));
        setEndTime(formatTime(schedule.end_time));
        setEditingId(schedule.id);
        setShowForm(true);
        setFormError(null);
    }

    function handleSubmit(e) {
        e.preventDefault();

        if (!cabinetId || !startTime || !endTime) {
            setFormError('Заполните кабинет, начало и конец смены');
            return;
        }
        if (startTime >= endTime) {
            setFormError('Начало должно быть раньше окончания');
            return;
        }

        sendJson(
            editingId ? `/api/v1/work_schedules/${editingId}/` : '/api/v1/work_schedules/',
            editingId ? 'PATCH' : 'POST',
            {
                doctor_id: Number(doctorId),
                cabinet_id: Number(cabinetId),
                weekday: Number(weekday),
                start_time: startTime,
                end_time: endTime,
            }
        )
            .then((response) => {
                if (response.status === 409) {
                    throw new Error('Кабинет занят или у врача уже есть смена в это время');
                }
                if (!response.ok) {
                    throw new Error('Не удалось сохранить смену');
                }
                resetForm();
                loadSchedules(doctorId);
            })
            .catch((saveError) => setFormError(saveError.message));
    }

    function remove(id) {
        if (!confirm('Удалить смену?')) {
            return;
        }
        authFetch(`/api/v1/work_schedules/${id}/`, { method: 'DELETE' })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                loadSchedules(doctorId);
            })
            .catch(() => alert('Не удалось удалить смену'));
    }

    function resetExceptionForm() {
        setDateFrom('');
        setDateTo('');
        setReason('vacation');
        setEditingExceptionId(null);
        setShowExceptionForm(false);
        setExceptionFormError(null);
    }

    function startCreateException() {
        resetExceptionForm();
        setShowExceptionForm(true);
    }

    function startEditException(item) {
        setDateFrom(item.date_from);
        setDateTo(item.date_to);
        setReason(item.reason);
        setEditingExceptionId(item.id);
        setShowExceptionForm(true);
        setExceptionFormError(null);
    }

    function handleExceptionSubmit(e) {
        e.preventDefault();

        if (!dateFrom || !dateTo) {
            setExceptionFormError('Укажите даты начала и окончания');
            return;
        }
        if (dateFrom > dateTo) {
            setExceptionFormError('Дата начала не может быть позже даты окончания');
            return;
        }

        sendJson(
            editingExceptionId
                ? `/api/v1/schedules_exception/${editingExceptionId}/?schedule_id=${editingExceptionId}`
                : '/api/v1/schedules_exception/',
            editingExceptionId ? 'PUT' : 'POST',
            {
                doctor_id: Number(doctorId),
                date_from: dateFrom,
                date_to: dateTo,
                reason,
            }
        )
            .then((response) => {
                if (response.status === 409) {
                    throw new Error('На эти даты у врача уже есть отпуск или больничный');
                }
                if (!response.ok) {
                    throw new Error('Не удалось сохранить отпуск');
                }
                resetExceptionForm();
                loadSchedules(doctorId);
            })
            .catch((saveError) => setExceptionFormError(saveError.message));
    }

    function removeException(id) {
        if (!confirm('Удалить отпуск или больничный?')) {
            return;
        }
        authFetch(`/api/v1/schedules_exception/${id}/?schedule_id=${id}`, { method: 'DELETE' })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                loadSchedules(doctorId);
            })
            .catch(() => alert('Не удалось удалить отпуск'));
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
                <h1>Графики работы</h1>
            </div>

            <div className={styles.toolbar}>
                <label className={styles.field}>
                    Врач
                    <select
                        className={styles.input}
                        value={doctorId}
                        onChange={(e) => changeDoctor(e.target.value)}
                    >
                        <option value="">Выберите врача…</option>
                        {doctors.map((doctor) => (
                            <option key={doctor.user_id} value={doctor.user_id}>
                                {doctor.user.full_name}
                            </option>
                        ))}
                    </select>
                </label>
            </div>

            {!selectedDoctor && <p className={styles.empty}>Выберите врача, чтобы увидеть его смены и отпуска.</p>}

            {selectedDoctor && (
                <div className={styles.formCard}>
                    <div className={styles.top}>
                        <h2>Смены: {selectedDoctor.user.full_name}</h2>
                        <button onClick={startCreate}>Добавить смену</button>
                    </div>

                    {showForm && (
                        <form className={styles.form} onSubmit={handleSubmit}>
                            <div className={styles.formGrid}>
                                <label className={styles.field}>
                                    День
                                    <select
                                        className={styles.input}
                                        value={weekday}
                                        disabled={editingId !== null}
                                        onChange={(e) => setWeekday(e.target.value)}
                                    >
                                        {weekdays.map((day) => (
                                            <option key={day.value} value={day.value}>{day.label}</option>
                                        ))}
                                    </select>
                                </label>
                                <label className={styles.field}>
                                    Кабинет
                                    <select
                                        className={styles.input}
                                        value={cabinetId}
                                        onChange={(e) => setCabinetId(e.target.value)}
                                    >
                                        {cabinets.map((cabinet) => (
                                            <option key={cabinet.id} value={cabinet.id}>№{cabinet.number}</option>
                                        ))}
                                    </select>
                                </label>
                                <label className={styles.field}>
                                    Начало
                                    <input
                                        type="time"
                                        className={styles.input}
                                        value={startTime}
                                        onChange={(e) => setStartTime(e.target.value)}
                                    />
                                </label>
                                <label className={styles.field}>
                                    Конец
                                    <input
                                        type="time"
                                        className={styles.input}
                                        value={endTime}
                                        onChange={(e) => setEndTime(e.target.value)}
                                    />
                                </label>
                            </div>
                            {formError && <p className={styles.formError}>{formError}</p>}
                            <div className={styles.rowActions}>
                                <button type="submit" className={styles.submit}>
                                    {editingId ? 'Сохранить' : 'Добавить'}
                                </button>
                                <button type="button" className="secondary" onClick={resetForm}>Отмена</button>
                            </div>
                        </form>
                    )}

                    {isSchedulesLoading && <p>Загрузка…</p>}

                    {!isSchedulesLoading && (
                        <div className={styles.tableWrap}>
                            <table className={styles.table}>
                                <thead>
                                    <tr>
                                        <th className={styles.th}>День</th>
                                        <th className={styles.th}>Время</th>
                                        <th className={styles.th}>Кабинет</th>
                                        <th className={styles.th}></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {sortedSchedules.map((item) => (
                                        <tr key={item.id}>
                                            <td className={styles.td}>{dayLabel(item.weekday)}</td>
                                            <td className={styles.td}>
                                                {formatTime(item.start_time)}–{formatTime(item.end_time)}
                                            </td>
                                            <td className={styles.td}>{cabinetNumber(item.cabinet_id)}</td>
                                            <td className={styles.td}>
                                                <div className={styles.rowActions}>
                                                    <button onClick={() => startEdit(item)} className="secondary">Изменить</button>
                                                    <button onClick={() => remove(item.id)} className="danger">Удалить</button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}

                                </tbody>
                            </table>
                        </div>
                    )}
                    {!isSchedulesLoading && schedules.length === 0 && (
                        <p className={styles.empty}>Смен пока нет.</p>
                    )}
                </div>
            )}

            {selectedDoctor && (
                <div className={styles.formCard}>
                    <div className={styles.top}>
                        <h2>Отпуска и больничные: {selectedDoctor.user.full_name}</h2>
                        <button onClick={startCreateException}>Добавить</button>
                    </div>

                    {showExceptionForm && (
                        <form className={styles.form} onSubmit={handleExceptionSubmit}>
                            <div className={styles.formGrid}>
                                <label className={styles.field}>
                                    С
                                    <input
                                        type="date"
                                        className={styles.input}
                                        value={dateFrom}
                                        onChange={(e) => setDateFrom(e.target.value)}
                                    />
                                </label>
                                <label className={styles.field}>
                                    По
                                    <input
                                        type="date"
                                        className={styles.input}
                                        value={dateTo}
                                        onChange={(e) => setDateTo(e.target.value)}
                                    />
                                </label>
                                <label className={styles.field}>
                                    Причина
                                    <select
                                        className={styles.input}
                                        value={reason}
                                        onChange={(e) => setReason(e.target.value)}
                                    >
                                        {reasons.map((item) => (
                                            <option key={item.value} value={item.value}>{item.label}</option>
                                        ))}
                                    </select>
                                </label>
                            </div>
                            {exceptionFormError && <p className={styles.formError}>{exceptionFormError}</p>}
                            <div className={styles.rowActions}>
                                <button type="submit" className={styles.submit}>
                                    {editingExceptionId ? 'Сохранить' : 'Добавить'}
                                </button>
                                <button type="button" className="secondary" onClick={resetExceptionForm}>Отмена</button>
                            </div>
                        </form>
                    )}

                    {isSchedulesLoading && <p>Загрузка…</p>}

                    {!isSchedulesLoading && exceptions.length === 0 && (
                        <p className={styles.empty}>Отпусков и больничных нет.</p>
                    )}

                    {!isSchedulesLoading && exceptions.length > 0 && (
                        <div className={styles.tableWrap}>
                            <table className={styles.table}>
                                <thead>
                                    <tr>
                                        <th className={styles.th}>Период</th>
                                        <th className={styles.th}>Причина</th>
                                        <th className={styles.th}></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {exceptions.map((item) => (
                                        <tr key={item.id}>
                                            <td className={styles.td}>
                                                {formatDate(item.date_from)} — {formatDate(item.date_to)}
                                            </td>
                                            <td className={styles.td}>{reasonLabel(item.reason)}</td>
                                            <td className={styles.td}>
                                                <div className={styles.rowActions}>
                                                    <button onClick={() => startEditException(item)} className="secondary">Изменить</button>
                                                    <button onClick={() => removeException(item.id)} className="danger">Удалить</button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default AdminSchedules;