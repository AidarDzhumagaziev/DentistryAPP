import { mockAppointments, statusNames } from '../../data/mockAppointments';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './AccountPage.module.css';

function getDay(start) {
    return new Date(start).getDate();
}

function getMonth(start) {
    return new Date(start).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' }).split(' ')[1];
}

function AccountPage() {
    const [appointments, setAppointments] = useState(mockAppointments);

    function cancel(id) {
        setAppointments(appointments.map((a) =>
            a.id === id ? { ...a, status: 'cancelled' } : a
        ));
    }

    return (
        <div>
            <div className={styles.top}>
                <h1>Личный кабинет</h1>
                <Link to="/booking" className={styles.newButton}>Новая запись</Link>
            </div>

            <div className={styles.list}>
                {appointments.map((appointment) => (
                    <div key={appointment.id} className={styles.row}>
                        <div className={styles.dateBox}>
                            <span className={styles.day}>{getDay(appointment.start)}</span>
                            <span className={styles.month}>{getMonth(appointment.start)}</span>
                            <span className={styles.time}>{appointment.start.slice(11, 16)}</span>
                        </div>

                        <div className={styles.info}>
                            <span className={styles.service}>{appointment.service}</span>
                            <span className={styles.doctor}>{appointment.doctor}</span>
                            <span className={`${styles.status} ${styles[appointment.status]}`}>
                                {statusNames[appointment.status]}
                            </span>
                        </div>

                        {(appointment.status === 'scheduled' || appointment.status === 'confirmed') && (
                            <button onClick={() => cancel(appointment.id)} className="danger">Отменить</button>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default AccountPage;