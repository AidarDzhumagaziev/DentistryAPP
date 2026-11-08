import FilterButtons from '../../components/FilterButtons/FilterButtons';
import { doctors } from '../../data/doctors'
import { specializations } from '../../data/specializations'
import styles from './DoctorPage.module.css';
import { useState } from 'react'


function DoctorsPage() {
    const [selectedId, setSelectedId] = useState(null);
    function getSpecializationName(id) {
      const specialization = specializations.find((s) => s.id === id);
      return specialization.name;
    }
    const shownDoctors = doctors.filter((doctor) => selectedId === null  || selectedId === doctor.specialization_id);
  return (
    <div className={styles.page}>
      <h1>Наши врачи</h1>
      <FilterButtons items={specializations} selectedId={selectedId} onSelect={setSelectedId} />
      <div className={styles.grid}>
      {shownDoctors.map((doctor) => (
        <div key={doctor.id} className={styles.card}>
          <div className={styles.photo}>Фото врача</div>
          <p className={styles.name} >{doctor.name}</p>
          <p className={styles.specialization} >{getSpecializationName(doctor.specialization_id)}</p>
          <p className={styles.experience} >Стаж {doctor.experience_years} лет</p>
          <p className={styles.bio} >{doctor.bio}</p>
        </div>
      ))}
      </div>
    </div>
  )
}

export default DoctorsPage;