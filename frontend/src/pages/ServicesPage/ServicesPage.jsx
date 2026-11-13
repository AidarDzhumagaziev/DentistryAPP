import FilterButtons from '../../components/FilterButtons/FilterButtons';
import { getJson } from '../../api/client';
import styles from './ServicesPage.module.css';
import { useState, useEffect} from 'react';
import { Link } from 'react-router-dom';

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
  const urgentServices = shownServices.filter((s) => s.name === 'Острая боль');
  const otherServices = shownServices.filter((s) => s.name !== 'Острая боль');
  const sortedServices = [...urgentServices, ...otherServices];
  
  if (isLoading) {
    return <p>Загрузка…</p>;
  }

  if (error) {
  return <p>{error}</p>;
  }

  function getSpecName(id) {
  const spec = specializations.find((s) => s.id === id);
  return spec ? spec.name : '';
}
  return (
    <div className={styles.page}>
      <h1>Услуги и цены</h1>
      <FilterButtons items={specializations} selectedId={selectedId} onSelect={setSelectedId} />
      <div className={styles.grid}>
      {sortedServices.map((service) => (
        <div key={service.id} className={service.name === 'Острая боль' ? `${styles.card} ${styles.urgent}` : styles.card}>
          <div className={styles.cardTop}>
            <p className={styles.name} >{service.name}</p>
            <span className={styles.duration}>{service.duration_min} мин</span>
          </div>
          <p className={styles.description}>{service.description}</p>
          <span className={styles.spec}>{getSpecName(service.specialization_id)}</span>
          {service.requires_consultation && <span className={styles.consult}>Сначала нужна консультация</span>}
          <div className={styles.cardBottom}>
            <p className={styles.price} >от {Number(service.price_from).toLocaleString('ru-RU')} ₽</p>
            <Link to="/booking" className={service.name === 'Острая боль' ? `${styles.bookButton} ${styles.urgentButton}` : styles.bookButton}>Записаться</Link>
          </div>
        </div>
      ))}
      </div>
    </div>
  );
}

export default ServicesPage;