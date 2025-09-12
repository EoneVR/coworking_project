<template>
  <div class="book-edit" v-if="book">
    <h1>Редактировать книгу</h1>

    <form @submit.prevent="updateBook" class="form">
      <label>Название</label>
      <input v-model="book.title" type="text" required />
      
      <label>Описание</label>
      <textarea v-model="book.description"></textarea>
      
      <label>Автор</label>
      <input v-model="book.author" type="text" required />
      
      <label>Цена</label>
      <input v-model="book.unit_price" type="number" step="0.01" />

      <label>Год</label>
      <input v-model="book.year_of_publish" type="number" />

      <label>Страниц</label>
      <input v-model="book.pages" type="number" />

      <label>Переплёт</label>
      <select v-model="book.binding">
        <option value="hard">Твёрдый</option>
        <option value="soft">Мягкий</option>
      </select>

      <label>В наличии</label>
      <input v-model="book.in_stock" type="number" />

      <button type="submit" class="btn">Сохранить</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BookEdit",
  data() {
    return {
      book: null
    }
  },
  async created() {
    const bookId = this.$route.params.id;
    try {
      const response = await axios.get(`http://localhost:8000/books/books/${bookId}/`);
      this.book = response.data;
    } catch (error) {
      console.error("Ошибка загрузки:", error);
    }
  },
methods: {
async updateBook() {
  try {
    await axios.put(
      `http://localhost:8000/books/books/${this.book.id}/`,
      this.book,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      }
    );

    alert("Книга обновлена!");
    this.$router.push(`/shop/books/${this.book.id}`);
  } catch (error) {
    console.error("Ошибка обновления:", error.response || error);
    alert("Ошибка при обновлении книги");
  }
}
}
}
</script>

<style scoped>
.form {
  max-width: 500px;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input, textarea, select {
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.btn {
  background: #3c8dbc;
  color: white;
  padding: 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  font-weight: bold;
  transition: background 0.3s;
}

.btn:hover {
  background: #5ca6d6;
}
</style>
