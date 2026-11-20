import { useEffect, useState } from 'react';
import { authFetch } from '../../api/client';
import { formatPhone } from '../../utils/phone';
import styles from './AdminPage.module.css';

function searchUrl(query) {
    const text = query.trim();
    if (!text) {
        return '/api/v1/admin/patients/';
    }
    let digits = text.replace(/\D/g, '');
    if (digits.length === 11 && digits.startsWith('8')) {
        digits = '7' + digits.slice(1);
    }
    if (digits.length >= 3) {
        return `/api/v1/admin/patients/?phone=${digits}`;
    }
    return `/api/v1/admin/patients/?full_name=${encodeURIComponent(text)}`;
}

function loadPatients(query) {
    return authFetch(searchUrl(query)).then((response) => {
        if (!response.ok) {
            throw new Error('Сервер ответил ошибкой');
        }
        return response.json();
    });
}

function PatientCard({ user, onClose }) {
    const [patient, setPatient] = useState(undefined);
    const [loadError, setLoadError] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [birthDate, setBirthDate] = useState('');
    const [allergies, setAllergies] = useState('');
    const [chronic, setChronic] = useState('');
    const [formError, setFormError] = useState(null);

    useEffect(() => {
        authFetch(`/api/v1/patients/${user.id}/`)
            .then((response) => {
                if (response.status === 404) {
                    return null;
                }
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then(setPatient)
            .catch(() => setLoadError('Не удалось загрузить анкету'));
    }, [user.id]);

    function startEdit() {
        setBirthDate(patient ? patient.birth_date : '');
        setAllergies(patient ? patient.allergies : '');
        setChronic(patient ? patient.chronic_diseas : '');
        setFormError(null);
        setIsEditing(true);
    }

    function handleSave(e) {
        e.preventDefault();
        if (!birthDate) {
            setFormError('Укажите дату рождения');
            return;
        }

        const data = {
            birth_date: birthDate,
            allergies: allergies.trim() || 'Нет',
            chronic_diseas: chronic.trim() || 'Нет',
        };
        const body = patient ? data : { ...data, user_id: user.id };

        authFetch(patient ? `/api/v1/patients/${user.id}/` : '/api/v1/patients/', {
            method: patient ? 'PATCH' : 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((saved) => {
                setPatient(saved);
                setIsEditing(false);
            })
            .catch(() => setFormError('Не удалось сохранить анкету'));
    }

    return (
        <div className={styles.formCard}>
            <div className={styles.cardHeader}>
                <h2>{user.full_name}</h2>
                <button type="button" className="secondary" onClick={onClose}>Закрыть</button>
            </div>

            {loadError && <p className={styles.formError}>{loadError}</p>}
            {patient === undefined && !loadError && <p>Загрузка…</p>}

            {patient === null && !isEditing && (
                <>
                    <p className={styles.muted}>Пациент ещё не заполнил анкету здоровья.</p>
                    <div className={styles.rowActions}>
                        <button onClick={startEdit}>Заполнить анкету</button>
                    </div>
                </>
            )}

            {patient && !isEditing && (
                <>
                    <dl className={styles.infoList}>
                        <dt>Дата рождения</dt>
                        <dd>{patient.birth_date.split('-').reverse().join('.')}</dd>
                        <dt>Аллергии</dt>
                        <dd>{patient.allergies || '—'}</dd>
                        <dt>Хронические заболевания</dt>
                        <dd>{patient.chronic_diseas || '—'}</dd>
                    </dl>
                    <div className={styles.rowActions}>
                        <button onClick={startEdit}>Изменить анкету</button>
                    </div>
                </>
            )}

            {isEditing && (
                <form className={styles.form} onSubmit={handleSave}>
                    <label className={styles.field}>
                        Дата рождения
                        <input type="date" className={styles.input} value={birthDate} onChange={(e) => setBirthDate(e.target.value)} />
                    </label>
                    <label className={styles.field}>
                        Аллергии
                        <input className={styles.input} value={allergies} onChange={(e) => setAllergies(e.target.value)} placeholder="Нет" />
                    </label>
                    <label className={styles.field}>
                        Хронические заболевания
                        <input className={styles.input} value={chronic} onChange={(e) => setChronic(e.target.value)} placeholder="Нет" />
                    </label>
                    {formError && <p className={styles.formError}>{formError}</p>}
                    <div className={styles.rowActions}>
                        <button type="button" className="secondary" onClick={() => setIsEditing(false)}>Отмена</button>
                        <button type="submit">Сохранить</button>
                    </div>
                </form>
            )}
        </div>
    );
}

function AdminPatients() {
    const [patients, setPatients] = useState([]);
    const [query, setQuery] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selected, setSelected] = useState(null);

    useEffect(() => {
        loadPatients('')
            .then(setPatients)
            .catch(() => setError('Не удалось загрузить пациентов'))
            .finally(() => setIsLoading(false));
    }, []);

    function handleSearch(e) {
        e.preventDefault();
        setError(null);
        loadPatients(query)
            .then(setPatients)
            .catch(() => setError('Не удалось найти пациентов'));
    }

    if (isLoading) {
        return <p>Загрузка…</p>;
    }

    return (
        <div>
            <div className={styles.top}>
                <h1>Пациенты</h1>
            </div>

            {selected && (
                <PatientCard key={selected.id} user={selected} onClose={() => setSelected(null)} />
            )}

            <form className={styles.searchRow} onSubmit={handleSearch}>
                <input
                    className={styles.input}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Имя или телефон"
                />
                <button type="submit">Найти</button>
            </form>

            {error && <p className={styles.formError}>{error}</p>}

            {patients.length === 0 && !error && (
                <p className={styles.empty}>Никого не нашли.</p>
            )}

            {patients.length > 0 && (
                <div className={styles.tableWrap}>
                    <table className={styles.table}>
                        <thead>
                            <tr>
                                <th className={styles.th}>Пациент</th>
                                <th className={styles.th}>Телефон</th>
                                <th className={styles.th}>Почта</th>
                                <th className={styles.th}></th>
                            </tr>
                        </thead>
                        <tbody>
                            {patients.map((patient) => (
                                <tr key={patient.id}>
                                    <td className={styles.td}>{patient.full_name}</td>
                                    <td className={styles.td}>{formatPhone(patient.phone.slice(2))}</td>
                                    <td className={styles.td}>{patient.email || '—'}</td>
                                    <td className={styles.td}>
                                        <div className={styles.rowActions}>
                                            <button className="secondary" onClick={() => setSelected(patient)}>Открыть</button>
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

export default AdminPatients;