<template>
  <div class="auth-container">
    <h2>{{ isLogin ? "Вход" : "Регистрация" }}</h2>

    <!-- Форма входа -->
    <form v-if="isLogin" @submit.prevent="login">
      <div>
        <label>Логин:</label>
        <input v-model="username" type="text" required />
      </div>
      <div>
        <label>Пароль:</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">Войти</button>
      <p class="switch" @click="isLogin = false">Нет аккаунта? Зарегистрироваться</p>
    </form>

    <!-- Форма регистрации -->
    <form v-else @submit.prevent="register">
      <div>
        <label>Логин:</label>
        <input v-model="username" type="text" required />
      </div>
      <div>
        <label>Email:</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>Пароль:</label>
        <input v-model="password" type="password" required />
      </div>
      <div>
        <label>Повторите пароль:</label>
        <input v-model="password2" type="password" required />
      </div>
      <button type="submit">Зарегистрироваться</button>
      <p class="switch" @click="isLogin = true">У меня уже есть аккаунт</p>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AuthPage",
  data() {
    return {
      isLogin: true, // по умолчанию форма входа
      username: "",
      email: "",
      password: "",
      password2: "",
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:8000/auth/jwt/create", {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem("access_token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);

        this.$router.push("/");
      } catch (err) {
        this.error = "Неверный логин или пароль";
      }
    },

    async register() {
      if (this.password !== this.password2) {
        this.error = "Пароли не совпадают";
        return;
      }
      try {
        await axios.post("http://localhost:8000/auth/users/", {
          username: this.username,
          email: this.email,
          password: this.password,
        });

        // После успешной регистрации — сразу входим
        await this.login();
      } catch (err) {
        this.error = "Ошибка регистрации";
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.error {
  color: red;
  margin-top: 10px;
}
button {
  margin-top: 15px;
  padding: 10px;
  width: 100%;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
button:hover {
  background: #369f6f;
}
.switch {
  margin-top: 10px;
  text-align: center;
  color: #42b883;
  cursor: pointer;
}
.switch:hover {
  text-decoration: underline;
}
</style>
