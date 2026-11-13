import {mockDoctorAppointments, statusNames} from '../../data/mockAppointments';
import {useState} from 'react';
import styles from './DoctorCabinetPage.module.css';

function formatDate(d) {
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${month}-${day}`;
}

function DoctorCabinetPage() {
    const [appointments, setAppointments] = useState(mockDoctorAppointments);
    const [day, setDay] = useState(formatDate(new Date()));
    const dayAppointments = appointments.filter((a) => a.start.slice(0, 10) === day);

    function shiftDay(offset){
        const d = new Date(day);
        d.setDate(d.getDate() + offset);
        return setDay(formatDate(d));
        }
    

        function changeStatus(id, newStatus){
            setAppointments(appointments.map((a) =>
            a.id === id ? { ...a, status: newStatus } : a
            ));
        }
        return(
        <div>
            <div className={styles.top}>
                <h1>Приёмы на {new Date(day).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}</h1>
                <div className={styles.arrows}>
                    <button className={styles.arrow} onClick={() => shiftDay(-1)}>‹</button>
                    <input className={styles.dateInput} type="date" value={day} onChange={(e) => {
                        setDay(e.target.value);}}/>
                    <button className={styles.arrow} onClick={() => shiftDay(1)}>›</button>
                </div>
            </div>
            {dayAppointments.length === 0 && <p>Приёмов нет</p>}
            <div className={styles.list}>
                {dayAppointments.map((appointment)=>(
                <div key={appointment.id} className={styles.row}>
                    <div className={styles.timeBox}>
                        <span className={styles.time}>{appointment.start.slice(11, 16)}</span>
                        <span className={styles.duration}>{appointment.duration} мин</span>
                    </div>
                    <div className={styles.info}>
                        <span className={styles.patient}>{appointment.patient}</span>
                        <span className={styles.service}>{appointment.service}</span>
                        <span className={styles.service}>кабинет {appointment.cabinet}</span>
                        <div className={styles.tags}>
                            <span className={`${styles.status} ${styles[appointment.status]}`}>{statusNames[appointment.status]}</span>
                            {appointment.alert && <span className={styles.alert}>{appointment.alert}</span>}
                        </div>


                    </div>
                    <div className={styles.actions}>
                        {(appointment.status === 'scheduled') && <button onClick={() => changeStatus(appointment.id, 'confirmed')}>Подтвердить</button>}
                        {(appointment.status === 'confirmed') && <button onClick={() => changeStatus(appointment.id, 'completed')}>Завершить</button>}
                        {(appointment.status === 'scheduled' || appointment.status === 'confirmed') && <button className="danger" onClick={() => changeStatus(appointment.id, 'no_show')}>Неявка</button>}
                    </div>
                </div>
                ))}
            </div>
        </div>
        )
}
export default DoctorCabinetPage;