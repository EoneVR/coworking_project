<template>
  <div class="home">
    <section class="hero">
      <h1>Добро пожаловать в Coworking Space</h1>
      <p>Коворкинг, кофейня и книжный магазин — всё в одном месте!</p>
      <div class="hero-buttons">
        <router-link to="/coworking" class="btn">Забронировать место</router-link>
        <router-link to="/shop" class="btn secondary">Перейти в магазин</router-link>
      </div>
    </section>

    <section class="cards">
      <div class="card">
        <h2>Коворкинг</h2>
        <p>Современные рабочие зоны для фрилансеров и команд.</p>
      </div>
      <div class="card">
        <h2>Кофейня</h2>
        <p>Ароматный кофе и свежая выпечка для продуктивности.</p>
      </div>
      <div class="card">
        <h2>Магазин</h2>
        <p>Книги, аксессуары и товары для работы.</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #1e1e2f, #3c3c5c);
  color: white;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero-buttons {
  margin-top: 1.5rem;
}

.btn {
  background: #ffcc00;
  color: #1e1e2f;
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  margin: 0 0.5rem;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.3s;
}

.btn:hover {
  background: #ffdb4d;
}

.secondary {
  background: #fff;
  color: #1e1e2f;
}

.cards {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 3rem auto;
  flex-wrap: wrap;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  padding: 2rem;
  width: 280px;
  text-align: center;
}
</style>
