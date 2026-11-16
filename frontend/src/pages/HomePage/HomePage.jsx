import styles from './HomePage.module.css';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useState, useEffect } from 'react';
import { getJson } from '../../api/client';
import { plural } from '../../utils/plural';

const steps = [
  { title: 'Выберите услугу', text: 'Осмотр, лечение, гигиена или срочный приём при острой боли.' },
  { title: 'Выберите врача и время', text: 'Мастер записи сам подскажет ближайшее свободное время.' },
  { title: 'Приходите на приём', text: 'Запись появится в личном кабинете. Отменить онлайн можно не позднее чем за сутки.' },
];
function HomePage() {
  const { role } = useAuth();
  const canBook = role !== 'doctor' && role !== 'admin';
  const [services, setServices] = useState([]);
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    getJson('/api/v1/services/')
      .then((data) => setServices(data))
      .catch(() => { });
  }, []);
  useEffect(() => {
    getJson('/api/v1/doctors/')
      .then((data) => setDoctors(data))
      .catch(() => { });
  }, []);

  const popular = services
    .filter((s) => !s.requires_consultation && s.name !== 'Острая боль')
    .slice(0, 3);
  const popularDoc = doctors
    .slice(0, 3);
  return (
    <div className={styles.page}>
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
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Как записаться</h2>
        <ol className={styles.steps}>
          {steps.map((step, index) => (
            <li key={step.title} className={styles.step}>
              <span className={styles.stepNumber}>{index + 1}</span>
              <h3 className={styles.stepTitle}>{step.title}</h3>
              <p className={styles.stepText}>{step.text}</p>
            </li>
          ))}
        </ol>
      </section>
      {popular.length > 0 && (
        <section className={styles.section}>
          <div className={styles.sectionHead}>
            <h2 className={styles.sectionTitle}>Популярные услуги</h2>
            <Link to="/services" className={styles.moreLink}>Все услуги</Link>
          </div>
          <div className={styles.cards}>
            {popular.map((service) => (
              <div key={service.id} className={styles.card}>
                <h3 className={styles.cardTitle}>{service.name}</h3>
                <p className={styles.cardMeta}>{service.duration_min} мин</p>
                <p className={styles.cardPrice}>от {Number(service.price_from).toLocaleString('ru-RU')} ₽</p>
                {canBook && (
                  <Link to="/booking" state={{ serviceId: service.id }} className={styles.cardButton}>Записаться</Link>
                )}
              </div>
            ))}
          </div>
        </section>
      )}
      {popularDoc.length > 0 && (
        <section className={styles.section}>
          <div className={styles.sectionHead}>
            <h2 className={styles.sectionTitle}>Наши врачи</h2>
            <Link to="/doctors" className={styles.moreLink}>Все врачи</Link>
          </div>
          <div className={styles.cards}>
            {popularDoc.map((doctor) => (
              <div key={doctor.user_id} className={styles.card}>
                <div className={styles.doctorPhoto}>Фото врача</div>
                <h3 className={styles.cardTitle} >{doctor.user.full_name}</h3>
                <p className={styles.cardSpec} >{doctor.specializations.map((s) => s.specialization.name).join(', ')}</p>
                <p className={styles.cardMeta} >Стаж {doctor.experience_years} {plural(doctor.experience_years, 'год', 'года', 'лет')}</p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default HomePage;