<template>
  <nav class="navbar">
    <div class="logo">Coworking Space</div>

    <ul class="nav-links">
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/coworking">Коворкинг</router-link></li>
      <li><router-link to="/coffeeshop">Кофейня</router-link></li>
      <li><router-link to="/shop">Магазин</router-link></li>
      <li v-if="isAdmin"><router-link to="/analytics">Аналитика</router-link></li>
    </ul>

    <div class="nav-actions">
      <!-- Если пользователь авторизован -->
      <template v-if="isAuthenticated">
        <router-link to="/cart" class="cart">
          🛒 <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
        </router-link>
        <router-link to="/profile" class="profile">👤</router-link>
        <button @click="logout" class="auth-btn logout">Выход</button>
      </template>

      <!-- Если пользователь не авторизован -->
      <button v-else @click="goToLogin" class="auth-btn">Войти</button>
    </div>
  </nav>
</template>

<script>
export default {
  name: "AppNavbar",
  data() {
    return {
      isAuthenticated: !!localStorage.getItem("access_token"), // сразу проверка токена
      isAdmin: true, // можешь доработать, если у тебя роли есть в токене
      cartCount: 0,
    };
  },
  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.isAuthenticated = false; // обновляем локальное состояние
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1e1e2f;
  color: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.logo {
  font-size: 1.4rem;
  font-weight: bold;
  color: #ffcc00;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  list-style: none;
}

.nav-links a {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: #ffcc00;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cart {
  position: relative;
  font-size: 1.3rem;
  color: #fff;
  text-decoration: none;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -12px;
  background: #ff4d4d;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  border-radius: 50%;
  padding: 3px 6px;
}

.auth-btn {
  background: #ffcc00;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

.auth-btn:hover {
  background: #ffdb4d;
}

.logout {
  background: #ff4d4d;
}

.logout:hover {
  background: #ff6666;
}

.profile {
  font-size: 1.5rem;
  color: #fff;
  text-decoration: none;
  position: relative;
  transition: color 0.2s;
}

.profile:hover {
  color: #ffcc00;
}
</style>
