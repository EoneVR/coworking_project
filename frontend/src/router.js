import {createRouter, createWebHistory} from "vue-router";
import Home from "./pages/home_page.vue";
import Shop from "./pages/shop_page.vue";
import Book from "./pages/books.vue";
import Book_detail from "./pages/book_detail.vue";
import Book_edit from "./pages/book_edit.vue";
import Login from "./pages/login.vue";
import Cart from "./pages/cart.vue";
import Checkout from "./pages/checkout.vue";
import Coffeeshop from "./pages/coffeeshop.vue";
import Coffee from "./pages/coffee.vue";
import Bakery from "./pages/bakery.vue";
import Analytics from "./pages/report_page.vue";
import Coworking from "./pages/coworking.vue";
import Booking from "./pages/booking.vue";
import Profile from "./pages/profile.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "/", name: "home", component: Home},
    {path: "/shop", name: "shop", component: Shop},
    {path: "/shop/books", name: "shop-books", component: Book},
    {path: "/shop/books/:id", name: "book-detail", component: Book_detail},
    {path: "/shop/books/:id/edit", name: "book-edit", component: Book_edit},
    {path: "/cart", name: "cart", component: Cart},
    {path: "/checkout", name: "checkout", component: Checkout},
    
    {path: "/login", name: "login", component: Login},
    {path: "/profile", name: "profile", component: Profile},
    
    {path: "/coffeeshop", name: "coffeshop", component: Coffeeshop},
    {path: "/coffeeshop/coffee", name: "coffeshop-coffe", component: Coffee},
    {path: "/coffeeshop/bakery", name: "coffeshop-bakery", component: Bakery},
    
    {path: "/analytics", name: "analytics", component: Analytics},
    
    {path: "/coworking", name: "coworking", component: Coworking},
    {path: '/coworking/booking', name: "coworking-booking", component: Booking}
  ],
  linkActiveClass: "active",
});

export default router;