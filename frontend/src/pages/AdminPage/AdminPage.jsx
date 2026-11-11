import { getJson } from '../../api/client';
import styles from './AdminPage.module.css';
import { useState, useEffect } from 'react';

function AdminPage(){
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [services, setServices] = useState([]);

      useEffect(() => {
      getJson('/api/v1/services/')
      .then((data) => setServices(data))
      .catch(() => setError('Не удалось загрузить услуги'))
      .finally(() => setIsLoading(false));
    }, []);

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
                    </tr>
                </thead>
                <tbody>
                    {services.map((service) => (
                    <tr key={service.id}>
                    <td className={styles.td}>{service.name}</td>
                    <td className={styles.td}>от {Number(service.price_from).toLocaleString('ru-RU')} ₽</td>
                    <td className={styles.td}>{service.duration_min} мин</td>
                    <td className={styles.td}>{service.requires_consultation ? 'Да' : 'Нет'}</td>
                    </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
export default AdminPage;