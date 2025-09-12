<template>
  <div class="checkout-page">
    <section class="hero">
      <h1>Оформление заказа</h1>
    </section>

    <section class="form-section">
      <form @submit.prevent="submitOrder">
        <div class="form-group">
          <label>Страна</label>
          <input v-model="form.country" type="text" required />
        </div>
        <div class="form-group">
          <label>Город</label>
          <input v-model="form.city" type="text" required />
        </div>
        <div class="form-group">
          <label>Адрес</label>
          <input v-model="form.address" type="text" required />
        </div>
        <div class="form-group">
          <label>Регион / Штат</label>
          <input v-model="form.state" type="text" />
        </div>
        <div class="form-group">
          <label>Индекс</label>
          <input v-model="form.zipcode" type="text" required />
        </div>
        <div class="form-group">
          <label>Телефон</label>
          <input v-model="form.phone" type="text" required />
        </div>
        <div class="form-group">
          <label>Примечание к заказу</label>
          <textarea v-model="form.order_notes"></textarea>
        </div>

        <button type="submit" class="btn checkout">Оплатить</button>
      </form>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NewCheckout",
  data() {
    return {
      cartId: null,
      form: {
        country: "",
        city: "",
        address: "",
        state: "",
        zipcode: "",
        phone: "",
        order_notes: ""
      }
    };
  },
  created() {
    // Берём cart_id из query параметров
    this.cartId = this.$route.query.cart_id;
    if (!this.cartId) {
      alert("Нет корзины для оформления заказа");
      this.$router.push("/cart");
    }
  },
  methods: {
    async submitOrder() {
      try {
        // 1️⃣ Создаём адрес доставки
        const addressRes = await axios.post(
          "http://localhost:8000/books/delivery/",
          this.form,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        );

        const deliveryId = addressRes.data.id;

        // 2️⃣ Создаём заказ с cart_id и delivery_address_id
        const orderRes = await axios.post(
          "http://localhost:8000/books/orders/",
          {
            cart_id: this.cartId,
            delivery_address_id: deliveryId
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }
        );

        // 3️⃣ Перенаправляем на Stripe
        window.location.href = orderRes.data.checkout_url;
      } catch (error) {
        console.error("Ошибка при оформлении заказа:", error);
        alert("Не удалось оформить заказ. Попробуйте ещё раз.");
      }
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

.form-section {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.3rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.btn.checkout {
  background: #3c8dbc;
  color: white;
  border: none;
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}
</style>
