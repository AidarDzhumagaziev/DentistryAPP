import { useState, useEffect } from 'react';
import styles from './BookingPage.module.css';
import { Link, useLocation } from 'react-router-dom';
import { getJson, authFetch } from '../../api/client';

function formatDate(d) {
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${month}-${day}`;
}

const stepNames = ['Услуга', 'Врач', 'Дата и время', 'Подтверждение'];
const HALF_YEAR_MS = 183 * 24 * 60 * 60 * 1000;
const CONSULTATION_NAME = 'Осмотр и консультация';

function hasConsultationIn(appointments) {
    return appointments.some((a) =>
        a.status === 'completed' &&
        a.service.name === CONSULTATION_NAME &&
        Date.now() - new Date(a.starts_at) < HALF_YEAR_MS
    );
}

function BookingPage(){
    const location = useLocation();
    const presetServiceId = location.state && location.state.serviceId ? location.state.serviceId : null;
    const [step, setStep] = useState(presetServiceId ? 2 : 1);
    const [serviceId, setServiceId] = useState(presetServiceId);
    const [doctorId, setDoctorId] = useState(null);
    const [services, setServices] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [date, setDate] = useState('');
    const [slots, setSlots] = useState([]);
    const [slotStart, setSlotStart] = useState(null);
    const [myAppointments, setMyAppointments] = useState([]);

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
    function getStepClass(number){
        if (number === step){
            return `${styles.stepPill} ${styles.current}`
        }
        if (number < step){
            return `${styles.stepPill} ${styles.done}`
        }
        return styles.stepPill
    }

    function getCardClass(id,selectedId) {
        if (id === selectedId) {
            return `${styles.card} ${styles.selected}`;
            }
            return styles.card;
        }

    useEffect(() => {
        Promise.all([
            getJson('/api/v1/services/'),
            authFetch('/api/v1/appointments/me/')
            .then((r) => (r.ok ? r.json() : [])),
        ])
        .then(([servicesData, myData]) => {
            setServices(servicesData);
            setMyAppointments(myData);

            const preset = servicesData.find((s) => s.id === presetServiceId);
            if (preset && preset.requires_consultation && !hasConsultationIn(myData)) {
                setServiceId(null);
                setStep(1);
            }
        });
    }, [presetServiceId]);

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
    const suitableDoctors = doctors.filter((doctor) => selectedService && doctor.specializations.some((s) => s.specialization.id === selectedService.specialization_id))
    const hasConsultation = hasConsultationIn(myAppointments);

    function isLocked(service) {
        return service.requires_consultation && !hasConsultation;
    }

    const consultationService = services.find((s) => s.name === CONSULTATION_NAME);
    return(
        <div className={styles.page}>
            <h1>Запись</h1>
            <div className={styles.steps}>{stepNames.map((name, index) => ( 
                <span key={name} className={getStepClass(index + 1)}>{index + 1}. {name}</span>  
                    
            ))}
            </div>
            <div className={styles.layout}>
            <section className={styles.main}>
                {(step === 1) && <h2>Выберите услугу</h2>}
                {(step === 1) && consultationService && services.some(isLocked) && (
                <div className={styles.notice}>
                    <span>{services.filter(isLocked).map((s) => s.name).join(', ')} — только после осмотра.</span>
                    <button
                        type="button"
                        className={styles.noticeButton}
                        onClick={() => {
                            setServiceId(consultationService.id);
                            setDoctorId(null);
                            setSlotStart(null);
                            setStep(2);
                        }}
                    >
                        Записаться на осмотр
                    </button>
                </div>
                )}
                {(step === 1) && 
                <div className={styles.grid}>
                    {services.map((service) => (
                        <button key={service.id} disabled={isLocked(service)} className={getCardClass(service.id,serviceId)} 
                            onClick={() => {
                                setServiceId(service.id);
                                setDoctorId(null);
                                setSlotStart(null);
                            }} >
                            <span className={styles.name} >{service.name}</span>
                            <span className={styles.price} >от {Number(service.price_from).toLocaleString('ru-RU')} ₽</span>
                            {isLocked(service) && <span className={styles.lockHint}>Сначала нужен осмотр</span>}
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
                            <span className={styles.specialization} >{doctor.specializations.map((s) => s.specialization.name).join(', ')}</span>
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
                        <label className={styles.field}>
                            Комментарий для врача (необязательно)
                            <textarea rows="3" placeholder="Например: болит зуб слева внизу" className={styles.textarea} />
                        </label>
                        <p className={styles.note}>Отменить запись онлайн можно не позднее чем за 24 часа.</p>
                    </div>
                }
                {(step === 5) && <div className={styles.doneScreen}>
                    <h2>Вы записаны</h2>
                    <p>Напоминание придёт накануне приёма.</p>
                    <Link to="/account" className={styles.doneLink}>Перейти к моим записям</Link>
                </div>}
                <div className={styles.actions}>
                    {(step > 1 && step < 5) && <button className={styles.secondary} onClick={() => setStep(step - 1)}>Назад</button>}
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
                     {(step === 4) && <button onClick={() => setStep(5)}>Записаться</button>}
                </div>
            </section>
            <aside className={styles.summary}>
                <h3>Ваша запись</h3>
                <div className={styles.confirm}>
                        <div className={styles.confirmRow}>
                            <span className={styles.label}>Услуга</span>
                            <span className={styles.value}>{selectedService ? selectedService.name : '—'}</span>
                        </div>
                        <div className={styles.confirmRow}>
                            <span className={styles.label}>Врач</span>
                            <span className={styles.value} >{selectedDoctor ? selectedDoctor.user.full_name : '—'}</span>
                        </div>
                        <div className={styles.confirmRow}>
                            <span className={styles.label}>Дата</span>
                            <span className={styles.value} >{date ? new Date(date).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' }) : '—'}</span>
                        </div>
                        <div className={styles.confirmRow}>
                            <span className={styles.label} >Время</span>
                            <span className={styles.value} >{slotStart ?slotStart.slice(11, 16) : '—'}</span>
                        </div>
                        <div className={styles.confirmRow}>
                            <span className={styles.label} >Стоимость</span>
                            <span className={styles.value} >{selectedService ? `от ${Number(selectedService.price_from).toLocaleString('ru-RU')} ₽` : '—'}</span>
                        </div>
                    </div>
            </aside>
            </div>
        </div>
    )
}
export default BookingPage;