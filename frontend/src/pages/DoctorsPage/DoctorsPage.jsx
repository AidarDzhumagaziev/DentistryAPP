import FilterButtons from '../../components/FilterButtons/FilterButtons';
import styles from './DoctorPage.module.css';
import { useState, useEffect } from 'react';


function DoctorsPage() {
    const [selectedId, setSelectedId] = useState(null);
    
    const [doctors, setDoctors] = useState([]);
    useEffect(() => {
      fetch('/api/v1/doctors/')
      .then((response) => response.json())
      .then((data) => setDoctors(data));
    }, []);

    const [specializations, setSpecializations] = useState([]);
    useEffect(() => {
      fetch('/api/v1/specializations/')
      .then((response) => response.json())
      .then((data) => setSpecializations(data));
    }, []);

    const shownDoctors = doctors.filter((doctor) => selectedId === null  || doctor.specializations.some((s) => s.id === selectedId));
  return (
    <div className={styles.page}>
      <h1>Наши врачи</h1>
      <FilterButtons items={specializations} selectedId={selectedId} onSelect={setSelectedId} />
      <div className={styles.grid}>
      {shownDoctors.map((doctor) => (
        <div key={doctor.user_id} className={styles.card}>
          <div className={styles.photo}>Фото врача</div>
          <p className={styles.name} >{doctor.user.full_name}</p>
          <p className={styles.specialization} >{doctor.specializations.map((s) => s.name).join(', ')}</p>
          <p className={styles.experience} >Стаж {doctor.experience_years} лет</p>
          <p className={styles.bio} >{doctor.bio}</p>
        </div>
      ))}
      </div>
    </div>
  )
}

export default DoctorsPage;