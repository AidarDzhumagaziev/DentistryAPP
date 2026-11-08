import FilterButtons from '../../components/FilterButtons/FilterButtons';
import styles from './ServicesPage.module.css';
import { useState, useEffect } from 'react';


function ServicesPage() {
  const [selectedId, setSelectedId] = useState(null);

  const [services, setServices] = useState([]);
  useEffect(() => {
  fetch('/api/v1/services/')
    .then((response) => response.json())
    .then((data) => setServices(data));
}, []);

  const [specializations, setSpecializations] = useState([]);
    useEffect(() => {
      fetch('/api/v1/specializations/')
      .then((response) => response.json())
      .then((data) => setSpecializations(data));
    }, []);
    
  const shownServices = services.filter((service) => selectedId === null  || selectedId === service.specialization_id);
  return (
    <div className={styles.page}>
      <h1>Услуги и цены</h1>
      <FilterButtons items={specializations} selectedId={selectedId} onSelect={setSelectedId} />
      <div className={styles.grid}>
      {shownServices.map((service) => (
        <div key={service.id} className={styles.card}>
          <p className={styles.name} >{service.name}</p>
          <p className={styles.price} >от {service.price_from} ₽</p>
        </div>
      ))}
      </div>
    </div>
  );
}

export default ServicesPage;