import { services } from '../../data/services'
import { specializations } from '../../data/specializations'
import styles from './ServicesPage.module.css';
import { useState } from 'react'


function ServicesPage() {
  const [selectedId, setSelectedId] = useState(null);
  function getFilterClass(id) {
    if (id === selectedId) {
    return `${styles.filter} ${styles.active}`;
    }
    return styles.filter
  }
  const shownServices = services.filter((service) => selectedId === null  || selectedId === service.specialization_id);
  return (
    <div className={styles.page}>
      <h1>Услуги и цены</h1>
      <div className={styles.filters}>
        <button className={getFilterClass(null)}  onClick={() => setSelectedId(null)}>Все</button>
         {specializations.map((specialization) => (
          <button className={getFilterClass(specialization.id)} key={specialization.id}  onClick={() => setSelectedId(specialization.id)} >{specialization.name}</button>
      ))}
      </div>
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