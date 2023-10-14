<template>
  
    <nav class="navbar navbar-expand-lg navbar-dark bg-violet">
       
        <router-link class="navbar-brand" to="/" :class="{ active: isActive('/') }" > Home</router-link>
    
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav mr-auto">
            
            <li class="nav-item" v-if="status">
              <router-link class="nav-link" to="/profile" :class="{ active: isActive('/profile') }">Profile</router-link>
            </li>
            <li lass="nav-item" v-if="status && !admin">
              <router-link class="nav-link" to="/userBookings" :class="{ active: isActive('/profile') }">Your Bookings</router-link>
            </li>
            <li class="nav-item" v-if="admin && status">
                <router-link class="nav-link" to="/addMovie" :class="{ active: isActive('/addMovie') }" >Add a Movie</router-link>
              </li>
              <li class="nav-item" v-if="admin && status">
                <router-link class="nav-link" to="/addVenue" :class="{ active: isActive('/addVenue') }" >Add a Theatre</router-link>
              </li>
              <li class="nav-item" v-if="admin && status">
                <router-link class="nav-link" to="/visualize" :class="{ active: isActive('/visualize') }" >Visualize</router-link>
              </li>
              <li class="nav-item">
                <button class="btn btn-transparent" @click="regionOverlay=true">Search region</button>
              </li>
              <li class="nav-item">
                <button class="btn btn-transparent" @click="langOverlay=true">Search language</button>
              </li>
            
            <li v-if="!status" class="nav-item">
              <router-link class="nav-link" to="/login" active>Login</router-link>
            </li>
            <li v-if="!status" class="nav-item">
              <router-link class="nav-link" to="/register" active>Register</router-link>
            </li>
           
         
          </ul>
    
          <form class="form-inline my-2 my-lg-0">
            <input v-model="searchQuery" class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-success my-2 my-sm-0" type="button" @click="searchMovies">Search</button>
          </form>
          <button v-if="status" class="btn btn-danger ml-2" @click="logout" onclick="location.reload()">Logout</button>
        </div>
        <div v-if="regionOverlay" class="overlay">
          <div class="form-group">
            <label for="venues">Avaliable Regions</label>
            <select multiple class="form-control" id="venues" v-model="selectedRegion"  required>
              <option v-for="region in regions" >{{ region }}</option>
              
            </select>
            <button class="btn btn-primary" @click="searchRegions(selectedRegion[0])">OK</button>
          </div>
          
        </div>
        <div v-if="langOverlay" class="overlay">
          <div class="form-group">
            <label for="venues">Avaliable Languages</label>
            <select multiple class="form-control" id="venues" v-model="selectedLanguage"  required>
              <option v-for="lang in langs" >{{ lang }}</option>
              
            </select>
            <button class="btn btn-primary" @click="searchLanguages(selectedLanguage[0])">OK</button>
          </div>
          
        </div>
      </nav>
</template>

<script>
 import axios from 'axios';

 
// Set the base URL for all Axios requests
axios.defaults.baseURL = 'http://localhost:5000';
export default {
    data(){
      return{
        status : false,
        admin : this.$store.state.user.admin,
        searchQuery : '',
        regionOverlay : false,
        langOverlay : false,
        regions : [],
        langs : [],
        selectedRegion : [],
        selectedLanguage : []
      }
    },
    
    methods: {
      logout () {
      const user = {
        username : "",
        role : "",
        admin : false,
        public_id : "",
        access_token : "",
      }
      this.$store.commit('SET_USER', user);
      
        this.$router.push('/login')
      },
      isActive(route) {
      return this.$route.path === route;
    },
    async searchMovies(){
      const query = this.searchQuery;
      this.$router.push({ path: '/movies', query: { name: query }, replace: true });
    },
    async searchRegions(region){
      this.$router.push(`/region/${region}`)
      this.$router.go(0)
    },
    async searchLanguages(lang){
      this.$router.push(`/language/${lang}`)
      this.$router.go(0)
    },
    clearMessage(){
      this.regionOverlay = false
      this.langOverlay = false
    },
    async getRegions(){
      
      try{
        const res = await axios.get("/api/regions")
        this.regions = res.data
      }catch(e){
        this.error = e
      }
    },
    async getLanguages(){
      
      try{
        const res = await axios.get("/api/languages")
        this.langs = res.data
      }catch(e){
        this.error = e
      }
    }

  },
  mounted(){
    if(this.$store.state.user.access_token){
      this.status = true;
       
        
    }
    this.getRegions()
    this.getLanguages()
  }
    
  }
</script>

<style>
@media screen and (min-width: 777px) {
  .bg-violet{
    background-color: blueviolet;
  }
  .nav {
    padding: 30px;
  }
  .navbar {
    height: 60px;
  }

  .navbar-nav {
    flex-direction: row;
    align-items: center;
  }

  .navbar-brand {
    margin-right: auto;
  }

  .navbar-nav .nav-item {
    margin-left: 10px;
  }

  .form-inline {
    margin-right: 10px;
  }

  .btn-outline-danger {
    margin-left: 10px;
  }
}
</style>

<!-- <style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.active {
    /* Styles for the active link */
    color: yellow;
    /* Add any other styles you want to apply */
  }
nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

.nav-link.router-link-exact-active {
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #42b983;
}
.profile-picture-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #e9ecef;
}
.profile-picture {
  width: 50px; /* Adjust the size as needed */
  height: 50px; /* Adjust the size as needed */
  border-radius: 50%; /* Make the image round */
}
</style> -->
