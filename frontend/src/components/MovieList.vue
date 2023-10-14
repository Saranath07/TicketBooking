<template>
    <div>
      
      <navbar></navbar>
     
      <div class="movies-list">
        <div v-for="movie in movies" :key="movie.id" class="movie-item">
          <div class="movie-image-container">
            <router-link :to="`/venues/${movie.show_id}`">
            <img :src="movie.show_pic" alt="Movie Poster" class="movie-image">
          </router-link>
            <div class="movie-details-box">
              <div class="movie-details">
                <div class="movie-name">{{ movie.show_name }}</div>
                
                <p class="movie-ratings">Ratings: {{ movie.ratings }}</p>
                <ul class="movie-tags">
                  <p> {{ movie.tags }}</p>
                </ul>
                <button class="btn btn-success">Ratings</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="error" class="overlay">
        <div class="box">
          <div class="error-message" style="color:red">{{ error }}</div>
          <button class="btn btn-primary" @click="clearErrorMessage">OK</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
   import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:5000';
  export default {
    data() {
      return {
        movies: [
            {'id' : 1,
            'name' : 'ExampleMovie'}
        ],
        showOverlay: false,
        error: '',
      };
    },
    mounted() {
      this.fetchMovies();
      console.log(this.$route.query)
    },
    methods: {
      async fetchMovies() {
       
        try{
        const response = await axios.get("/api/search_movies",{
        params : { name: this.$route.query.name }
      })
      console.log(response)
      
      const baseUrl = 'http://localhost:5000';
          const modifiedMovies = response.data.map((movie) => {
          return {
          ...movie,
          show_pic: baseUrl + "/static/shows" + movie.show_pic,
        };
        
    });
        this.movies = modifiedMovies

      }catch(error){
        console.log(error)
      }
      },
      clearMessage() {
        this.showOverlay = false;
        this.$router.push("/profile")
      }
    },
   
    
  };
  </script>

<style>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; 
}

.box {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}
.success-message{
  color: green;
  margin-bottom: 10px;
}

.error-message {
  color: red;
  margin-bottom: 10px;
}
</style>