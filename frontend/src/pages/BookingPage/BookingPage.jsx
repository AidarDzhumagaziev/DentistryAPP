import { useState, useEffect } from 'react';
import styles from './BookingPage.module.css';
import { Link, useLocation } from 'react-router-dom';
import { getJson, authFetch } from '../../api/client';
import { CLINIC } from '../../data/clinic';
import HealthForm from '../../components/HealthForm/HealthForm';

function formatDate(d) {
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${month}-${day}`;
}

function addMinutes(start, minutes) {
    const d = new Date(start);
    d.setMinutes(d.getMinutes() + minutes);
    return d.toISOString();
}

const stepNames = ['Услуга', 'Врач', 'Дата и время', 'Подтверждение'];

function hasConsultationFor(service, services, appointments) {
    const consultation = services.find((s) => s.is_consultation && s.specialization_id === service.specialization_id);
    if (!consultation) {
        return false;
    }
    return appointments.some((a) => a.service.id === consultation.id && a.status !== 'cancelled');
}

const bookingErrors = {
    'CONSULTATION_REQUIRED': 'Сначала нужна консультация врача этой специальности.',
    'Slot is already booked': 'Это время уже заняли. Выберите другое.',
    'Patient has appointment in this diaposon': 'У вас уже есть запись на это время. Выберите другое.',
};

function BookingPage() {
    const location = useLocation();
    const presetServiceId = location.state && location.state.serviceId ? location.state.serviceId : null;
    const presetDoctorId = location.state && location.state.doctorId ? location.state.doctorId : null;
    const [step, setStep] = useState(presetServiceId ? 2 : 1);
    const [serviceId, setServiceId] = useState(presetServiceId);
    const [doctorId, setDoctorId] = useState(presetDoctorId);
    const [services, setServices] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [date, setDate] = useState('');
    const [slots, setSlots] = useState([]);
    const [slotStart, setSlotStart] = useState(null);
    const [myAppointments, setMyAppointments] = useState([]);
    const [isSending, setIsSending] = useState(false);
    const [bookingError, setBookingError] = useState(null);
    const [isSearching, setIsSearching] = useState(false);
    const [days, setDays] = useState([]);
    const [hasProfile, setHasProfile] = useState(true);

    function loadDays() {
        const dates = [];
        for (let i = 0; i < 14; i++) {
            const d = new Date();
            d.setDate(d.getDate() + i);
            dates.push(formatDate(d));
        }
        const requests = dates.map((day) =>
            getJson(`/api/v1/slots/?service_id=${serviceId}&doctor_id=${doctorId}&date=${day}`)
        );
        Promise.all(requests)
            .then((results) => {
                const list = dates.map((day, i) => ({ date: day, free: results[i].length > 0 }));
                setDays(list);
                const first = list.find((d) => d.free);
                if (first) {
                    setDate(first.date);
                }
            })
            .catch(() => setDays([]))
            .finally(() => setIsSearching(false));
    }
    function submitBooking() {
        setIsSending(true);
        setBookingError(null);

        authFetch('/api/v1/appointments/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                doctor_id: doctorId,
                service_id: serviceId,
                starts_at: slotStart,
                ends_at: addMinutes(slotStart, selectedService.duration_min),
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((body) => {
                        const code = typeof body.detail === 'object' ? body.detail.code : body.detail;
                        throw new Error(code);
                    });
                }
                setStep(5);
            })
            .catch((err) => setBookingError(
                bookingErrors[err.message] || `Не удалось записаться. Проверьте, заполнена ли анкета, или позвоните в клинику: ${CLINIC.phone}.`
            ))
            .finally(() => setIsSending(false));
    }
    function saveProfileAndBook(values) {
        setBookingError(null);
        authFetch('/api/v1/patients/me/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(values),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Сервер ответил ошибкой');
                }
                setHasProfile(true);
                submitBooking();
            })
            .catch(() => setBookingError('Не удалось сохранить анкету. Попробуйте ещё раз.'));
    }
    function getStepClass(number) {
        if (number === step) {
            return `${styles.stepPill} ${styles.current}`
        }
        if (number < step) {
            return `${styles.stepPill} ${styles.done}`
        }
        return styles.stepPill
    }

    function getCardClass(id, selectedId) {
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
            authFetch('/api/v1/patients/me/').then((r) => r.ok),
        ])
            .then(([servicesData, myData, profileOk]) => {
                setServices(servicesData);
                setMyAppointments(myData);
                setHasProfile(profileOk);

                const preset = servicesData.find((s) => s.id === presetServiceId);

                if (preset && preset.requires_consultation && !hasConsultationFor(preset, servicesData, myData)) {
                    setServiceId(null);
                    setDoctorId(null);
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

    const selectedService = services.find((s) => s.id === serviceId);
    const selectedDoctor = doctors.find((s) => s.user_id === doctorId);
    const suitableDoctors = doctors.filter((doctor) => selectedService && doctor.specializations.some((s) => s.specialization.id === selectedService.specialization_id))

    function isLocked(service) {
        return service.requires_consultation && !hasConsultationFor(service, services, myAppointments);
    }

    const lockedService = services.find(isLocked);
    const consultationService = lockedService
        ? services.find((s) => s.is_consultation && s.specialization_id === lockedService.specialization_id)
        : null;

    return (
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
                            <span>Некоторые услуги доступны только после консультации врача.</span>
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
                            <span>Записаться на консультацию</span>
                            </button>
                        </div>
                    )}
                    {(step === 1) &&
                        <div className={styles.grid}>
                            {services.map((service) => (
                                <button key={service.id} disabled={isLocked(service)} className={getCardClass(service.id, serviceId)}
                                    onClick={() => {
                                        setServiceId(service.id);
                                        setDoctorId(null);
                                        setSlotStart(null);
                                    }} >
                                    <span className={styles.name} >{service.name}</span>
                                    <span className={styles.price} >от {Number(service.price_from).toLocaleString('ru-RU')} ₽</span>
                                    {isLocked(service) && <span className={styles.lockHint}>Сначала нужна консультация</span>}
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
                                        setSlotStart(null);
                                    }
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
                    {(step === 3 && !isSearching) && (
                        <div className={styles.days}>
                            {days.map((d) => (
                                <button
                                    key={d.date}
                                    type="button"
                                    disabled={!d.free}
                                    className={`${getCardClass(d.date, date)} ${styles.day}`}
                                    onClick={() => {
                                        setDate(d.date);
                                        setSlotStart(null);
                                    }}
                                >
                                    <span className={styles.weekday}>{new Date(d.date).toLocaleDateString('ru-RU', { weekday: 'short' })}</span>
                                    <span className={styles.dayNumber}>{Number(d.date.slice(8, 10))}</span>
                                </button>
                            ))}
                        </div>
                    )}
                    {(step === 3 && isSearching) && <p>Ищем ближайшее свободное время…</p>}
                    {(step === 3 && !isSearching && !date) && <p>В ближайшие две недели свободного времени нет. Выберите другого врача.</p>}
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
                            <p className={styles.note}>Отменить запись онлайн можно не позднее чем за 24 часа.</p>
                        </div>
                    }
                    {(step === 4 && !hasProfile) && (
                        <div className={styles.confirm}>
                            <p className={styles.note}>Перед первой записью заполните анкету здоровья — её увидит врач. Это нужно сделать один раз.</p>
                            <HealthForm submitLabel={isSending ? 'Записываем…' : 'Сохранить анкету и записаться'} onSave={saveProfileAndBook} />
                        </div>
                    )}
                    {(step === 5) && <div className={styles.doneScreen}>
                        <h2>Вы записаны</h2>
                        <p>Запись появилась в личном кабинете.</p>
                        <Link to="/account" className={styles.doneLink}>Перейти к моим записям</Link>
                    </div>}
                    {bookingError && <p className={styles.bookingError}>{bookingError}</p>}
                    <div className={styles.actions}>
                        {(step > 1 && step < 5) && <button className={styles.secondary} onClick={() => setStep(step - 1)}>Назад</button>}
                        {(step < 4) && (
                            <button
                                onClick={() => {
                                    if (step === 2) {
                                        setDate('');
                                        setSlots([]);
                                        setIsSearching(true);
                                        loadDays();
                                    }
                                    setStep(step + 1);
                                }}
                                disabled={(step === 1 && serviceId === null) || (step === 2 && doctorId === null) || (step === 3 && slotStart === null)}
                            >
                                Далее
                            </button>
                        )}
                        {(step === 4 && hasProfile) && (
                            <button onClick={submitBooking} disabled={isSending}>
                                {isSending ? 'Записываем…' : 'Записаться'}
                            </button>
                        )}
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
                            <span className={styles.value} >{slotStart ? slotStart.slice(11, 16) : '—'}</span>
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