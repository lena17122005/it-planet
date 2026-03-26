import { Navigate, Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import VacancyDetail from './pages/VacancyDetail';
import SeekerDashboard from './pages/Dashboard/SeekerDashboard';
import EmployerDashboard from './pages/Dashboard/EmployerDashboard';
import CuratorDashboard from './pages/Dashboard/CuratorDashboard';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import type { Role } from './types';

function ProtectedRoute({ role, children }: { role: Role; children: JSX.Element }) {
  const { state } = useAuth();
  if (!state.user) return <Navigate to="/login" replace />;
  if (state.user.role !== role) return <Navigate to="/" replace />;
  return children;
}

function Layout({ children }: { children: JSX.Element }) {
  const { state, logout } = useAuth();

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link to="/" className="text-xl font-bold text-brand-700">Трамплин</Link>
          <nav className="flex items-center gap-2 text-sm">
            {!state.user && (
              <>
                <Link to="/login" className="rounded-lg px-3 py-2 hover:bg-slate-100">Вход</Link>
                <Link to="/register" className="rounded-lg bg-brand-500 px-3 py-2 text-white">Регистрация</Link>
              </>
            )}
            {state.user && (
              <>
                <span className="rounded-lg bg-slate-100 px-3 py-2">{state.user.displayName}</span>
                <button className="rounded-lg px-3 py-2 hover:bg-slate-100" onClick={logout}>Выйти</button>
              </>
            )}
          </nav>
        </div>
      </header>
      {children}
    </>
  );
}

function AppRoutes() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/vacancies/:id" element={<VacancyDetail />} />
        <Route
          path="/dashboard/seeker"
          element={
            <ProtectedRoute role="seeker">
              <SeekerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard/employer"
          element={
            <ProtectedRoute role="employer">
              <EmployerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard/curator"
          element={
            <ProtectedRoute role="curator">
              <CuratorDashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Layout>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen text-slate-900">
        <AppRoutes />
      </div>
    </AuthProvider>
  );
}
