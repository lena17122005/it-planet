export default function SeekerDashboard() {
  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="text-2xl font-bold">Кабинет соискателя</h1>
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <section className="glass-card p-4">Профиль и приватность</section>
        <section className="glass-card p-4">Отклики и избранное</section>
        <section className="glass-card p-4">Нетворкинг и контакты</section>
      </div>
    </main>
  );
}
