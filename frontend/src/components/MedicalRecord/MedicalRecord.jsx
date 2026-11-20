import { Fragment, useEffect, useState } from 'react';
import { authFetch } from '../../api/client';
import styles from './MedicalRecord.module.css';

const fields = [
    { key: 'complaints', label: 'Жалобы' },
    { key: 'objective_findings', label: 'Осмотр' },
    { key: 'diagnosis', label: 'Диагноз' },
    { key: 'treatment_plan', label: 'План лечения' },
];

function MedicalRecord({ appointmentId, editable }) {
    const [record, setRecord] = useState(undefined);
    const [isEditing, setIsEditing] = useState(false);
    const [form, setForm] = useState({});
    const [error, setError] = useState(null);

    useEffect(() => {
        authFetch(`/api/v1/appointments/${appointmentId}/medical-record/`)
            .then((response) => {
                if (response.status === 404) {
                    return null;
                }
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((data) => setRecord(data))
            .catch(() => setRecord(null));
    }, [appointmentId]);

    function startEdit() {
        setForm({
            complaints: record ? record.complaints || '' : '',
            objective_findings: record ? record.objective_findings || '' : '',
            diagnosis: record ? record.diagnosis || '' : '',
            treatment_plan: record ? record.treatment_plan || '' : '',
        });
        setError(null);
        setIsEditing(true);
    }

    function save(e) {
        e.preventDefault();
        if (!form.diagnosis.trim()) {
            setError('Укажите диагноз');
            return;
        }
        authFetch(`/api/v1/appointments/${appointmentId}/medical-record`, {
            method: record ? 'PATCH' : 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                return response.json();
            })
            .then((data) => {
                setRecord(data);
                setIsEditing(false);
            })
            .catch(() => setError('Не удалось сохранить заключение'));
    }

    if (record === undefined) {
        return null;
    }
    if (!record && !editable) {
        return null;
    }

    if (isEditing) {
        return (
            <form className={styles.box} onSubmit={save}>
                <b>Заключение врача</b>
                {fields.map((f) => (
                    <label key={f.key} className={styles.field}>
                        {f.label}
                        <textarea
                            rows="2"
                            className={styles.input}
                            value={form[f.key]}
                            onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                        />
                    </label>
                ))}
                {error && <p className={styles.error}>{error}</p>}
                <div className={styles.actions}>
                    <button type="button" className="secondary" onClick={() => setIsEditing(false)}>Отмена</button>
                    <button type="submit">Сохранить</button>
                </div>
            </form>
        );
    }

    if (!record) {
        return (
            <div>
                <button type="button" className={`secondary ${styles.smallButton}`} onClick={startEdit}>Заполнить заключение</button>
            </div>
        );
    }

    return (
        <div className={styles.box}>
            <b>Заключение врача</b>
            <dl className={styles.list}>
                {fields.filter((f) => record[f.key]).map((f) => (
                    <Fragment key={f.key}>
                        <dt>{f.label}</dt>
                        <dd>{record[f.key]}</dd>
                    </Fragment>
                ))}
            </dl>
            {editable && (
                <div className={styles.actions}>
                    <button type="button" className="secondary" onClick={startEdit}>Изменить</button>
                </div>
            )}
        </div>
    );
}

export default MedicalRecord;