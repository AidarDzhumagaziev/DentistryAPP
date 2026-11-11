import { useState, useEffect } from 'react';
import styles from './BookingPage.module.css';
import { getJson } from '../../api/client';

function BookingPage(){
    const [step, setStep] = useState(1);

    const [services, setServices] = useState([]);
    useEffect(() => {
        getJson('/api/v1/services/')
        .then((data) => setServices(data))
    }, []);

    return(
        <>
            <h1>Запись</h1>
            <div>Шаг {step} из 4</div>

            {(step === 1) && <h2>Выберите услугу</h2>}
            {(step === 1) && 
            <div className={styles.grid}>
                {services.map((service) => (
                    <button key={service.id} className={styles.card}>
                        <span className={styles.name} >{service.name}</span>
                        <span className={styles.price} >от {Number(service.price_from).toLocaleString('ru-RU')} ₽</span>
                    </button>
                ))}
            </div>
            }
            {(step === 2) && <h2>Выберите врача</h2>}
            {(step === 3) && <h2>Выберите дату и время</h2>}
            {(step === 4) && <h2>Подтверждение</h2>}

            {(step <4) && <button onClick={() =>setStep(step+1)}>Далее</button>}
            {(step >1) && <button onClick={() =>setStep(step-1)}>Назад</button>}
         
        </>
    )
}
export default BookingPage;