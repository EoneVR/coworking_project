<template>
  <div class="analytics-page">
    <section class="hero">
      <h1>Аналитика</h1>
    </section>

    <div class="form">
      <label>
        Источник отчёта:
        <select v-model="source">
          <option value="bookshop">Магазин</option>
          <option value="coworking">Коворкинг</option>
        </select>
      </label>

      <label>
        Тип отчёта:
        <select v-model="reportType">
          <option value="revenue">Доход</option>
          <option value="orders_count">Количество заказов</option>
          <option value="top_books">Топ книг</option>
          <option value="avg_check">Средний чек</option>
          <option value="monthly_sales">Месячные продажи</option>
          <option value="room_usage">Загрузка комнат</option>
          <option value="popular_room_types">Популярные типы комнат</option>
          <option value="subscriptions_usage">Подписки</option>
          <option value="avg_duration">Средняя длительность</option>
          <option value="monthly_stats">Месячная статистика</option>
        </select>
      </label>

      <label>
        Начало периода:
        <input type="date" v-model="startDate" />
      </label>

      <label>
        Конец периода:
        <input type="date" v-model="endDate" />
      </label>

      <button @click="fetchReport">Сформировать</button>
    </div>

    <div class="result" v-if="report">
      <h2>Результат отчёта:</h2>
      <pre>{{ report }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AnalyticsPage",
  data() {
    return {
      source: "bookshop",
      reportType: "revenue",
      startDate: "",
      endDate: "",
      report: null,
    };
  },
  methods: {
    async fetchReport() {
      try {
        let url =
          this.source === "bookshop"
            ? "http://localhost:8000/analytics/analytics_for_bookshop/"
            : "http://localhost:8000/analytics/analytics_for_coworking/";

        const res = await axios.get(url, {
          params: {
            start_date: this.startDate,
            end_date: this.endDate,
            report_type: this.reportType,
          },
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        this.report = res.data;
      } catch (error) {
        console.error("Ошибка загрузки отчёта:", error);
        this.report = { error: "Не удалось получить отчёт" };
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

.form {
  display: grid;
  gap: 1rem;
  max-width: 400px;
  margin: 2rem auto;
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

button {
  padding: 0.6rem 1rem;
  background: #3c8dbc;
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

button:hover {
  background: #2a6f99;
}

.result {
  margin: 2rem auto;
  max-width: 700px;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 12px;
  white-space: pre-wrap;
}
</style>
