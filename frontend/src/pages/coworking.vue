<template>
  <div class="coworking-page">
    <section class="hero">
      <h1>Коворкинг</h1>
    </section>

    <!-- Секция комнат -->
    <section class="rooms">
      <h2>Наши помещения</h2>
      <div class="grid">
        <div v-for="room in rooms" :key="room.id" class="card">
          <img v-if="room.image" :src="room.image" :alt="room.title" />
          <div class="content">
            <h3>{{ room.title }}</h3>
            <p><strong>Тип:</strong> {{ room.room_type }}</p>
            <p><strong>Описание:</strong> {{ room.description }}</p>
            <p><strong>Вместимость:</strong> {{ room.capacity }} чел.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Секция подписок -->
    <section class="subscriptions">
      <h2>Подписки</h2>
      <div class="grid">
        <div v-for="sub in subscriptions" :key="sub.id" class="card">
          <img v-if="sub.image" :src="sub.image" :alt="sub.title" />
          <div class="content">
            <h3>{{ sub.title }}</h3>
            <p><strong>Длительность:</strong> {{ sub.duration }}</p>
            <p><strong>Цена:</strong> {{ sub.price }} ₽</p>
            <button @click="buySubscription(sub.id)" class="buy-btn">
              Купить
            </button>
          </div>
        </div>
      </div>
    </section>
    <section class="booking-btn-section">
  <router-link to="/coworking/booking" class="booking-btn">Забронировать</router-link>
</section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CoworkingPage",
  data() {
    return {
      rooms: [],
      subscriptions: [],
    };
  },
  async mounted() {
    try {
      const roomsRes = await axios.get("http://localhost:8000/zone/rooms/");
      this.rooms = roomsRes.data.results;

      const subsRes = await axios.get("http://localhost:8000/zone/subscriptions/");
      this.subscriptions = subsRes.data.results;
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
  },
  methods: {
    async buySubscription(subscriptionId) {
      try {
        const res = await axios.post(
          `http://localhost:8000/zone/subscriptions/${subscriptionId}/checkout/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        // ✅ Бэк вернул checkout_url → редирект
        window.location.href = res.data.checkout_url;
      } catch (error) {
        console.error("Ошибка при создании сессии:", error);
        alert("Не удалось создать подписку. Попробуйте ещё раз.");
      }
    },
  },
};
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #3c3c5c, #1e1e2f);
  color: white;
}

section {
  text-align: center;
  margin: 2rem auto;
  max-width: 1200px;
  padding: 1rem;
}

h2 {
  margin-bottom: 1rem;
  text-align: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.card {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-6px);
}

.card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.content {
  padding: 1.2rem;
}

.buy-btn {
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background: #3c3c5c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.buy-btn:hover {
  background: #2a2a45;
}

.booking-btn-section {
  display: flex;
  justify-content: center;
  margin: 3rem 0;
}

.booking-btn {
  display: inline-block;
  background: linear-gradient(135deg, #3c3c5c, #1e1e2f);
  color: white;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 12px;
  text-decoration: none;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.booking-btn:hover {
  background: linear-gradient(135deg, #4a4a7a, #2a2a45);
  transform: translateY(-3px);
}
</style>

