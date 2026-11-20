import { useEffect, useState } from 'react';
import { authFetch, getJson } from '../../api/client';
import { initials } from '../../utils/initials';
import { plural } from '../../utils/plural';
import { formatPhone } from '../../utils/phone';
import styles from './AdminPage.module.css';


const createErrors = {
    'Phone already registered': 'Этот телефон уже занят',
    'Email already registered': 'Эта почта уже занята',
};

function AdminDoctors() {
    const [doctors, setDoctors] = useState([]);
    const [specializations, setSpecializations] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const [editingId, setEditingId] = useState(null);
    const [isCreating, setIsCreating] = useState(false);
    const [fullName, setFullName] = useState('');
    const [phoneDigits, setPhoneDigits] = useState('');
    const [email, setEmail] = useState('');
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

    function startCreate() {
        setEditingId(null);
        setIsCreating(true);
        setFullName('');
        setPhoneDigits('');
        setEmail('');
        setExperience('');
        setBio('');
        setPhotoUrl('');
        setSpecIds([]);
        setFormError(null);
    }

    function startEdit(doctor) {
        setIsCreating(false);
        setEditingId(doctor.user_id);
        setExperience(String(doctor.experience_years));
        setBio(doctor.bio);
        setPhotoUrl(doctor.photo_url);
        setSpecIds(doctor.specializations.map((s) => s.specialization.id));
        setFormError(null);
    }

    function closeForm() {
        setEditingId(null);
        setIsCreating(false);
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
        if (isCreating) {
            if (!fullName.trim()) {
                setFormError('Укажите ФИО врача');
                return;
            }
            if (phoneDigits.length !== 10) {
                setFormError('Введите телефон полностью');
                return;
            }
            if (!email.includes('@')) {
                setFormError('Укажите почту врача');
                return;
            }
        }
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

        const doctorData = {
            experience_years: years,
            bio: bio.trim(),
            photo_url: photoUrl.trim(),
            specializations_ids: specIds,
        };
        const url = isCreating ? '/api/v1/admin/doctors/' : `/api/v1/doctors/${editingId}/`;
        const body = isCreating
            ? { ...doctorData, user: { full_name: fullName.trim(), phone: '+7' + phoneDigits, email: email.trim().toLowerCase() } }
            : doctorData;

        authFetch(url, {
            method: isCreating ? 'POST' : 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((data) => {
                        throw new Error(data.detail);
                    });
                }
                return response.json();
            })
            .then((saved) => {
                if (isCreating) {
                    setDoctors([...doctors, saved]);
                } else {
                    setDoctors(doctors.map((d) => (d.user_id === saved.user_id ? saved : d)));
                }
                closeForm();
            })
            .catch((err) => setFormError(createErrors[err.message] || 'Не удалось сохранить врача'));
    }

    if (isLoading) {
        return <p>Загрузка…</p>;
    }
    if (error) {
        return <p>{error}</p>;
    }

    const editingDoctor = doctors.find((d) => d.user_id === editingId);
    const showForm = isCreating || editingDoctor;

    return (
        <div>
            <div className={styles.top}>
                <h1>Врачи</h1>
                {!showForm && <button onClick={startCreate}>Добавить врача</button>}
            </div>

            {showForm && (
                <form className={styles.formCard} onSubmit={handleSubmit}>
                    <h2>{isCreating ? 'Новый врач' : `Изменить: ${editingDoctor.user.full_name}`}</h2>
                    {isCreating && (
                        <div className={styles.formGrid}>
                            <label className={styles.field}>
                                ФИО
                                <input className={styles.input} value={fullName} onChange={(e) => setFullName(e.target.value)} />
                            </label>
                            <label className={styles.field}>
                                Телефон
                                <input type="tel" className={styles.input} value={formatPhone(phoneDigits)}
                                    onChange={(e) => {
                                        const digits = e.target.value.replace(/\D/g, '');
                                        setPhoneDigits(digits.slice(1, 11));
                                    }}
                                />
                            </label>
                            <label className={styles.field}>
                                Почта
                                <input type="email" className={styles.input} value={email} onChange={(e) => setEmail(e.target.value)} />
                            </label>
                        </div>
                    )}
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
                        <button type="button" className="secondary" onClick={closeForm}>Отмена</button>
                        <button type="submit">{isCreating ? 'Добавить' : 'Сохранить'}</button>
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