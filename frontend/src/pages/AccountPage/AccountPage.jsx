import {mockAppointments, statusNames} from '../../data/mockAppointments';
import { useState} from 'react';
import styles from './AccountPage.module.css';


function AccountPage() {
    const [appointments, setAppointments] = useState(mockAppointments);

    function cancel(id){
        setAppointments(appointments.map((a) =>
        a.id === id ? { ...a, status: 'cancelled' } : a
        ));
    }
    return(
    <div>
        <h1>Личный кабинет</h1>
        <div className={styles.grid}>
            {appointments.map((appointment)=>(
            <div key={appointment.id} className={styles.card}>
                <p>{appointment.service}</p>
                <p>{appointment.doctor}</p>
                <p>{new Date(appointment.start).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}</p>
                <p>{appointment.start.slice(11, 16)}</p>
                <p>{statusNames[appointment.status]}</p>
                {(appointment.status === 'scheduled' || appointment.status === 'confirmed') && <button onClick={() => cancel(appointment.id)}>Отменить</button>}
            </div>
            ))}
        </div>
    </div>
    )
}
export default AccountPage;