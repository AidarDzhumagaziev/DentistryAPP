import {mockAppointments, statusNames} from '../../data/mockAppointments';
import styles from './AccountPage.module.css';

function AccountPage() {
    return(
    <div>
        <h1>Личный кабинет</h1>
        <div className={styles.grid}>
            {mockAppointments.map((appointment)=>(
            <div key={appointment.id} className={styles.card}>
                <p>{appointment.service}</p>
                <p>{appointment.doctor}</p>
                <p>{new Date(appointment.start).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}</p>
                <p>{appointment.start.slice(11, 16)}</p>
                <p>{statusNames[appointment.status]}</p>
            </div>
            ))}
        </div>
    </div>
    )
}
export default AccountPage;