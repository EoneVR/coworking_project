<template>
  <div class="booking-page">
    <section class="hero">
      <h1>Бронирование помещений</h1>
    </section>

    <section class="form-section">
      <form @submit.prevent="createBooking">
        <div class="form-group">
          <label>Помещение</label>
          <select v-model="form.room" required>
            <option disabled value="">-- Выберите помещение --</option>
            <option v-for="room in rooms" :key="room.id" :value="room.id">
              {{ room.title }} ({{ room.room_type }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Начало брони</label>
          <input type="datetime-local" v-model="form.start_time" required />
        </div>

        <div class="form-group">
          <label>Окончание брони</label>
          <input type="datetime-local" v-model="form.end_time" required />
        </div>

        <div class="form-group" v-if="subscriptions.length > 0">
          <label>Использовать подписку</label>
          <select v-model="form.subscription">
            <option :value="null">Не использовать</option>
            <option v-for="sub in subscriptions" :key="sub.id" :value="sub.id">
              {{ sub.subscription.title }} (до {{ sub.end_date }})
            </option>
          </select>
        </div>

        <button type="submit" class="btn">Забронировать</button>
      </form>
    </section>

    <section class="bookings" v-if="bookings.length > 0">
      <h2>Мои бронирования</h2>
      <div class="grid">
        <div class="card" v-for="booking in bookings" :key="booking.id">
          <h3>{{ booking.room.title }}</h3>
          <p><strong>Начало:</strong> {{ formatDate(booking.start_time) }}</p>
          <p><strong>Конец:</strong> {{ formatDate(booking.end_time) }}</p>
          <p><strong>Цена:</strong> {{ booking.price }} ₽</p>
          <p v-if="booking.subscription">
            <strong>Подписка:</strong> {{ booking.subscription.subscription.title }}
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BookingPage",
  data() {
    return {
      rooms: [],
      subscriptions: [],
      bookings: [],
      form: {
        room: "",
        start_time: "",
        end_time: "",
        subscription: null
      }
    };
  },
  async mounted() {
    try {
      // Загружаем комнаты
      const roomsRes = await axios.get("http://localhost:8000/zone/rooms/");
      this.rooms = roomsRes.data.results || roomsRes.data;

      // Загружаем активные подписки пользователя
      const subsRes = await axios.get("http://localhost:8000/zone/user_subscriptions/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
      });
      this.subscriptions = subsRes.data;

      // Загружаем бронирования пользователя
      const bookingsRes = await axios.get("http://localhost:8000/zone/bookings/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
      });
      this.bookings = bookingsRes.data.results || bookingsRes.data;
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
  },
  methods: {
    async createBooking() {
  try {
    const res = await axios.post(
      "http://localhost:8000/zone/bookings/checkout/",
      this.form,
      {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
      }
    );

    if (res.data.checkout_url) {
      // Переход на оплату
      window.location.href = res.data.checkout_url;
    } else {
      // Бесплатная бронь
      alert(res.data.message || "Бронирование успешно создано!");
      this.bookings.push(res.data);
    }
  } catch (error) {
    console.error("Ошибка при создании бронирования:", error.response?.data || error);
    alert("Не удалось создать бронирование.");
  }
},
    formatDate(dateString) {
      const options = { dateStyle: "short", timeStyle: "short" };
      return new Date(dateString).toLocaleString(undefined, options);
    }
  }
};
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #3c3c5c, #1e1e2f);
  color: white;
}

.form-section {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.4rem;
}

.form-group select,
.form-group input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.btn {
  display: inline-block;
  background: #3c8dbc;
  color: white;
  border: none;
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}
.btn:hover {
  background: #2a6f99;
}

.bookings {
  margin: 2rem auto;
  max-width: 1200px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
</style>
