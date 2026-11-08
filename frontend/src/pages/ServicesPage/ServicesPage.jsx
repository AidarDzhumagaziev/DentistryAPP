import FilterButtons from '../../components/FilterButtons/FilterButtons';
import { getJson } from '../../api/client';
import styles from './ServicesPage.module.css';
import { useState, useEffect } from 'react';


function ServicesPage() {
  
  const [selectedId, setSelectedId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const [services, setServices] = useState([]);
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

  const shownServices = services.filter((service) => selectedId === null  || selectedId === service.specialization_id);

  if (isLoading) {
    return <p>Загрузка…</p>;
  }

  if (error) {
  return <p>{error}</p>;
  }
  return (
    <div className={styles.page}>
      <h1>Услуги и цены</h1>
      <FilterButtons items={specializations} selectedId={selectedId} onSelect={setSelectedId} />
      <div className={styles.grid}>
      {shownServices.map((service) => (
        <div key={service.id} className={styles.card}>
          <p className={styles.name} >{service.name}</p>
          <p className={styles.price} >от {Number(service.price_from).toLocaleString('ru-RU')} ₽</p>
        </div>
      ))}
      </div>
    </div>
  );
}

export default ServicesPage;