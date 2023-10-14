import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from '../components/Login.vue';
import Protected from '../components/Protected.vue';
import Register from '../components/Register.vue';
import Home from '../components/Home.vue';
import AddMovie from '../components/AddMovie.vue';
import AddVenue from '../components/AddVenue.vue';
import AdminMovies from '../components/AdminMovies.vue';
import ShowVenues from '../components/ShowVenues.vue';
import Seating from '../components/Seating.vue';
import store from '@/store/index.js';
import Unauthorized from '../components/Unauthorized.vue'
import BookingDetails from '../components/BookingDetails.vue';
import MovieList from '../components/MovieList.vue'
import FetchVenues from '../components/FetchVenues.vue'
import Visualization from '../components/Visualization.vue'
import Region from '../components/Region.vue'
import Language from '../components/Language.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  {
    path: '/region/:name',
    name: 'region',
    component: Region,
  },
  {
    path: '/language/:name',
    name: 'language',
    component: Language,
  },
  {
    path : '/visualize',
    name : 'visualize',
    component : Visualization,
    meta: { requiresAuth: true,
      requiresAdmin: true
     },
  },
  {
    path: '/addVenue',
    name: 'addVenue',
    component: AddVenue,
    meta: { requiresAuth: true,
            requiresAdmin: true
           },
  },
  {
    path: '/addMovie',
    name: 'addMovie',
    component: AddMovie,
    meta: { requiresAuth: true, 
            requiresAdmin: true
     },
  },
  {
    path: '/login',
    name : 'login',
    component: Login,
  },
  {
    path: '/profile',
    name: 'protected',
    component: Protected,
    meta: { requiresAuth: true },
  },
 
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/allmovies',
    name: 'AdminMovies',
    component: AdminMovies,
    meta: { requiresAuth: true },
  },
  {
    path: '/venues/:show_id',
    name: 'ShowVenues',
    component: ShowVenues,
    meta: { requiresAuth: true },
  },
  {
    path: '/showvenues/:showvenue_id',
    name: 'Seating',
    component: Seating,
    meta: { requiresAuth: true },
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: Unauthorized,
    
  },
  {
    path: '/userBookings',
    name : 'BookingDetails',
    component : BookingDetails
  },
  { 
    path: '/movies', 
    component: MovieList,
    props: (route) => ({ query: route.query.name })
  },
  {
    path: '/venueList',
    name : 'FetchVenues',
    component : FetchVenues
  },

  
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

// router.beforeEach((to, from, next) => {
//   if (to.path === from.path) {
//     next(false); // prevent navigation
//   } else {
//     next(); // allow navigation
//   }
// });

router.beforeEach((to, from, next) => {
  const loggedIn = store.state.user.access_token
  const isAdmin = store.state.user.admin

  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (!loggedIn || !isAdmin) {
      
      next(loggedIn ? '/unauthorized' : '/login');
    } else {
      
      next();
    }
  } else {

    next();
  }
});



export default router;
