import { useEffect, useState } from 'react';
import { authFetch, getJson } from '../../api/client';
import { initials } from '../../utils/initials';
import { plural } from '../../utils/plural';
import styles from './AdminPage.module.css';

function AdminDoctors() {
    const [doctors, setDoctors] = useState([]);
    const [specializations, setSpecializations] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const [editingId, setEditingId] = useState(null);
    const [experience, setExperience] = useState('');
    const [bio, setBio] = useState('');
    const [photoUrl, setPhotoUrl] = useState('');
    const [specIds, setSpecIds] = useState([]);
    const [formError, setFormError] = useState(null);

    useEffect(() => {
        Promise.all([getJson('/api/v1/doctors/'), getJson('/api/v1/specializations/')])
            .then(([doctorsData, specsData]) => {
                setDoctors(doctorsData);
                setSpecializations(specsData);
            })
            .catch(() => setError('Не удалось загрузить врачей'))
            .finally(() => setIsLoading(false));
    }, []);

    function startEdit(doctor) {
        setEditingId(doctor.user_id);
        setExperience(String(doctor.experience_years));
        setBio(doctor.bio);
        setPhotoUrl(doctor.photo_url);
        setSpecIds(doctor.specializations.map((s) => s.specialization.id));
        setFormError(null);
    }

    function toggleSpec(id) {
        if (specIds.includes(id)) {
            setSpecIds(specIds.filter((x) => x !== id));
        } else {
            setSpecIds([...specIds, id]);
        }
    }

    function handleSubmit(e) {
        e.preventDefault();
        const years = Number(experience);
        if (!Number.isInteger(years) || years < 1) {
            setFormError('Стаж — целое число лет, не меньше 1');
            return;
        }
        if (!bio.trim()) {
            setFormError('Напишите пару слов о враче');
            return;
        }
        if (specIds.length === 0) {
            setFormError('Выберите хотя бы одну специализацию');
            return;
        }
        authFetch(`/api/v1/doctors/${editingId}/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                experience_years: years,
                bio: bio.trim(),
                photo_url: photoUrl.trim(),
                specializations_ids: specIds,
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((updated) => {
                setDoctors(doctors.map((d) => (d.user_id === updated.user_id ? updated : d)));
                setEditingId(null);
            })
            .catch(() => setFormError('Не удалось сохранить врача'));
    }

    if (isLoading) {
        return <p>Загрузка…</p>;
    }
    if (error) {
        return <p>{error}</p>;
    }

    const editingDoctor = doctors.find((d) => d.user_id === editingId);

    return (
        <div>
            <div className={styles.top}>
                <h1>Врачи</h1>
            </div>
            <p className={styles.muted}>Добавить нового врача можно будет, когда сервер научится создавать пользователя-врача.</p>

            {editingDoctor && (
                <form className={styles.formCard} onSubmit={handleSubmit}>
                    <h2>Изменить: {editingDoctor.user.full_name}</h2>
                    <div className={styles.formGrid}>
                        <label className={styles.field}>
                            Стаж, лет
                            <input type="number" min="1" className={styles.input} value={experience} onChange={(e) => setExperience(e.target.value)} />
                        </label>
                        <label className={styles.field}>
                            Фото (путь к файлу)
                            <input className={styles.input} value={photoUrl} onChange={(e) => setPhotoUrl(e.target.value)} placeholder="/images/doctors/anna.png" />
                        </label>
                    </div>
                    <label className={styles.field}>
                        О враче
                        <textarea rows="3" className={styles.input} value={bio} onChange={(e) => setBio(e.target.value)} />
                    </label>
                    <div className={styles.field}>
                        Специализации
                        {specializations.map((spec) => (
                            <label key={spec.id} className={styles.checkField}>
                                <input type="checkbox" checked={specIds.includes(spec.id)} onChange={() => toggleSpec(spec.id)} />
                                {spec.name}
                            </label>
                        ))}
                    </div>
                    {formError && <p className={styles.formError}>{formError}</p>}
                    <div className={styles.rowActions}>
                        <button type="button" className="secondary" onClick={() => setEditingId(null)}>Отмена</button>
                        <button type="submit">Сохранить</button>
                    </div>
                </form>
            )}

            <div className={styles.tableWrap}>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th className={styles.th}></th>
                            <th className={styles.th}>Врач</th>
                            <th className={styles.th}>Специализации</th>
                            <th className={styles.th}>Стаж</th>
                            <th className={styles.th}></th>
                        </tr>
                    </thead>
                    <tbody>
                        {doctors.map((doctor) => (
                            <tr key={doctor.user_id}>
                                <td className={styles.td}>
                                    {doctor.photo_url
                                        ? <img src={doctor.photo_url} alt={doctor.user.full_name} className={styles.doctorThumb} />
                                        : <div className={styles.doctorThumb}>{initials(doctor.user.full_name)}</div>}
                                </td>
                                <td className={styles.td}>{doctor.user.full_name}</td>
                                <td className={styles.td}>{doctor.specializations.map((s) => s.specialization.name).join(', ')}</td>
                                <td className={styles.td}>{doctor.experience_years} {plural(doctor.experience_years, 'год', 'года', 'лет')}</td>
                                <td className={styles.td}>
                                    <div className={styles.rowActions}>
                                        <button className="secondary" onClick={() => startEdit(doctor)}>Изменить</button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AdminDoctors;