<template>
  <div class="menu-page">
    <section class="hero">
      <h1>Меню кофейни</h1>
    </section>

    <section class="blocks">
      <!-- Бар -->
      <router-link to="/coffeeshop/coffee" class="block-link">
        <div class="block">
          <h2>Бар</h2>
          <p>Напитки и кофе</p>
        </div>
      </router-link>

      <!-- Выпечка -->
      <router-link to="/coffeeshop/bakery" class="block-link">
        <div class="block">
          <h2>Выпечка</h2>
          <p>Свежая выпечка каждый день</p>
        </div>
      </router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: "MenuPage",
};
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #1e1e2f, #3c3c5c);
  color: white;
}

.blocks {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 2rem;
}

.block-link {
  width: 40%;
  text-decoration: none;
  color: inherit;
}

.block {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.2s ease;
}

.block:hover {
  transform: translateY(-5px);
}

.block h2 {
  margin-bottom: 1rem;
}

.block p {
  margin: 0;
  color: #555;
}
</style>
