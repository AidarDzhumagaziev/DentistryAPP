import { getJson, authHeaders } from '../../api/client';
import styles from './AdminPage.module.css';
import { useState, useEffect } from 'react';

function AdminPage(){
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [services, setServices] = useState([]);
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [price, setPrice] = useState('');
    const [duration, setDuration] = useState('');
    const [buffer, setBuffer] = useState('');
    const [cabinetType, setCabinetType] = useState('general');
    const [specializationId, setSpecializationId] = useState('');
    const [needConsult, setNeedConsult] = useState(false);

    function handleSubmit(e){
        e.preventDefault();
        fetch(`/api/v1/services/`, {
            method: 'POST',
            headers: { ...authHeaders(), 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                description: description, 
                specialization_id: Number(specializationId), 
                price_from: Number(price),
                duration_min: Number(duration),
                buffer_min:Number(buffer),
                cabinet_type: cabinetType,
                requires_consultation: needConsult,
            })
        })
        .then((response) =>{
            if (!response.ok) {
                throw new Error('Сервер ответил ошибкой');
            }
            return response.json();
        })
        .then((data) => {
            setServices([...services, data]);
            setName('');
            setDescription('');
            setPrice('');
            setDuration('');
            setBuffer('');
            setCabinetType('general');
            setSpecializationId('');
            setNeedConsult(false);
        })
        .catch(() => alert('Не удалось добавить услугу'))
    }

    useEffect(() => {
        getJson('/api/v1/services/')
        .then((data) => setServices(data))
        .catch(() => setError('Не удалось загрузить услуги'))
        .finally(() => setIsLoading(false));
    }, []);

    const [specializations, setSpecializations] = useState([]);
        useEffect(() => {
        getJson('/api/v1/specializations/')
        .then((data) => setSpecializations(data));
    }, []);


    function deleteService(id){
        if (!confirm('Удалить услугу?')) return;

        fetch(`/api/v1/services/${id}/`, {
            method: 'DELETE',
            headers:authHeaders() ,
        })
        .then((response) =>{
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                setServices(services.filter((s) => s.id !== id));
            })
        .catch(() => alert('Не удалось удалить услугу'))
    }
    if (isLoading) {
        return <p>Загрузка…</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }
    return(
        <div>
            <h1>Админ панель</h1>
            <table className={styles.table}>
                <thead>
                    <tr>
                    <th className={styles.th}>Название</th>
                    <th className={styles.th}>Цена</th>
                    <th className={styles.th}>Длительность</th>
                    <th className={styles.th}>Консультация</th>
                    <th className={styles.th}></th>
                    </tr>
                </thead>
                <tbody>
                    {services.map((service) => (
                    <tr key={service.id}>
                    <td className={styles.td}>{service.name}</td>
                    <td className={styles.td}>от {Number(service.price_from).toLocaleString('ru-RU')} ₽</td>
                    <td className={styles.td}>{service.duration_min} мин</td>
                    <td className={styles.td}>{service.requires_consultation ? 'Да' : 'Нет'}</td>
                    <td className={styles.td}><button onClick={() => deleteService(service.id)}>Удалить</button></td>
                    </tr>
                    ))}
                </tbody>
            </table>



            <h1 className={styles.h1}>Добавить услугу</h1>
            <form className={styles.form} onSubmit={handleSubmit}>
                <label className={styles.field}>
                    Название 
                    <input type="text" className={styles.input} 
                    value={name}
                    onChange={(e) => setName(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Описание
                    <input type="text" className={styles.input} 
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Цена от 
                    <input type="number" className={styles.input} 
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Длительность, мин
                    <input type="number" className={styles.input}
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Перерыв после, мин
                    <input type="number" className={styles.input}
                    value={buffer}
                    onChange={(e) => setBuffer(e.target.value)}/>
                </label>
                <label className={styles.field}>
                    Кабинет
                    <select value={cabinetType} onChange={(e) => setCabinetType(e.target.value)}>
                        <option value="general">Общий</option>
                        <option value="surgical">Хирургический</option>
                        <option value="roentgen">Рентген</option>
                    </select>
                </label>
                <label className={styles.field}>
                    Специальность
                    <select value={specializationId} onChange={(e) => setSpecializationId(e.target.value)}>
                        <option value="">Выберите…</option>
                        {specializations.map((s)=>(
                            <option key={s.id} value={s.id}>{s.name}</option>
                        ))}
                    </select>
                </label>
                <label className={styles.field}>
                    Нужна консультация
                    <input type="checkbox" checked={needConsult} onChange={(e) => setNeedConsult(e.target.checked)} />
                </label>
                <button type="submit">Добавить</button>
            </form>
        </div>
    )
}
export default AdminPage;