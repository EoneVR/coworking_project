<template>
  <div class="book-detail" v-if="book">
    <!-- Hero -->
    <section class="hero">
      <h1>{{ book.title }}</h1>
      <p>Автор: {{ book.author }}</p>
    </section>

    <!-- Контент -->
    <section class="content">
      <div class="book-wrapper">
        <!-- Фото -->
        <div class="image-block">
          <img
            :src="book.image ? `http://localhost:8000${book.image}` : '/no-image.png'"
            alt="Обложка книги"
          />
        </div>

        <!-- Инфо -->
        <div class="info">
        <p><strong>Название:</strong> {{ book.title}}</p>
        <p><strong>Описание:</strong> {{ book.description }}</p>
        <p><strong>Автор:</strong> {{ book.author }}</p>
        <p><strong>Год:</strong> {{ book.year_of_publish }}</p>
        <p><strong>Страниц:</strong> {{ book.pages }}</p>
        <p><strong>Переплёт:</strong> {{ book.binding }}</p>
        <p><strong>В наличии:</strong> {{ book.in_stock }}</p>
        <p><strong>Цена:</strong> {{ book.unit_price }} ₽</p>

          <!-- Кнопки -->
          <button class="btn" @click="addToCart">🛒 В корзину</button>

          <div v-if="isAdmin" class="admin-buttons">
            <button class="btn edit" @click="editBook">Изменить</button>
            <button class="btn delete" @click="deleteBook">Удалить</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BookDetail",
  data() {
    return {
      book: null,
      isAdmin: true // пока тестово; потом подтянешь из auth
    }
  },
  async created() {
    try {
      const bookId = this.$route.params.id;
      const response = await axios.get(`http://localhost:8000/books/books/${bookId}/`);
      this.book = response.data;
    } catch (error) {
      console.error("Ошибка при загрузке книги:", error);
    }
  },
methods: {
  async addToCart() {
    try {
      await axios.post("http://localhost:8000/books/carts/add_to_cart/", {
        book_id: this.book.id,
        quantity: 1
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      });

      alert("Книга добавлена в корзину!");
      this.$emit("cart-updated"); // ⚡ обновит счётчик в navbar
    } catch (error) {
      console.error("Ошибка при добавлении:", error);
      alert("Ошибка при добавлении в корзину");
    }
  },

  editBook() {
    this.$router.push(`/shop/books/${this.book.id}/edit`);
  },
  
  async deleteBook() {
    if (!confirm("Удалить книгу?")) return;
    try {
      await axios.delete(`http://localhost:8000/books/books/${this.book.id}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      });
      console.log("TOKEN:", localStorage.getItem("access_token"));
      alert("Книга удалена!");
      this.$router.push("/shop/books");
    } catch (error) {
  console.error("FULL ERROR OBJECT:", error);

  if (error.response) {
    console.error("Status:", error.response.status);
    console.error("Data:", error.response.data);
  } else if (error.request) {
    console.error("Request made, no response:", error.request);
  } else {
    console.error("Error setting up request:", error.message);
  }

  alert("Ошибка при удалении книги");
}
  }
}

}
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #1e1e2f, #3c3c5c);
  color: white;
}

.content {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.book-wrapper {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  align-items: flex-start;
}

.image-block img {
  max-width: 280px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.info {
  flex: 1;
}

.btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  border: none;
  transition: background 0.3s;
}

.btn:not(.delete):not(.edit) {
  background: #ffcc00;
  color: #1e1e2f;
}

.btn.edit {
  background: #3c8dbc;
  color: white;
  margin-left: 0.5rem;
}

.btn.edit:hover {
  background: #5ca6d6;
}

.btn.delete {
  background: #ff4d4d;
  color: white;
  margin-left: 0.5rem;
}

.btn.delete:hover {
  background: #ff6666;
}
</style>
