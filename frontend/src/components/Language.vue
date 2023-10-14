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
                    <div class="movie-lang">{{ movie.language }}</div>
                    <p class="movie-ratings">Ratings: {{ movie.ratings }}</p>
                    <ul class="movie-tags">
                      <p> {{ movie.tags }}</p>
                    </ul>
                   
                  </div>
                </div>
              </div>
            </div>
           
          </div>
    </div>
</template>

<script>
 import axios from 'axios';


axios.defaults.baseURL = 'http://localhost:5000';
export default{
    data(){
        return {
            lang : this.$route.params.name,
            movies: [],
        }
    },
    mounted(){
        this.fetchShowsLanguages()
    },
    methods : {
       async fetchShowsLanguages(){
        try{
            const res = await axios.get(`/api/search_lang/${this.lang}`)
            this.movies = res.data
            console.log(res.data)
            const baseUrl = 'http://localhost:5000';
          const modifiedMovies = res.data.map((movie) => {
          return {
          ...movie,
          show_pic: baseUrl + "/static/shows" + movie.show_pic,
        };
      
        
});
            this.movies = modifiedMovies;

        }catch(e){
            this.error = e
        }
       }
    }
}
</script>