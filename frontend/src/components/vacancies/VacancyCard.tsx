import { motion } from 'framer-motion';
import type { Vacancy } from '../../types';
import Button from '../common/Button';

interface Props {
  vacancy: Vacancy;
  isFavorite: boolean;
  onToggleFavorite: (id: string) => void;
  onOpen: (vacancy: Vacancy) => void;
}

export default function VacancyCard({ vacancy, isFavorite, onToggleFavorite, onOpen }: Props) {
  return (
    <motion.article layout className="glass-card p-4">
      <div className="mb-2 flex items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold">{vacancy.title}</h3>
          <p className="text-sm text-slate-500">{vacancy.company} • {vacancy.city}</p>
        </div>
        <button className="text-xl" onClick={() => onToggleFavorite(vacancy.id)}>{isFavorite ? '💙' : '🤍'}</button>
      </div>

      <p className="text-sm text-slate-700">{vacancy.description}</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {vacancy.tags.map((tag) => (
          <span key={tag} className="rounded-full bg-slate-100 px-2 py-1 text-xs">#{tag}</span>
        ))}
      </div>
      <div className="mt-4 flex items-center justify-between">
        <span className="text-sm font-medium text-brand-700">
          {vacancy.salaryFrom ? `${vacancy.salaryFrom.toLocaleString()} ₽` : 'З/п по договоренности'}
        </span>
        <Button variant="secondary" onClick={() => onOpen(vacancy)}>Подробнее</Button>
      </div>
    </motion.article>
  );
}
