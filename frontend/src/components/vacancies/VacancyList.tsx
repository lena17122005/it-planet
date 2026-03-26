import type { Vacancy } from '../../types';
import VacancyCard from './VacancyCard';

interface Props {
  vacancies: Vacancy[];
  favorites: string[];
  onToggleFavorite: (id: string) => void;
  onOpen: (vacancy: Vacancy) => void;
}

export default function VacancyList({ vacancies, favorites, onToggleFavorite, onOpen }: Props) {
  if (!vacancies.length) {
    return <div className="glass-card p-6 text-sm text-slate-500">Ничего не найдено. Измените фильтры.</div>;
  }

  return (
    <div className="space-y-3">
      {vacancies.map((vacancy) => (
        <VacancyCard
          key={vacancy.id}
          vacancy={vacancy}
          isFavorite={favorites.includes(vacancy.id)}
          onToggleFavorite={onToggleFavorite}
          onOpen={onOpen}
        />
      ))}
    </div>
  );
}
