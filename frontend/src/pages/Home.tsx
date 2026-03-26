import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import Map from '../components/map/Map';
import Modal from '../components/common/Modal';
import VacancyList from '../components/vacancies/VacancyList';
import type { Vacancy } from '../types';
import { useVacancies } from '../hooks/useVacancies';

const LS_KEY = 'tramplin_favorites';

function readFavorites(): string[] {
  const raw = localStorage.getItem(LS_KEY);
  return raw ? JSON.parse(raw) : [];
}

export default function Home() {
  const { vacancies, filters, setFilters } = useVacancies();
  const [selected, setSelected] = useState<Vacancy | null>(null);
  const [favorites, setFavorites] = useState<string[]>(() => readFavorites());

  const counters = useMemo(
    () => ({
      all: vacancies.length,
      events: vacancies.filter((v) => v.type === 'event').length,
      favorites: vacancies.filter((v) => favorites.includes(v.id)).length
    }),
    [favorites, vacancies]
  );

  const toggleFavorite = (id: string) => {
    const next = favorites.includes(id) ? favorites.filter((item) => item !== id) : [...favorites, id];
    setFavorites(next);
    localStorage.setItem(LS_KEY, JSON.stringify(next));
  };

  return (
    <main className="mx-auto max-w-7xl space-y-4 p-4 lg:p-6">
      <section className="glass-card p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold">Трамплин</h1>
            <p className="mt-1 text-sm text-slate-500">Карьера, стажировки, события и нетворкинг в одном месте.</p>
          </div>
          <div className="grid grid-cols-3 gap-2 text-sm">
            <div className="rounded-xl bg-slate-100 px-3 py-2">Всего: <b>{counters.all}</b></div>
            <div className="rounded-xl bg-emerald-100 px-3 py-2">События: <b>{counters.events}</b></div>
            <div className="rounded-xl bg-blue-100 px-3 py-2">Избранное: <b>{counters.favorites}</b></div>
          </div>
        </div>

        <div className="mt-4 grid gap-3 md:grid-cols-2 lg:grid-cols-6">
          <input
            className="rounded-xl border border-slate-200 px-3 py-2"
            placeholder="Поиск по названию/компании"
            value={filters.query}
            onChange={(e) => setFilters((prev) => ({ ...prev, query: e.target.value }))}
          />
          <input
            className="rounded-xl border border-slate-200 px-3 py-2"
            placeholder="Город"
            value={filters.city}
            onChange={(e) => setFilters((prev) => ({ ...prev, city: e.target.value }))}
          />
          <input
            type="number"
            className="rounded-xl border border-slate-200 px-3 py-2"
            placeholder="Зарплата от"
            onChange={(e) => setFilters((prev) => ({ ...prev, salaryFrom: Number(e.target.value) || undefined }))}
          />
          <input
            type="number"
            className="rounded-xl border border-slate-200 px-3 py-2"
            placeholder="Зарплата до"
            onChange={(e) => setFilters((prev) => ({ ...prev, salaryTo: Number(e.target.value) || undefined }))}
          />
          <select
            className="rounded-xl border border-slate-200 px-3 py-2"
            value={filters.format}
            onChange={(e) => setFilters((prev) => ({ ...prev, format: e.target.value as typeof prev.format }))}
          >
            <option value="all">Формат: любой</option>
            <option value="office">Офис</option>
            <option value="hybrid">Гибрид</option>
            <option value="remote">Удаленно</option>
          </select>
          <input
            className="rounded-xl border border-slate-200 px-3 py-2"
            placeholder="Теги: React, FastAPI"
            value={filters.tags}
            onChange={(e) => setFilters((prev) => ({ ...prev, tags: e.target.value }))}
          />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.1fr,0.9fr]">
        <motion.div layout className="glass-card p-3">
          <Map vacancies={vacancies} favoriteIds={favorites} onSelect={setSelected} />
        </motion.div>
        <motion.div layout className="space-y-3">
          <VacancyList vacancies={vacancies} favorites={favorites} onToggleFavorite={toggleFavorite} onOpen={setSelected} />
        </motion.div>
      </section>

      <Modal isOpen={Boolean(selected)} onClose={() => setSelected(null)} title={selected?.title ?? ''}>
        {selected && (
          <div className="space-y-3 text-sm text-slate-700">
            <p><b>Компания:</b> {selected.company}</p>
            <p><b>Тип:</b> {selected.type} • <b>Формат:</b> {selected.format}</p>
            <p><b>Адрес:</b> {selected.address ?? selected.city}</p>
            <p><b>Описание:</b> {selected.description}</p>
            {selected.requirements && <p><b>Требования:</b> {selected.requirements}</p>}
            <p><b>Теги:</b> {selected.tags.join(', ')}</p>
            <button className="rounded-xl bg-brand-500 px-4 py-2 text-white">Откликнуться</button>
          </div>
        )}
      </Modal>
    </main>
  );
}
