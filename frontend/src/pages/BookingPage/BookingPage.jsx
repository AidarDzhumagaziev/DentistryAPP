import { useState, useEffect } from 'react';
import styles from './BookingPage.module.css';
import { getJson } from '../../api/client';

function formatDate(d) {
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${month}-${day}`;
}

function BookingPage(){
    const [step, setStep] = useState(1);
    const [serviceId, setServiceId] = useState(null);
    const [doctorId, setDoctorId] = useState(null);
    const [services, setServices] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [date, setDate] = useState('');
    const [slots, setSlots] = useState([]);
    const [slotStart, setSlotStart] = useState(null);

    function findNearestDate(offset){
        if (offset > 14){
            return 
        }
        const d = new Date();
        d.setDate(d.getDate() + offset);
        const day = formatDate(d);
            getJson(`/api/v1/slots/?service_id=${serviceId}&doctor_id=${doctorId}&date=${day}`)
            .then((data) => {
            if (data.length > 0){
                return setDate(day)
            }
            else return findNearestDate(offset + 1)
        })
    }


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

    useEffect(() => {
        if (!date) return;

        getJson(`/api/v1/slots/?service_id=${serviceId}&doctor_id=${doctorId}&date=${date}`)
        .then((data) => setSlots(data))
    }, [serviceId, doctorId, date]);

    const selectedService = services.find((s)=> s.id === serviceId);
    const selectedDoctor = doctors.find((s)=> s.user_id === doctorId);
    const suitableDoctors = doctors.filter((doctor) => selectedService && doctor.specializations.some((s) => s.id === selectedService.specialization_id))
    return(
        <div className={styles.page}>
            <h1>Запись</h1>
            <div className={styles.stepLabel}>Шаг {step} из 4</div>

            {(step === 1) && <h2>Выберите услугу</h2>}
            {(step === 1) && 
            <div className={styles.grid}>
                {services.map((service) => (
                    <button key={service.id} className={getCardClass(service.id,serviceId)} 
                        onClick={() => {
                            setServiceId(service.id);
                            setDoctorId(null);
                            setSlotStart(null);
                        }} >
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
                    <button key={doctor.user_id} className={getCardClass(doctor.user_id, doctorId)}
                        onClick={() => {
                           setDoctorId(doctor.user_id);
                           setSlotStart(null);}
                        }>
                        <span className={styles.name} >{doctor.user.full_name}</span>
                        <span className={styles.specialization} >{doctor.specializations.map((s) => s.name).join(', ')}</span>
                        <span className={styles.experience} >Стаж {doctor.experience_years} лет</span>
                        <span className={styles.bio} >{doctor.bio}</span>
                    </button>
                ))}
            </div>
            }



            {(step === 3) && <h2>Выберите дату и время</h2>}
            {(step === 3) && <input type="date" value={date} 
                onChange={(e) => {
                    setDate(e.target.value);
                    setSlotStart(null);
                }}/>
            }
            {(step === 3) &&
                <div className={styles.timegrid}>
                    {slots.map((slot) => (
                        <button key={slot.start} className={getCardClass(slot.start, slotStart)} onClick={() => setSlotStart(slot.start)}>
                            {slot.start.slice(11, 16)}
                        </button>
                    ))}
                </div>
            } 
            {(step === 3 && date && slots.length === 0) && <p>На эту дату нет свободного времени</p>}


            {(step === 4) && <h2>Подтверждение</h2>}
            {(step === 4) && 
                <div className={styles.confirm}>
                    <span className={styles.name} >{selectedService.name}</span>
                    <span className={styles.price} >от {Number(selectedService.price_from).toLocaleString('ru-RU')} ₽</span>
                    <span className={styles.name} >{selectedDoctor.user.full_name}</span>
                    <span className={styles.specialization} >{selectedDoctor.specializations.map((s) => s.name).join(', ')}</span>
                    <span className={styles.experience} >Стаж {selectedDoctor.experience_years} лет</span>
                    <span className={styles.date} >{new Date(date).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}</span>
                    <span className={styles.slot} >{slotStart.slice(11, 16)}</span>
                    <button>Записаться</button>
                </div>
            }

            <div className={styles.actions}>
                {(step > 1) && <button className={styles.secondary} onClick={() => setStep(step - 1)}>Назад</button>}
                {(step < 4) && (
                    <button
                        onClick={() => {
                            if (step === 2) {
                                findNearestDate(0);
                            }
                            setStep(step + 1);
                        }}
                        disabled={(step === 1 && serviceId === null) || (step === 2 && doctorId === null) || (step === 3 && slotStart === null)}
                    >
                        Далее
                    </button>
                )}
            </div>
         
        </div>
    )
}
export default BookingPage;