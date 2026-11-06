import { services } from '../../data/services'
import styles from './ServicesPage.module.css';

function ServicesPage() {
  return (
    <>
      <h1>Услуги и цены</h1>
      <div className={styles.grid}>
      {services.map((service) => (
        <div key={service.id} className={styles.card}>
          <p className={styles.name} >{service.name}</p>
          <p className={styles.price} >от {service.price_from} ₽</p>
        </div>
      ))}
      </div>
    </>
  );
}

export default ServicesPage;