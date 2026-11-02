import { Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import HomePage from './pages/HomePage/HomePage';
import DoctorsPage from './pages/DoctorsPage/DoctorsPage';
import ServicesPage from './pages/ServicesPage/ServicesPage';

function App() {
  return (
    <>
      <Header />
      <main style={{ padding: '24px' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/doctors" element={<DoctorsPage />} />
        </Routes>
      </main>
    </>
  );
}

export default App;