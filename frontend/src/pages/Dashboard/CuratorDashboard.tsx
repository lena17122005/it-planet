export default function CuratorDashboard() {
  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="text-2xl font-bold">Кабинет куратора</h1>
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <section className="glass-card p-4">Компании на верификации</section>
        <section className="glass-card p-4">Вакансии на модерации</section>
        <section className="glass-card p-4">Управление пользователями и тегами</section>
      </div>
    </main>
  );
}
