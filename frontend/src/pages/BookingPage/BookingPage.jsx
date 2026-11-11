import { useState, useEffect } from 'react';
import styles from './BookingPage.module.css';
import { getJson } from '../../api/client';



function BookingPage(){
    const [step, setStep] = useState(1);
    const [serviceId, setServiceId] = useState(null);
    const [doctorId, setDoctorId] = useState(null);
    const [services, setServices] = useState([]);
    const [doctors, setDoctors] = useState([]);

    function getCardClass(id,selectedId) {
        if (id === selectedId) {
            return `${styles.card} ${styles.selected}`;
        }
            return styles.card;
        }

    useEffect(() => {
        getJson('/api/v1/services/')
        .then((data) => setServices(data))
    }, []);

    useEffect(() => {
      getJson('/api/v1/doctors/')
      .then((data) => setDoctors(data))
    }, []);

    const selectedService = services.find((s)=> s.id === serviceId);
    const suitableDoctors = doctors.filter((doctor) => selectedService && doctor.specializations.some((s) => s.id === selectedService.specialization_id))
    return(
        <>
            <h1>Запись</h1>
            <div>Шаг {step} из 4</div>

            {(step === 1) && <h2>Выберите услугу</h2>}
            {(step === 1) && 
            <div className={styles.grid}>
                {services.map((service) => (
                    <button key={service.id} className={getCardClass(service.id,serviceId)} onClick={() => setServiceId(service.id)} >
                        <span className={styles.name} >{service.name}</span>
                        <span className={styles.price} >от {Number(service.price_from).toLocaleString('ru-RU')} ₽</span>
                    </button>
                ))}
            </div>
            }
            {(step === 2) && <h2>Выберите врача</h2>}
            {(step === 2) && 
            <div className={styles.grid}>
                {suitableDoctors.map((doctor) => (
                    <button key={doctor.user_id} className={getCardClass(doctor.user_id, doctorId)} onClick={() => setDoctorId(doctor.user_id)} >
                        <span className={styles.name} >{doctor.user.full_name}</span>
                        <span className={styles.specialization} >{doctor.specializations.map((s) => s.name).join(', ')}</span>
                        <span className={styles.experience} >Стаж {doctor.experience_years} лет</span>
                        <span className={styles.bio} >{doctor.bio}</span>
                    </button>
                ))}
            </div>
            }



            {(step === 3) && <h2>Выберите дату и время</h2>}
            {(step === 4) && <h2>Подтверждение</h2>}

            {(step <4) && <button onClick={() =>setStep(step+1)} disabled={(step === 1 && serviceId === null) || (step === 2 && doctorId === null)}>Далее</button>}
            {(step >1) && <button onClick={() =>setStep(step-1)}>Назад</button>}
         
        </>
    )
}
export default BookingPage;