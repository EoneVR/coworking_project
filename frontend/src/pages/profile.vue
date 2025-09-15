<template>
  <div class="profile-page">
    <h1>👤 Профиль</h1>

    <!-- Логин -->
    <section class="profile-info">
      <p><strong>Логин:</strong> {{ username }}</p>
    </section>

    <!-- Заказы -->
    <section class="profile-section">
      <h2>
        📚 Мои заказы
        <button class="toggle-btn" @click="showOrders = !showOrders">
          {{ showOrders ? "Скрыть" : "Показать" }}
        </button>
      </h2>

      <transition name="fade">
        <ul v-if="showOrders && orders.length > 0" class="order-list">
          <li v-for="order in orders" :key="order.id" class="order-card">
            <p>
              Заказ #{{ order.id }} — <b>{{ order.payment_status }}</b>
              ({{ formatDate(order.placed_at) }})
            </p>
            <ul>
              <li v-for="item in order.items" :key="item.id">
                {{ item.book_title }} — {{ item.quantity }} шт. × {{ item.unit_price }} ₽
              </li>
            </ul>
          </li>
        </ul>
      </transition>

      <p v-if="showOrders && orders.length === 0">Нет заказов</p>
    </section>

    <!-- Подписки -->
    <section class="profile-section">
      <h2>
        🎟 Мои подписки
        <button class="toggle-btn" @click="showSubscriptions = !showSubscriptions">
          {{ showSubscriptions ? "Скрыть" : "Показать" }}
        </button>
      </h2>

      <transition name="fade">
        <ul v-if="showSubscriptions && subscriptions.length > 0" class="subscription-list">
          <li v-for="sub in subscriptions" :key="sub.id" class="subscription-card">
            <p><b>{{ sub.subscription.title }}</b></p>
            <p>с {{ sub.start_date }} до {{ sub.end_date }}</p>
            <p v-if="sub.is_active">✅ Активна (осталось {{ daysLeft(sub.end_date) }} дней)</p>
            <p v-else>❌ Истекла</p>
          </li>
        </ul>
      </transition>

      <p v-if="showSubscriptions && subscriptions.length === 0">Нет подписок</p>
    </section>

    <!-- Бронирования -->
    <section class="profile-section">
      <h2>
        🏠 Мои брони
        <button class="toggle-btn" @click="showBookings = !showBookings">
          {{ showBookings ? "Скрыть" : "Показать" }}
        </button>
      </h2>

      <transition name="fade">
        <ul v-if="showBookings && bookings.length > 0" class="booking-list">
          <li v-for="booking in bookings" :key="booking.id" class="booking-card">
            <p><b>{{ booking.room.title }}</b></p>
            <p>{{ formatDate(booking.start_time) }} — {{ formatDate(booking.end_time) }}</p>
            <p>Цена: {{ booking.price }} ₽</p>
            <p v-if="booking.subscription">🔗 Подписка</p>
          </li>
        </ul>
      </transition>

      <p v-if="showBookings && bookings.length === 0">Нет бронирований</p>
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
      // состояния шторок
      showOrders: false,
      showSubscriptions: false,
      showBookings: false,
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
        this.subscriptions = subsResp.data.results;

        // Бронирования
        const bookingsResp = await axios.get("http://127.0.0.1:8000/zone/bookings/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.bookings = bookingsResp.data.results;

      } catch (err) {
        console.error("Ошибка при загрузке профиля:", err);
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString("ru-RU");
    },
    daysLeft(endDate) {
      const today = new Date();
      const end = new Date(endDate);
      const diffTime = end - today;
      return Math.max(0, Math.ceil(diffTime / (1000 * 60 * 60 * 24)));
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

.toggle-btn {
  margin-left: 1rem;
  padding: 0.2rem 0.6rem;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  background: #007bff;
  color: white;
  transition: background 0.3s;
}
.toggle-btn:hover {
  background: #0056b3;
}

/* Анимация плавного появления/скрытия */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
