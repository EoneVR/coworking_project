<template>
  <div class="profile-page">
    <h1>👤 Профиль</h1>

    <!-- Логин -->
    <section class="profile-info">
      <p><strong>Логин:</strong> {{ username }}</p>
    </section>

    <!-- Заказы -->
    <section class="profile-section">
      <h2>📚 Мои заказы</h2>
      <ul v-if="orders.length > 0" class="order-list">
        <li v-for="order in orders" :key="order.id" class="order-card">
          <p>Заказ #{{ order.id }} — <b>{{ order.payment_status }}</b> ({{ formatDate(order.placed_at) }})</p>
          <ul>
            <li v-for="item in order.items" :key="item.id">
              {{ item.book.title }} — {{ item.quantity }} шт. × {{ item.unit_price }} ₽
            </li>
          </ul>
        </li>
      </ul>
      <p v-else>Нет заказов</p>
    </section>

    <!-- Подписки -->
    <section class="profile-section">
      <h2>🎟 Мои подписки</h2>
      <ul v-if="subscriptions.length > 0" class="subscription-list">
        <li v-for="sub in subscriptions" :key="sub.id" class="subscription-card">
          <p><b>{{ sub.subscription.title }}</b></p>
          <p>с {{ sub.start_date }} до {{ sub.end_date }}</p>
          <p v-if="sub.is_active">✅ Активна (осталось {{ sub.remaining_days }} дней)</p>
          <p v-else>❌ Истекла</p>
        </li>
      </ul>
      <p v-else>Нет подписок</p>
    </section>

    <!-- Бронирования -->
    <section class="profile-section">
      <h2>🏠 Мои брони</h2>
      <ul v-if="bookings.length > 0" class="booking-list">
        <li v-for="booking in bookings" :key="booking.id" class="booking-card">
          <p><b>{{ booking.room.name }}</b></p>
          <p>{{ formatDate(booking.start_time) }} — {{ formatDate(booking.end_time) }}</p>
          <p>Цена: {{ booking.price }} ₽</p>
          <p v-if="booking.subscription">🔗 Подписка</p>
        </li>
      </ul>
      <p v-else>Нет бронирований</p>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProfilePage",
  data() {
    return {
      username: "",
      orders: [],
      subscriptions: [],
      bookings: [],
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("access_token");

        // Получаем профиль
        const userResp = await axios.get("http://127.0.0.1:8000/auth/users/me/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.username = userResp.data.username;

        // Получаем заказы
        const ordersResp = await axios.get("http://127.0.0.1:8000/books/orders/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.orders = ordersResp.data;

        // Подписки
        const subsResp = await axios.get("http://127.0.0.1:8000/zone/user-subscriptions/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.subscriptions = subsResp.data;

        // Бронирования
        const bookingsResp = await axios.get("http://127.0.0.1:8000/zone/bookings/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.bookings = bookingsResp.data;

      } catch (err) {
        console.error("Ошибка при загрузке профиля:", err);
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString("ru-RU");
    },
  },
  mounted() {
    this.fetchProfile();
  },
};
</script>

<style scoped>
.profile-page {
  padding: 2rem;
  max-width: 800px;
  margin: auto;
}

.profile-info {
  margin-bottom: 2rem;
  background: #f4f4f9;
  padding: 1rem;
  border-radius: 8px;
}

.profile-section {
  margin-bottom: 2rem;
}

.order-card,
.subscription-card,
.booking-card {
  background: #fff;
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
</style>
