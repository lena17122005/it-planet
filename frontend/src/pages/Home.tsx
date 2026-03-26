import Map from '../components/map/Map';
import VacancyList from '../components/vacancies/VacancyList';
import { useVacancies } from '../hooks/useVacancies';

export default function Home() {
  const { vacancies, isLoading } = useVacancies();

  return (
    <main className="mx-auto grid max-w-7xl gap-6 p-4 lg:grid-cols-2">
      <section className="space-y-4">
        <h1 className="text-2xl font-bold">Трамплин</h1>
        {isLoading ? <div className="h-40 animate-pulse rounded-xl bg-slate-200" /> : <VacancyList vacancies={vacancies} />}
      </section>
      <section>{isLoading ? <div className="h-[420px] animate-pulse rounded-xl bg-slate-200" /> : <Map vacancies={vacancies} />}</section>
    </main>
  );
}
