<template>
  <div class="books">
    <section class="hero">
      <h1>Книги</h1>
      <p v-if="categoryId">Показаны книги категории №{{ categoryId }}</p>
      <p v-else>Все доступные книги</p>
    </section>

    <section class="cards">
      <div 
        v-for="book in filteredBooks" 
        :key="book.id"
        class="card"
      >
        <!-- Картинка -->
        <img 
          v-if="book.image" 
          :src="`http://localhost:8000${book.image}`" 
          alt="book cover" 
          class="card-img"
        />

        <h2>{{ book.title }}</h2>
        <p><strong>Автор:</strong> {{ book.author }}</p>
        <p><strong>Цена:</strong> {{ book.unit_price }} ₽</p>

        <div class="card-buttons">
          <button class="btn" @click="addToCart(book)">В корзину</button>
          <router-link :to="`/shop/books/${book.id}`" class="btn secondary">Подробнее</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BooksPage",
  data() {
    return {
      books: [],
      categoryId: null
    }
  },
  computed: {
    filteredBooks() {
      if (!this.categoryId) return this.books;
      return this.books.filter(book => book.category === Number(this.categoryId));
    }
  },
  async created() {
    try {
      this.categoryId = this.$route.query.category || null;
      const response = await axios.get("http://localhost:8000/books/books/");
      this.books = response.data.results;
    } catch (error) {
      console.error("Ошибка при загрузке книг:", error);
    }
  },
  watch: {
    "$route.query.category"(newVal) {
      this.categoryId = newVal || null;
    }
  },
  methods: {
    async addToCart(book) {
      try {
        await axios.post("http://localhost:8000/books/carts/add_to_cart/", {
          book_id: book.id,
          quantity: 1
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        });

        alert("Книга добавлена в корзину!");
        this.$emit("cart-updated");
      } catch (error) {
        console.error("Ошибка при добавлении:", error);
        alert("Ошибка при добавлении в корзину");
      }
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

.cards {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin: 2rem auto;
  max-width: 1100px;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  padding: 1.5rem;
  text-align: center;
  width: 280px;
}

.card h2 {
  margin-bottom: 0.5rem;
}

.card-img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.card-buttons {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn {
  padding: 0.6rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.3s;
}

.btn:first-child {
  background: #ffcc00;
  color: #1e1e2f;
}

.btn:first-child:hover {
  background: #ffdb4d;
}

.btn.secondary {
  background: #1e1e2f;
  color: white;
}

.btn.secondary:hover {
  background: #33334d;
}
</style>
