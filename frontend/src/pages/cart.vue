<template>
  <div class="cart-page">
    <!-- Hero -->
    <section class="hero">
      <h1>Моя корзина</h1>
    </section>

    <!-- Контент -->
    <section class="content" v-if="cart && cart.items.length > 0">
      <div class="cart-items">
        <div v-for="item in cart.items" :key="item.id" class="cart-item">
          <!-- Фото -->
          <img
            class="book-image"
            :src="item.book.image ? `http://localhost:8000${item.book.image}` : '/no-image.png'"
            alt="Обложка книги"
          />

          <!-- Инфо -->
          <div class="info">
            <h3>{{ item.book.title }}</h3>
            <p>Автор: {{ item.book.author }}</p>
            <p>Цена: {{ item.book.unit_price }} ₽</p>
          </div>

          <!-- Количество -->
          <div class="quantity">
            <button @click="updateQuantity(item, item.quantity - 1)">-</button>
            <span>{{ item.quantity }}</span>
            <button @click="updateQuantity(item, item.quantity + 1)">+</button>
          </div>

          <!-- Итог по позиции -->
          <div class="subtotal">
            {{ item.book.unit_price * item.quantity }} ₽
          </div>

          <!-- Удаление -->
          <button class="btn delete" @click="removeItem(item.book.id)">Удалить</button>
        </div>
      </div>

      <!-- Итог -->
      <div class="cart-summary">
        <p><strong>Итого:</strong> {{ totalPrice }} ₽</p>
        <button class="btn clear" @click="clearCart">Очистить корзину</button>
        <button class="btn checkout" @click="goToCheckout">Перейти к оплате</button>
      </div>
    </section>

    <section v-else class="empty-cart">
      <p>Ваша корзина пуста 😢</p>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NewCart",
  data() {
    return {
      cart: null
    };
  },
  computed: {
    totalPrice() {
      if (!this.cart) return 0;
      return this.cart.items.reduce(
        (sum, item) => sum + item.book.unit_price * item.quantity,
        0
      );
    }
  },
  async created() {
    await this.fetchCart();
  },
  methods: {
async fetchCart() {
  try {
    const response = await axios.get("http://localhost:8000/books/carts/my_cart/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      }
    });
    this.cart = response.data;
  } catch (error) {
    console.error("Ошибка загрузки корзины:", error);
  }
},
async updateQuantity(item, newQuantity) {
  if (newQuantity <= 0) {
    return this.removeItem(item.book.id);
  }
  try {
    await axios.post("http://localhost:8000/books/carts/add_to_cart/", {
      book_id: item.book.id,
      quantity: newQuantity
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      }
    });
    await this.fetchCart();
  } catch (error) {
    console.error("Ошибка изменения количества:", error);
  }
},
async removeItem(bookId) {
  try {
    await axios.post("http://localhost:8000/books/carts/remove_from_cart/", {
      book_id: bookId
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      }
    });
    await this.fetchCart();
  } catch (error) {
    console.error("Ошибка удаления:", error);
  }
},
async clearCart() {
  if (!confirm("Очистить корзину?")) return;
  try {
    await axios.post("http://localhost:8000/books/carts/clear_cart/", {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      }
    });
    this.cart.items = [];
  } catch (error) {
    console.error("Ошибка очистки корзины:", error);
  }
},
goToCheckout() {
    if (!this.cart || !this.cart.id) {
      alert("Корзина пуста");
      return;
    }
    // Передаём cart_id в query
    this.$router.push({ path: "/checkout", query: { cart_id: this.cart.id } });
  }
  }
};
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

.cart-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border-bottom: 1px solid #ddd;
  padding: 1rem 0;
}

.book-image {
  width: 100px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.info {
  flex: 1;
}

.quantity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity button {
  background: #eee;
  border: none;
  padding: 0.3rem 0.6rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.subtotal {
  font-weight: bold;
  width: 80px;
  text-align: right;
}

.cart-summary {
  margin-top: 2rem;
  text-align: right;
}

.btn {
  margin-top: 1rem;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  transition: background 0.3s;
}

.btn.delete {
  background: #ff4d4d;
  color: white;
}

.btn.clear {
  background: #999;
  color: white;
  margin-right: 1rem;
}

.btn.checkout {
  background: #3c8dbc;
  color: white;
}

.empty-cart {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
}
</style>
