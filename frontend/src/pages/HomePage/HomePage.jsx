import styles from './HomePage.module.css';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function HomePage() {
  const { role } = useAuth();
  const canBook = role !== 'doctor' && role !== 'admin';
  return (
    <section className={styles.hero}>
      <div className={styles.text}>
        <span className={styles.badge}>Онлайн-запись 24/7</span>
        <h1 className={styles.title}>Запишитесь к стоматологу онлайн</h1>
        <p className={styles.subtitle}>Выберите услугу, врача и свободное время. Без звонков в регистратуру.</p>
        {canBook && (
        <div className={styles.actions}>
          <Link to="/booking" className={styles.primary}>Записаться на приём</Link>
          <Link to="/booking" className={styles.urgent}>Острая боль</Link>
        </div>
        )}
      </div>
      <div className={styles.photo}>
        Здесь будет фото клиники
      </div>
    </section>
  );
}

export default HomePage;