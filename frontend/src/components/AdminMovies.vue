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
                        <button v-if="!role" class="btn btn-success" @click="rateShow(movie.show_id)">Rate it!!</button>
                         
                            <button v-if="role" @click="openEditModal(movie)" class="btn btn-outline-warning">Edit</button>
                            
                            <button v-if="role" @click="deleteMovie(movie)" class="btn btn-outline-danger">Delete</button>
                        
                          <button v-if="role" @click="exportCsvShows(movie.show_id)" class="btn btn-outline-success">Export</button>
                        
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="showRateOverlay" class="overlay">
                  <div class="box">
                    <form @submit.prevent="rateMovie">
                      <div class="form-row">
                        <div class="form-col">
                        <div class="form-group">
                          <label for="ratings">Give your Ratings out of 10</label>
                          <input type="range" class="form-control" id="ratings" v-model="ratings" min="0" max="10" step="0.01">
                          <span>{{ ratings }}</span>
                        </div>
                        </div>
                        
                      </div>
                    </form>
                    <div class="modal-footer">
                      <button class="btn btn-success" @click="rateMovie">Submit</button>
                    <button class="btn btn-danger" @click="clearMessage">Cancel</button>
                  </div>
                  </div>
                </div>
               
              </div>
              <div v-if="showEditModal" class="overlay">
                <div class="box">
                  <h5 class="modal-title">Edit Movie {{currentEditMovie}}</h5>
                  <button type="button" class="close" @click="closeEditModal">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <div class="modal-body">
                    <form>
                      <div class="form-group">
                        <label for="edit-movie-name">Movie Name</label>
                        <input type="text" class="form-control" id="edit-movie-name" v-model="editMovieName">
                      </div>

                      <div class="form-group">
                        <label for="price">Add an Image</label>
                       
                        <div>
                          <input type="file" @change="handleFileUpload">
                         
                       
                          <img :src="imageUrl" alt="Movie Image" v-if="imageUrl">
                        </div>
                        <div class="form-group">
                          <label for="venues">Venues</label>
                          <select multiple class="form-control" id="venues" v-model="selectedVenues" required>
                            <option v-for="venue in venues" :value="venue.id" :key="venue.id">{{ venue.name }}</option>
                          </select>
                        </div>
                        </div>
                        <div class="form-group">
                          <label for="startTime">Timings</label>
                          <div class="time-input-group">
                            <input type="time" class="form-control" id="startTime" v-model="startTime" required>
                            <span class="time-input-separator">-</span>
                            <input type="time" class="form-control" id="endTime" v-model="endTime" required>
                          </div>
                        </div>
                        
                          <div class="form-group">
                            <label for="price">Price</label>
                            <div class="input-group">
                              <div class="input-group-prepend">
                                <span class="input-group-text">₹</span>
                              </div>
                              <input type="number" class="form-control" id="price" v-model="price" step="0.01" required>
                            </div>
                            </div>
                          
                    
                      <div class="form-group">
                        <label for="edit-movie-description">Description</label>
                        <textarea class="form-control" id="edit-movie-description" v-model="editMovieDescription"></textarea>
                      </div>
                     
                    </form>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-success" @click="saveMovieChanges(currentEditId)">Save Changes</button>
                    <button type="button" class="btn btn-danger" @click="closeEditModal">Cancel</button>
                  </div>
                </div>
                 
              </div>

              <div v-if="showOverlay" class="overlay">
                <div class="overlay-content">
                  <p>Movie added successfully!</p>
                 
                  <div v-if="showOverlay" class="overlay">
                    <div class="box">
                      <div class="success-message" style="color:green">{{ message }}</div>
                      <button class="btn btn-primary" @click="clearMessage">OK</button>
                    </div>
                  </div>
                  
                </div>
                </div>

                <div v-if="deleteOverlay" class="overlay">
                  <div class="box">
                    <div class="modal-body">
                   Are you sure you want to delete this movie {{ currentEditMovie }}? 
                   This cannot be changed later.
                   </div>
                   <div class="modal-footer">
                    <button type="button" class="btn btn-danger" @click="deleteMovieApi(currentEditId)">Delete</button>
                    <button type="button" class="btn btn-success" @click="closeDeleteModal">No, I have changed my mind</button>
                  </div>
                  </div>
                </div> 
                <div v-if="successOverlay" class="overlay">
                  <div class="box">
                    <div class="success-message" style="color:green">{{ message }}</div>
                    <button class="btn btn-primary" @click="clearMessage">OK</button>
                  </div>
                </div>
                

    <div v-if="error" class="overlay">
      <div class="box">
        <div class="error-message" style="color:red">{{ error }}</div>
        <button class="btn btn-primary" @click="clearMessage">OK</button>
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
        adminUsername: '',
        role : this.$store.state.user.admin,
        movies: [] ,
        currentEditId : '',
        showOverlay: false,
        error: '',
        showEditModal: false,
        currentEditMovie : "",
        editMovieId: null,
      editMovieName: '',
      editMovieDescription: '',
        imageUrl : '',
        editMoviePicture : '',
        deleteOverlay : false,
        venues : [],
        selectedVenues : [],
        startTime : '',
        endTime : '',
        price : 0,
        showRateOverlay : false,
        showId : "",
        ratings : 5,
        message : '',
        successOverlay : false,
      };
    },
    created() {
      // Get the admin's username from the route params
      this.adminUsername = this.$store.state.user.username;
      // Fetch the movies created by the admin
      this.fetchAdminMovies();
    },
    
    mounted(){
      const token = this.$store.state.user.access_token
        if (!token) {
        this.$router.push('/login')
        return
        }
        
    },

    methods: {
      rateShow(show_id){
    this.showRateOverlay = true
    this.showId = show_id
  },
  async rateMovie(){
    console.log("Hello")
    const token = this.$store.state.user.access_token
    const data = {
          ratings : this.ratings
        }
    try{
      const response = await axios.put(`/ratings/${this.showId}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        
      })
      this.message = response.data.message
      this.successOverlay = true
      
    }catch(error){
          this.error = error;
        }
  },
      fetchAdminMovies() {
        const token = this.$store.state.user.access_token
        if(!token){
          this.$router.push('/login')
          return
        }
        // Make an HTTP request to fetch the movies created by the admin
        axios.get(`/api/show`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
          .then(response => {
            console.log(response.data)
            const baseUrl = 'http://localhost:5000';
          const modifiedMovies = response.data.map((movie) => {
          return {
          ...movie,
          show_pic: baseUrl + "/static/shows" + movie.show_pic,
        };
        
});
            this.movies = modifiedMovies;
            console.log(this.movies[0].show_pic)
          })
          .catch(error => {
            console.error(error);
          });
          
  
      },
      async fetchVenues(show_id){
        
      const token = this.$store.state.user.access_token
        if (!token) {
        this.$router.push('/login')
        return
        }
        try{
        const response = await axios.get('/api/venue', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
      
      })
      this.venues = []
      const my_venues = response.data
      
      for(let i = 0; i < my_venues.length; i++ ){
        this.venues.push({
          'id' : my_venues[i].venue_id,
          'name' : my_venues[i].venue_name
        })
      }
      console.log(this.venues)
        }catch(error){
          console.log(error)
        }

    },
      openEditModal(movie) {
        this.currentEditMovie = movie.show_name
        this.currentEditId = movie.show_id
        console.log(this.showEditModal)
      this.showEditModal = true;
      console.log(this.showEditModal)
      this.fetchVenues(movie.show_id)
      
    },
    closeEditModal() {
      this.showEditModal = false;
      this.editMovieId = null;
      this.editMovieName = '';
      this.editMovieDescription = ''
      this.editMoviePicture = ''
    },
    closeDeleteModal() {
      
      this.deleteOverlay = false;
      
    },
    async saveMovieChanges(show_id) {
      const token = this.$store.state.user.access_token
      const timings = `${this.startTime} - ${this.endTime}`;
      console.log(this.selectedVenues)
      const show_attributes = [
        {name :  'show_name', value : this.editMovieName},
        {name :  'description', value : this.editMovieDescription},
        {name :  'timings', value : timings},
        {name :  'venues', value : this.selectedVenues},
        {name : 'price', value : this.price}

      ]
      
      const formData = new FormData();
      show_attributes.forEach(attribute => {
        formData.append(attribute.name, attribute.value);
      });
      console.log(formData)
      formData.append('show_pic', this.editMoviePicture);
      try{
        const response = await axios.put(`/api/show/${show_id}`, formData,{
        headers: {
            Authorization: `Bearer ${token}`
        }
        })
        this.message = response.data.message;
        this.showOverlay = true
      }catch(error){
        this.error = error
      }
      
      this.closeEditModal();
    },
    deleteMovie(movie) {
      this.currentEditMovie = movie.show_name
      this.currentEditId = movie.show_id
      this.deleteOverlay = true
      console.log(this.deleteOverlay)
    
    },
    async deleteMovieApi(movieId){
      const token = this.$store.state.user.access_token
      const url = "/api/show/" + movieId
      console.log(url)
      try{
        const response = await axios.delete(url, {
        headers: {
            Authorization: `Bearer ${token}`
        }
        })
        this.message = response.data.message;
        this.deleteVenueOverlay = false
        this.successOverlay = true
      }catch(error){
        this.error = error
      }
    },
      clearMessage() {
        this.showOverlay = false;
        this.showRateOverlay = false
        this.successOverlay = false
        window.location.reload();
      },
      handleFileUpload(event) {
      this.editMoviePicture = event.target.files[0];
      const file = event.target.files[0];
      this.imageUrl = URL.createObjectURL(file);
    
    },
    async exportCsvVenue(venueId) {
      try {
        const response = await axios.get(`/export_csv_venue/${venueId}`, {
          responseType: 'blob',  
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });

  
        const url = window.URL.createObjectURL(new Blob([response.data]));

      
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `venue_${venueId}_details.csv`);
        document.body.appendChild(link);
        link.click();

        URL.revokeObjectURL(url);
        document.body.removeChild(link);
    } catch (error) {
        console.log(error);
      }
},
async exportCsvShows(showId) {
      try {
        const response = await axios.get(`/export_csv_show/${showId}`, {
          responseType: 'blob',  
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });

        const url = window.URL.createObjectURL(new Blob([response.data]));

        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `show_${showId}_details.csv`);
        document.body.appendChild(link);
        link.click();

 
        URL.revokeObjectURL(url);
        document.body.removeChild(link);
    } catch (error) {
        console.log(error);
      }
},

    }
  };
  </script>
  
  <style>
  .movies-list {
    margin-top: 20px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .movie-item {
    width: calc(20% - 20px);
    margin-bottom: 20px;
  }
  
  .movie-image-container {
    position: relative;
    margin-bottom: 10px;
  }
  
  .movie-image {
    width: 200px;
    height: 300px;
  
  }
  
  .movie-details-box {
    background-color: rgba(242, 242, 242, 0.9);
    padding: 10px 20px;
    border-radius: 5px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 300px;
    opacity: 0;
    transition: all 0.3s ease;
    z-index: 1;
  }
  
  .movie-item:hover .movie-details-box {
    opacity: 1;
  }
  
  .movie-details {
    margin-top: 10px;
  }
  
  .movie-name {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .movie-price,
  .movie-ratings {
    margin-bottom: 5px;
  }
  
  .movie-tags {
    margin-top: 5px;
    list-style: none;
    padding: 0;
  }
  
  .movie-tags li {
    display: inline-block;
    margin-right: 5px;
    background-color: #ccc;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 12px;
    color: #fff;
  }
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
  .modal-body {
    max-height: 500px;
    overflow-y: auto;
  }
  
  .modal-footer {
    justify-content: flex-start;
  }
</style>






