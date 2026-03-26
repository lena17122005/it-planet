import { type FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import type { Role } from '../types';

export default function Register() {
  const navigate = useNavigate();
  const [role, setRole] = useState<Role>('seeker');
  const [email, setEmail] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [password, setPassword] = useState('');

  const [companyName, setCompanyName] = useState('');
  const [inn, setInn] = useState('');
  const [corporateEmail, setCorporateEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage('');
    try {
      await apiClient.post('/api/v1/auth/register', {
        email,
        display_name: displayName,
        password,
        role,
        company_name: role === 'employer' ? companyName : undefined,
        inn: role === 'employer' ? inn : undefined,
        corporate_email: role === 'employer' ? corporateEmail : undefined
      });
      setMessage('Регистрация успешна. Код подтверждения для MVP: 123456');
      setTimeout(() => navigate('/login'), 900);
    } catch {
      setMessage('Ошибка регистрации. Проверьте данные.');
    }
  };

  return (
    <main className="mx-auto max-w-xl p-6">
      <form onSubmit={handleSubmit} className="glass-card grid gap-3 p-6">
        <h1 className="text-2xl font-bold">Регистрация</h1>
        <select className="rounded-xl border p-2" value={role} onChange={(e) => setRole(e.target.value as Role)}>
          <option value="seeker">Соискатель</option>
          <option value="employer">Работодатель</option>
          <option value="curator">Куратор</option>
        </select>
        <input className="rounded-xl border p-2" placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="rounded-xl border p-2" placeholder="Отображаемое имя" value={displayName} onChange={(e) => setDisplayName(e.target.value)} />
        <input className="rounded-xl border p-2" placeholder="Пароль" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

        {role === 'employer' && (
          <>
            <input className="rounded-xl border p-2" placeholder="Название компании" value={companyName} onChange={(e) => setCompanyName(e.target.value)} />
            <input className="rounded-xl border p-2" placeholder="ИНН" value={inn} onChange={(e) => setInn(e.target.value)} />
            <input className="rounded-xl border p-2" placeholder="Корп. email" value={corporateEmail} onChange={(e) => setCorporateEmail(e.target.value)} />
          </>
        )}

        {message && <p className="text-sm text-slate-600">{message}</p>}
        <button className="rounded-xl bg-brand-500 p-2 text-white">Создать аккаунт</button>
      </form>
    </main>
  );
}
