import FilterButtons from '../../components/FilterButtons/FilterButtons';
import { getJson } from '../../api/client';
import styles from './DoctorPage.module.css';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { plural } from '../../utils/plural';
import { initials } from '../../utils/initials';


function DoctorsPage() {
    const [selectedId, setSelectedId] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const { role } = useAuth();
    const canBook = role !== 'doctor' && role !== 'admin';

    const [doctors, setDoctors] = useState([]);
    useEffect(() => {
      getJson('/api/v1/doctors/')
      .then((data) => setDoctors(data))
      .catch(() => setError('Не удалось загрузить врачей'))
      .finally(() => setIsLoading(false));
    }, []);

    const [specializations, setSpecializations] = useState([]);
    useEffect(() => {
      getJson('/api/v1/specializations/')
      .then((data) => setSpecializations(data));
    }, []);

    const shownDoctors = doctors.filter((doctor) => selectedId === null  || doctor.specializations.some((s) => s.specialization.id === selectedId));

   if (isLoading) {
    return <p>Загрузка…</p>;
  }

  if (error) {
  return <p>{error}</p>;
  }
  return (
    <div className={styles.page}>
      <h1>Наши врачи</h1>
      <FilterButtons items={specializations} selectedId={selectedId} onSelect={setSelectedId} />
      <div className={styles.grid}>
      {shownDoctors.map((doctor) => (
        <div key={doctor.user_id} className={styles.card}>
          {doctor.photo_url ? <img src={doctor.photo_url} alt={doctor.user.full_name} className={styles.photo} /> : <div className={styles.photo}>{initials(doctor.user.full_name)}</div>}
          <p className={styles.name} >{doctor.user.full_name}</p>
          <p className={styles.specialization} >{doctor.specializations.map((s) => s.specialization.name).join(', ')}</p>
          <p className={styles.experience} >Стаж {doctor.experience_years} {plural(doctor.experience_years, 'год', 'года', 'лет')}</p>
          <p className={styles.bio} >{doctor.bio}</p>
          {canBook && <Link to="/booking" className={styles.bookButton}>Записаться к врачу</Link>}
        </div>
      ))}
      </div>
    </div>
  )
}

export default DoctorsPage;