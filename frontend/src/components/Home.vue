<template>
    <div>
        <navbar></navbar>
        <!-- <navbar1></navbar1> -->

        
        <div v-if="role && username">
            {{username}}'s Home Page
            <br>
            You are an Admin
         <h2 v-if="movies.length!=0">Your Movies</h2>
            <div v-if="movies" class="movies-list">
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
                     
                         
                          <button @click="exportCsvShows(movie.show_id)" class="btn btn-outline-success">Export</button>
                     
                      </div>
                    </div>
                  </div>
                </div>
               
              </div>
              <div v-if="movies.length==0">
                <h1>No movies added yet</h1>
              </div>
              <router-link to="/allmovies" class="btn btn-primary">View More Movies</router-link>
              <h2 >Your Venues</h2>
              <div  class="venues-container">
              <div
                v-for="venue in venues"
                :key="venue.venue_id"
                class="venue-item"
              >
                <div class="venue-details">
                  <h2 class="venue-name">{{ venue.venue_name }}</h2>
                  <div>
                    <p class="venue-location">{{ venue.location }}</p>
                    <p class="venue-capacity">Capacity: {{ venue.capacity }}</p>
                  </div>
                  <p class="venue-description">{{ venue.venue_description }}</p>
                  <button @click="exportCsvVenue(venue.venue_id)" class="btn btn-outline-success">Export</button>
                  <button @click="deleteVen(venue.venue_id)" class="btn btn-outline-danger">Delete Venue</button>  
                  <button @click="editVen(venue.venue_id)" class="btn btn-outline-warning">Edit Venue</button>  
                </div>
                </div>
              </div>
              
        </div>
        <div v-else-if="username">
            {{username}}'s Home Page
            <br>
            You are user
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
                      <button class="btn btn-success" @click="rateShow(movie.show_id)">Rate it!!</button>
                    </div>
                  </div>
                </div>
              </div>
             
            </div>
            <router-link to="/allmovies" class="btn btn-primary">View More Movies</router-link>
            <div class="venues-container">
              <div
                v-for="venue in venues"
                :key="venue.venue_id"
                class="venue-item"

              >
                <div class="venue-details">
                  <h2 class="venue-name">{{ venue.venue_name }}</h2>
                  <div>
                    <p class="venue-location">{{ venue.region }}</p>
                    <p class="venue-capacity">Capacity: {{ venue.capacity }}</p>
                  </div>
                  <p class="venue-description">{{ venue.venue_description }}</p>
                 
                
                  
                </div>
              </div>
            </div>
        </div>
        <div v-if="showOverlay" class="overlay">
          <div class="overlay-content">
            <p>Movie added successfully!</p>
           
            <div v-if="showOverlay" class="overlay">
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
          </div>
          <div v-if="deleteVenueOverlay" class="overlay">
            <div class="box">
              <div class="modal-body">
             Are you sure you want to delete this venue? 
             This cannot be changed later.
             </div>
             <div class="modal-footer">
              <button type="button" class="btn btn-danger" @click="deleteVenueApi(currentVenueId)">Delete</button>
              <button type="button" class="btn btn-success" @click="closeDeleteModal">No, I have changed my mind</button>
            </div>
            </div>
          </div> 
          <div v-if="showEditModal" class="overlay">
            <div class="box">
              <h5 class="modal-title">Edit Venue </h5>
              <button type="button" class="close" @click="closeEditModal">
                <span aria-hidden="true">&times;</span>
              </button>
              <div class="modal-body">
                <form>
                  <div class="form-group">
                    <label for="edit-movie-name">Venue Name</label>
                    <input type="text" class="form-control" id="edit-movie-name" v-model="editVenueName">
                  </div>

                  
                
                  <div class="form-group">
                    <label for="edit-movie-description">Description</label>
                    <textarea class="form-control" id="edit-movie-description" v-model="editVenueDescription"></textarea>
                  </div>
                  <div class="form-group">
                    <label for="edit-movie-description">Region</label>
                    <textarea class="form-control" id="edit-movie-description" v-model="editVenueregion"></textarea>
                  </div>
                 
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-success" @click="editVenueApi(currentVenueId)">Save Changes</button>
                <button type="button" class="btn btn-danger" @click="closeEditModal">Cancel</button>
              </div>
            </div>
             
          </div>
          
        
       
        
        <div v-if="error" class="overlay">
          <div class="box">
            <div class="error-message" style="color:red">{{ error }}</div>
            <button class="btn btn-primary" @click="clearMessage">OK</button>
          </div>
        </div>
        <div v-if="successOverlay" class="overlay">
          <div class="box">
            <div class="success-message" style="color:green">{{ message }}</div>
            <button class="btn btn-primary" @click="clearMessage">OK</button>
          </div>
        </div>
        <div v-else>
          Home Page
          
      </div>
    </div>
    
</template>

<script>
  import axios from 'axios';
  axios.defaults.baseURL = 'http://localhost:5000';
export default {
    name : 'Home',
    data(){
        return {
            role : this.$store.state.user.admin,
            username : this.$store.state.user.username,
            movies : [],
            venues: [],
            token :  this.$store.state.user.access_token,
            showOverlay: false,
            error: '',
            ratings : 5,
            showId : '',
            successOverlay : false,
            message : "",
            deleteVenueOverlay : false,
            currentVenueId: '',
            showEditModal : false,
            editVenueDescription : '',
            editVenueName : '',
            editVenueregion : '',
            
        }
    },
    mounted(){
        console.log(this.$store.state.user)
        console.log(this.$store.state.user.admin)
        console.log("Movies", this.movies)
        const token = this.$store.state.user.access_token
        if (!token) {
          this.$router.push('/login')
          return
        }
        this.fetchLatestMovies();
        this.fetchVenues()
        
        
    },
    methods: {
      editVen(venueId){
      this.showEditModal = true
      this.currentVenueId = venueId
    },
    async editVenueApi(venueId){
      const token = this.$store.state.user.access_token
    
     
      const show_attributes = [
        {name :  'venue_name', value : this.editVenueName},
        {name :  'description', value : this.editVenueDescription},
        

      ]
      
      const formData = new FormData();
      show_attributes.forEach(attribute => {
        formData.append(attribute.name, attribute.value);
      });
      console.log(formData)
      
      try{
        const response = await axios.put(`/api/venue/${venueId}`, formData,{
        headers: {
            Authorization: `Bearer ${token}`
        }
        })
        this.message = response.data.message;
        this.successOverlay = true
      }catch(error){
        this.error = error
      }
      
      this.showEditModal = false
      
    },
    deleteVen(venueId){
      this.deleteVenueOverlay = true
      this.currentVenueId = venueId
    },
    async deleteVenueApi(venueId){
      const token = this.$store.state.user.access_token
      const url = "/api/venue/" + venueId
      console.log(url)
      try{
        const response = await axios.delete(url, {
        headers: {
            Authorization: `Bearer ${token}`
        }
        })
        this.message = response.data.message;
        this.deleteOverlay = false
        this.showOverlay = true
      }catch(error){
        this.error = error
      }
    },
    closeEditModal() {
      
      this.showEditModal = false;
      
    },
    closeDeleteModal() {
      
      this.deleteVenueOverlay = false;
      
    },
    fetchLatestMovies() {
      const token = this.$store.state.user.access_token
      // console.log(token)
      //   // Make an HTTP request to fetch the movies created by the admin
      //   if(!token){
      //     this.$router.push('/login')
      //     return
      //   }
      if(token){
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
            this.movies = this.movies.slice(0, 5);
            console.log(this.movies)
          })
          .catch(error => {
            console.error(error);
          });

  }

  },
  rateShow(show_id){
    this.showOverlay = true
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
  async fetchVenues(){
          const token = this.$store.state.user.access_token
          if (!token) {
          this.$router.push('/login')
          return
        }
            
           
            try{
            const response = await axios.get(`/api/venue`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      console.log("Venues : ", response.data)
      this.venues = response.data
      console.log(this.venues)
    }catch(error){
        this.error = error.message;
    }
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
clearMessage() {
        this.showOverlay = false;
        window.location.reload();
      },
}
}

</script>

<style>
.venues-container {
  display: flex;
flex-wrap: wrap;
justify-content: center;
align-items: flex-start;
}

.venue-item {
  width: 30%; /* Adjust as needed */
  margin-bottom: 20px; /* Adjust as needed */
  background-color: #f5f5f5;
border-radius: 8px;
padding: 20px;
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
margin-top: 20px;
margin-left: 20px;
}



.venue-details {
background-color: #f5f5f5;
padding: 10px;
margin-top: 10px;
}

.venue-name {
font-size: 20px;
font-weight: bold;
}

.venue-location {
margin-top: 5px;
}

.venue-capacity,
.venue-available-seats {
margin-top: 5px;
font-size: 14px;
}

.venue-description {
margin-top: 10px;
}
.seats-container {
  margin-top: 10px;
  display: flex;
}

.seat-box {
  --color: black;
  display: inline-block;
  margin: 5px;
  padding: 10px 15px;
  text-decoration: none;
  border-radius: 5px;
  border-color: var(--color);
  color: var(--color);
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
</style>