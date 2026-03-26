import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import VacancyDetail from './pages/VacancyDetail';
import SeekerDashboard from './pages/Dashboard/SeekerDashboard';
import EmployerDashboard from './pages/Dashboard/EmployerDashboard';
import CuratorDashboard from './pages/Dashboard/CuratorDashboard';

export default function App() {
  return (
    <div className="min-h-screen text-slate-900">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/vacancies/:id" element={<VacancyDetail />} />
        <Route path="/dashboard/seeker" element={<SeekerDashboard />} />
        <Route path="/dashboard/employer" element={<EmployerDashboard />} />
        <Route path="/dashboard/curator" element={<CuratorDashboard />} />
      </Routes>
    </div>
  );
}
