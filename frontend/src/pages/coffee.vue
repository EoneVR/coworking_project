<template>
  <div class="menu-list">
    <section class="hero">
      <h1>Бар</h1>
    </section>

    <section class="items">
      <div v-for="item in coffeeItems" :key="item.id" class="card">
        <img
          v-if="item.image"
          :src="`http://localhost:8000${item.image}`"
          alt="coffee"
          class="card-img"
        />
        <h3>{{ item.title }}</h3>
        <p>{{ item.size }} — {{ item.ingredients }}</p>
        <p class="price">{{ item.unit_price }} ₽</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CoffeePage",
  data() {
    return {
      coffeeItems: [],
    };
  },
  async created() {
    try {
      const res = await axios.get("http://localhost:8000/coffee/coffees/");
      this.coffeeItems = res.data.results;
    } catch (error) {
      console.error("Ошибка загрузки бара:", error);
    }
  },
};
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #3c3c5c, #1e1e2f);
  color: white;
}

.items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  margin: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 1.2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.price {
  font-weight: bold;
  color: #3c8dbc;
}
</style>
