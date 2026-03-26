import { type FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { apiClient } from '../services/api';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const { data } = await apiClient.post('/api/v1/auth/login', { email, password });
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);

      const me = await apiClient.get('/api/v1/users/me');
      login({
        id: String(me.data.id),
        email: me.data.email,
        displayName: me.data.display_name,
        role: me.data.role
      });

      navigate(`/dashboard/${me.data.role}`);
    } catch {
      setError('Неверный email или пароль');
    }
  };

  return (
    <main className="mx-auto max-w-md p-6">
      <form onSubmit={handleSubmit} className="glass-card space-y-4 p-6">
        <h1 className="text-2xl font-bold">Вход</h1>
        <input className="w-full rounded-xl border p-2" placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full rounded-xl border p-2" placeholder="Пароль" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error && <p className="text-sm text-red-500">{error}</p>}
        <button className="w-full rounded-xl bg-brand-500 p-2 text-white">Войти</button>
      </form>
    </main>
  );
}
