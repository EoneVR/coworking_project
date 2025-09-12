<template>
  <div class="shop">
    <section class="hero">
      <h1>Категории книг</h1>
      <p>Выберите категорию, чтобы посмотреть доступные книги</p>
    </section>

    <section class="cards">
      <div 
        v-for="category in categories" 
        :key="category.id" 
        class="card"
      >
        <h2>{{ category.title }}</h2>
        <router-link 
          :to="{ name: 'shop-books', query: { category: category.id } }" 
          class="btn"
        >
          Смотреть книги
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ShopPage",
  data() {
    return {
      categories: []
    }
  },
  async created() {
    try {
      const response = await axios.get("http://localhost:8000/books/categories/");
      this.categories = response.data.results;
    } catch (error) {
      console.error("Ошибка при загрузке категорий:", error);
    }
  }
}
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #1e1e2f, #3c3c5c);
  color: white;
}

.hero h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.cards {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin: 2rem auto;
  max-width: 900px;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  padding: 1.5rem;
  text-align: center;
  width: 250px;
}

.btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1rem;
  background: #ffcc00;
  color: #1e1e2f;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.3s;
}

.btn:hover {
  background: #ffdb4d;
}
</style>
