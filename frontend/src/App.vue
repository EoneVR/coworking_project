<template>
  <div id="app">
    <AppNavbar :isAdmin="isAdmin" :isAuthenticated="isAuthenticated" :cartCount="cartCount" />
    <router-view />
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue'

export default {
  name: 'App',    // <-- должно быть App
  components: { AppNavbar },
  data() {
    return {
      isAdmin: true,
      isAuthenticated: true,
      cartCount: 2
    }
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-color: #f9f9f9;
}
</style>
