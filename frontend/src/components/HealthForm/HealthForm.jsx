import { useState } from 'react';
import styles from './HealthForm.module.css';

function HealthForm({ initial, onSave, submitLabel }) {
    const [birthDate, setBirthDate] = useState(initial ? initial.birth_date : '');
    const [allergies, setAllergies] = useState(initial ? initial.allergies : '');
    const [chronic, setChronic] = useState(initial ? initial.chronic_diseas : '');
    const [error, setError] = useState(null);

    function handleSubmit(e) {
        e.preventDefault();
        if (!birthDate) {
            setError('Укажите дату рождения');
            return;
        }
        if (new Date(birthDate) > new Date()) {
            setError('Дата рождения не может быть в будущем');
            return;
        }
        if (!allergies.trim()) {
            setError('Укажите аллергии или напишите «нет»');
            return;
        }
        if (!chronic.trim()) {
            setError('Укажите хронические болезни или напишите «нет»');
            return;
        }
        setError(null);
        onSave({
            birth_date: birthDate,
            allergies: allergies.trim(),
            chronic_diseas: chronic.trim(),
        });
    }

    return (
        <form className={styles.form} onSubmit={handleSubmit}>
            <label className={styles.field}>
                Дата рождения
                <input
                    type="date"
                    className={styles.input}
                    value={birthDate}
                    onChange={(e) => setBirthDate(e.target.value)}
                />
            </label>
            <label className={styles.field}>
                Аллергии
                <textarea
                    rows="2"
                    className={styles.input}
                    placeholder="Например: лидокаин, пенициллин. Если нет — напишите «нет»"
                    value={allergies}
                    onChange={(e) => setAllergies(e.target.value)}
                />
            </label>
            <label className={styles.field}>
                Хронические болезни
                <textarea
                    rows="2"
                    className={styles.input}
                    placeholder="Например: гипертония, диабет. Если нет — напишите «нет»"
                    value={chronic}
                    onChange={(e) => setChronic(e.target.value)}
                />
            </label>
            {error && <p className={styles.error}>{error}</p>}
            <button type="submit" className={styles.submit}>{submitLabel}</button>
        </form>
    );
}

export default HealthForm;