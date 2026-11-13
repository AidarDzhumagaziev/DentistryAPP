export const statusNames = {
  scheduled: 'Запланирована',
  confirmed: 'Подтверждена',
  completed: 'Завершена',
  cancelled: 'Отменена',
  no_show: 'Неявка',
};

export const mockAppointments = [
    { id: 1, service: 'Лечение кариеса', doctor: 'Дмитрий Лебедев', start: '2026-11-16T14:00:00', status: 'scheduled'},
    { id: 2, service: 'Профессиональная гигиена', doctor: 'Мария Орлова', start: '2026-11-20T10:30:00', status: 'confirmed'},
    { id: 3, service: 'Осмотр и консультация', doctor: 'Анна Иванова', start: '2026-11-02T09:00:00', status: 'completed'},
];

export const mockDoctorAppointments = [
    { id: 1, patient: 'Иван Петров', service: 'Лечение кариеса', start: '2026-11-14T14:00:00', status: 'scheduled', duration: 60, cabinet: 102, alert: 'Аллергия: лидокаин'},
    { id: 2, patient: 'Ольга Сидорова', service: 'Осмотр и консультация', start: '2026-11-14T14:45:00', status: 'confirmed', duration: 30, cabinet: 102, alert:''},
    { id: 3, patient: 'Сергей Волков', service: 'Острая боль', start: '2026-11-14T15:30:00', status: 'scheduled', duration: 30, cabinet: 102, alert: ''},
];