import type { Vacancy } from '../../types';

interface Props {
  vacancies: Vacancy[];
}

export default function VacancyList({ vacancies }: Props) {
  return (
    <div className="space-y-3">
      {vacancies.map((vacancy) => (
        <article key={vacancy.id} className="rounded-xl bg-white p-4 shadow">
          <h3 className="text-lg font-semibold">{vacancy.title}</h3>
          <p className="text-slate-600">{vacancy.company} • {vacancy.city}</p>
          <p className="mt-2 text-sm">{vacancy.tags.join(', ')}</p>
        </article>
      ))}
    </div>
  );
}
