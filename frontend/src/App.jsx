import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
import HomePage from './pages/HomePage/HomePage';
import ServicesPage from './pages/ServicesPage/ServicesPage';
import DoctorsPage from './pages/DoctorsPage/DoctorsPage';
import LoginPage from './pages/LoginPage/LoginPage';
import NotFoundPage from './pages/NotFoundPage/NotFoundPage';
import RegisterPage from './pages/RegisterPage/RegisterPage';
import AccountPage from './pages/AccountPage/AccountPage';
import DoctorCabinetPage from './pages/DoctorCabinetPage/DoctorCabinetPage';
import AdminPage from './pages/AdminPage/AdminPage';
import BookingPage from './pages/BookingPage/BookingPage';


function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="services" element={<ServicesPage />} />
        <Route path="doctors" element={<DoctorsPage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="doctor-cabinet" element={<ProtectedRoute roles={['doctor']}><DoctorCabinetPage /></ProtectedRoute>} />
        <Route path="admin" element={<ProtectedRoute roles={['admin']}><AdminPage /></ProtectedRoute>} />
        <Route path="account" element={<ProtectedRoute><AccountPage /></ProtectedRoute>} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="booking" element={<ProtectedRoute><BookingPage /></ProtectedRoute>} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;