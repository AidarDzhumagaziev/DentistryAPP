import { useEffect, useState } from 'react';
import { authFetch, getJson } from '../../api/client';
import styles from './AdminPage.module.css';

const cabinetTypes = [
  { value: 'general', label: 'Общий' },
  { value: 'surgical', label: 'Хирургический' },
  { value: 'roentgen', label: 'Рентген' },
];

function typeLabel(value) {
  const type = cabinetTypes.find((item) => item.value === value);
  return type ? type.label : value;
}


function AdminCabinets() {
  const [cabinets, setCabinets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);
  const [formError, setFormError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [number, setNumber] = useState('');
  const [type, setType] = useState('general');

  useEffect(() => {
    getJson('/api/v1/cabinets/')
      .then((data) => setCabinets(data))
      .catch(() => setLoadError('Не удалось загрузить кабинеты'))
      .finally(() => setIsLoading(false));
  }, []);

  function resetForm() {
    setNumber('');
    setType('general');
    setEditingId(null);
    setShowForm(false);
    setFormError(null);
  }

  function startCreate() {
    resetForm();
    setShowForm(true);
  }

  function startEdit(cabinet) {
    setNumber(String(cabinet.number));
    setType(cabinet.type);
    setEditingId(cabinet.id);
    setShowForm(true);
    setFormError(null);
  }

  function handleSubmit(e) {
    e.preventDefault();
    const value = Number(number);

    if (!Number.isInteger(value) || value <= 0) {
      setFormError('Номер кабинета — целое число больше нуля');
      return;
    }
    if (cabinets.some((item) => item.number === value && item.id !== editingId)) {
      setFormError('Кабинет с таким номером уже есть');
      return;
    }

    const url = editingId ? `/api/v1/cabinets/${editingId}/` : '/api/v1/cabinets/';
    const method = editingId ? 'PUT' : 'POST';

    authFetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ number: value, type: type }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Сервер ответил ошибкой');
        }
        return response.json();
      })
      .then((data) => {
        if (editingId) {
          setCabinets(cabinets.map((item) => (item.id === data.id ? data : item)));
        } else {
          setCabinets([...cabinets, data]);
        }
        resetForm();
      })
      .catch(() => setFormError('Не удалось сохранить кабинет'));
  }

  function remove(id) {
    if (!confirm('Удалить кабинет?')) {
      return;
    }
    authFetch(`/api/v1/cabinets/${id}/`, { method: 'DELETE' })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Сервер ответил ошибкой');
        }
        setCabinets(cabinets.filter((item) => item.id !== id));
      })
      .catch(() => alert('Не удалось удалить кабинет: возможно, он занят в графике'));
  }
  if (isLoading) {
    return <p>Загрузка…</p>;
  }

  if (loadError) {
    return <p>{loadError}</p>;
  }
  return (
    <div>
      <div className={styles.top}>
        <h1>Кабинеты</h1>
        <button onClick={startCreate}>Добавить кабинет</button>
      </div>

      {showForm && (
        <div className={styles.formCard}>
          <h2>{editingId ? 'Изменить кабинет' : 'Новый кабинет'}</h2>
          <form className={styles.form} onSubmit={handleSubmit}>
            <label className={styles.field}>
              Номер
              <input
                type="number"
                min="1"
                className={styles.input}
                value={number}
                onChange={(e) => setNumber(e.target.value)}
              />
            </label>
            <label className={styles.field}>
              Тип
              <select className={styles.input} value={type} onChange={(e) => setType(e.target.value)}>
                {cabinetTypes.map((item) => (
                  <option key={item.value} value={item.value}>{item.label}</option>
                ))}
              </select>
            </label>
            {formError && <p className={styles.formError}>{formError}</p>}
            <div className={styles.rowActions}>
              <button type="submit" className={styles.submit}>{editingId ? 'Сохранить' : 'Добавить'}</button>
              <button type="button" className="secondary" onClick={resetForm}>Отмена</button>
            </div>
          </form>
        </div>
      )}
      <div className={styles.tableWrap}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th className={styles.th}>Номер</th>
              <th className={styles.th}>Тип</th>
              <th className={styles.th}></th>
            </tr>
          </thead>
          <tbody>
            {cabinets.map((cabinet) => (
              <tr key={cabinet.id}>
                <td className={styles.td}>{cabinet.number}</td>
                <td className={styles.td}>{typeLabel(cabinet.type)}</td>
                <td className={styles.td}>
                  <div className={styles.rowActions}>
                    <button onClick={() => startEdit(cabinet)} className="secondary">Изменить</button>
                    <button onClick={() => remove(cabinet.id)} className="danger">Удалить</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {cabinets.length === 0 && <p className={styles.empty}>Кабинетов пока нет.</p>}
    </div>
  );
}
export default AdminCabinets;