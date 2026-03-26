export default function EmployerDashboard() {
  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="text-2xl font-bold">Кабинет работодателя</h1>
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <section className="glass-card p-4">Профиль компании + статус верификации</section>
        <section className="glass-card p-4">Создание вакансии/мероприятия</section>
        <section className="glass-card p-4">Отклики по вакансиям</section>
      </div>
    </main>
  );
}
