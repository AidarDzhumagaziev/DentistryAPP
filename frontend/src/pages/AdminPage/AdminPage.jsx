import { getJson, authFetch } from '../../api/client';
import styles from './AdminPage.module.css';
import { useState, useEffect } from 'react';
import AdminCabinets from './AdminCabinets';
import AdminSchedules from './AdminSchedules';
import AdminAppointments from './AdminAppointments';
import FilterButtons from '../../components/FilterButtons/FilterButtons';
import AdminDoctors from './AdminDoctors';

const sections = [
    { id: 'services', label : 'Услуги' },
    { id: 'doctors', label : 'Врачи' },
    { id: 'cabinets', label : 'Кабинеты' },
    { id: 'schedules', label : 'Графики работы' },
    { id: 'appointments', label : 'Записи' },
];



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
    const [showForm, setShowForm] = useState(false);
    const [section, setSection] = useState('services');
    const [editingId, setEditingId] = useState(null);
    const [filterId, setFilterId] = useState(null);

    function getSectionClass(id) {
        if (id === section) {
        return `${styles.menuItem} ${styles.menuActive}`;
        }
        return styles.menuItem
    }
    function resetForm() {
        setName('');
        setDescription('');
        setPrice('');
        setDuration('');
        setBuffer('');
        setCabinetType('general');
        setSpecializationId('');
        setNeedConsult(false);
        setEditingId(null);
        setShowForm(false);
    }
    function toggleForm() {
        if (showForm) {
            resetForm();
        } else {
            setShowForm(true);
        }
    }
    function startEdit(service) {
        setName(service.name);
        setDescription(service.description);
        setPrice(Number(service.price_from));
        setDuration(service.duration_min);
        setBuffer(service.buffer_min);
        setCabinetType(service.cabinet_type);
        setSpecializationId(service.specialization_id);
        setNeedConsult(service.requires_consultation);
        setEditingId(service.id);
        setShowForm(true);
    }
    function handleSubmit(e){
        e.preventDefault();
        const url = editingId ? `/api/v1/services/${editingId}/` : '/api/v1/services/';
        const method = editingId ? 'PUT' : 'POST';

        authFetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                description: description,
                specialization_id: Number(specializationId),
                price_from: Number(price),
                duration_min: Number(duration),
                buffer_min: Number(buffer),
                cabinet_type: cabinetType,
                requires_consultation: needConsult,
            })
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Сервер ответил ошибкой');
            }
            return response.json();
        })
        .then((data) => {
            if (editingId) {
                setServices(services.map((s) => (s.id === data.id ? data : s)));
            } else {
                setServices([...services, data]);
            }
            resetForm();
        })
        .catch(() => alert('Не удалось сохранить услугу'));
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
    const shownServices = services.filter((service) => filterId === null || service.specialization_id === filterId);


    function deleteService(id){
        if (!confirm('Удалить услугу?')) return;

        authFetch(`/api/v1/services/${id}/`, {
            method: 'DELETE',
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
        <div className={styles.layout}>

            <nav className={styles.sidebar}>
                    {sections.map((s) => (
                    <button key={s.id} className={getSectionClass(s.id)} onClick={() => setSection(s.id)}>
                        {s.label}
                    </button>
                    ))}
            </nav>
            <div className={styles.content}>
            {section === 'services' && (<div>
                <div className={styles.top}>
                    <h1>Услуги</h1>
                    <button onClick={toggleForm}>
                        {showForm ? 'Отмена' : 'Добавить услугу'}
                    </button>
                </div>

                {showForm && (<div className={styles.formCard}>
                    <h2>{editingId ? 'Изменить услугу' : 'Новая услуга'}</h2>
                    <form className={styles.form} onSubmit={handleSubmit}>
                        <label className={styles.field}>
                            Название 
                            <input type="text" className={styles.input} 
                            value={name}
                            onChange={(e) => setName(e.target.value)}/>
                        </label>
                        <label className={styles.field}>
                            Описание
                            <textarea rows="3"  className={styles.input} 
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
                            Пауза до следующего пациента, мин
                            <input type="number" min="0" max="60" className={styles.input}
                            value={buffer}
                            onChange={(e) => setBuffer(e.target.value)}/>
                        </label>
                        <label className={styles.field}>
                            Кабинет
                            <select className={styles.input} value={cabinetType} onChange={(e) => setCabinetType(e.target.value)}>
                                <option value="general">Общий</option>
                                <option value="surgical">Хирургический</option>
                                <option value="roentgen">Рентген</option>
                            </select>
                        </label>
                        <label className={styles.field}>
                            Специальность
                            <select className={styles.input} value={specializationId} onChange={(e) => setSpecializationId(e.target.value)}>
                                <option value="">Выберите…</option>
                                {specializations.map((s)=>(
                                    <option key={s.id} value={s.id}>{s.name}</option>
                                ))}
                            </select>
                        </label>
                        <label className={styles.checkField}>
                            <input type="checkbox" checked={needConsult} onChange={(e) => setNeedConsult(e.target.checked)} />
                            Нужна консультация
                        </label>
                        <button type="submit" className={styles.submit}>{editingId ? 'Сохранить' : 'Добавить'}</button>
                    </form>
                </div>)}
                <div className={styles.filtersRow}>
                    <FilterButtons
                        items={specializations}
                        selectedId={filterId}
                        onSelect={setFilterId}
                    />
                </div>
                <div className={styles.tableWrap}>
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
                        {shownServices.map((service) => (
                        <tr key={service.id}>
                        <td className={styles.td}>{service.name}</td>
                        <td className={styles.td}>от {Number(service.price_from).toLocaleString('ru-RU')} ₽</td>
                        <td className={styles.td}>{service.duration_min} мин</td>
                        <td className={styles.td}>{service.requires_consultation ? 'Да' : 'Нет'}</td>
                        <td className={styles.td}>
                            <div className={styles.rowActions}>
                                <button onClick={() => startEdit(service)} className="secondary">Изменить</button>
                                <button onClick={() => deleteService(service.id)} className="danger">Удалить</button>
                            </div>
                        </td>
                        </tr>
                        ))}
                    </tbody>
                </table>
                </div>
                {shownServices.length === 0 && (
                    <p className={styles.empty}>По этой специальности услуг нет.</p>
                )}
            </div>)}
            {section === 'cabinets' && <AdminCabinets />}
            {section === 'schedules' && <AdminSchedules />}
            {section === 'appointments' && <AdminAppointments />}
            {section === 'doctors' && <AdminDoctors />}
            </div>
        </div>
    )
}
export default AdminPage;