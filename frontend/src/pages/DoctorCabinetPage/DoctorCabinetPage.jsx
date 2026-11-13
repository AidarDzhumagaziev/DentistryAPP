import {mockDoctorAppointments, statusNames} from '../../data/mockAppointments';
import {useState} from 'react';
import styles from './DoctorCabinetPage.module.css';


function DoctorCabinetPage() {
    const [appointments, setAppointments] = useState(mockDoctorAppointments);
    
        function changeStatus(id, newStatus){
            setAppointments(appointments.map((a) =>
            a.id === id ? { ...a, status: newStatus } : a
            ));
        }
        return(
        <div>
            <h1>Кабинет врача</h1>
            <div className={styles.grid}>
                {appointments.map((appointment)=>(
                <div key={appointment.id} className={styles.card}>
                    <p>{appointment.patient}</p>
                    <p>{appointment.service}</p>
                    <p>{appointment.start.slice(11, 16)}</p>
                    <p>{statusNames[appointment.status]}</p>
                    {(appointment.status === 'scheduled') && <button onClick={() => changeStatus(appointment.id, 'confirmed')}>Подтвердить</button>}
                    {(appointment.status === 'scheduled' || appointment.status === 'confirmed') && <button className="danger" onClick={() => changeStatus(appointment.id, 'no_show')}>Неявка</button>}
                </div>
                ))}
            </div>
        </div>
        )
}
export default DoctorCabinetPage;