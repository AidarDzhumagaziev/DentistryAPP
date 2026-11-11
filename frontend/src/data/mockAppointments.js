export const statusNames = {
  scheduled: 'Запланирована',
  confirmed: 'Подтверждена',
  completed: 'Завершена',
  cancelled: 'Отменена',
  no_show: 'Неявка',
};

export const mockAppointments = [
    { id: 1, service: 'Лечение кариеса', doctor: 'Дмитрий Лебедев', start: '2026-11-16T14:00:00', status: 'scheduled' },
    { id: 2, service: 'Профессиональная гигиена', doctor: 'Мария Орлова', start: '2026-11-20T10:30:00', status: 'confirmed' },
    { id: 3, service: 'Осмотр и консультация', doctor: 'Анна Иванова', start: '2026-11-02T09:00:00', status: 'completed' },
];