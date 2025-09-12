<template>
  <div class="menu-list">
    <section class="hero">
      <h1>Пекарня</h1>
    </section>

    <section class="items">
      <div v-for="item in bakeryItems" :key="item.id" class="card">
        <img
          v-if="item.image"
          :src="item.image"
          alt="bakery"
          class="card-img"
        />
        <h3>{{ item.title }}</h3>
        <p>{{ item.ingredients }}</p>
        <p>В наличии: {{ item.in_stock }}</p>
        <p class="price">{{ item.unit_price }} ₽</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BakeryPage",
  data() {
    return {
      bakeryItems: [],
    };
  },
  async created() {
    try {
      const res = await axios.get("http://localhost:8000/coffee/bakery/");
      this.bakeryItems = res.data.results;
    } catch (error) {
      console.error("Ошибка загрузки выпечки:", error);
    }
  },
};
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #5c3c3c, #2f1e1e);
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
  color: #d35400;
}
</style>
