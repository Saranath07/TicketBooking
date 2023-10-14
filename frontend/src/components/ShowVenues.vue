<template>
    <div>
      <navbar></navbar>
  
      <div class="venues-container">
        <div
          v-for="venue in venues"
          :key="venue.id"
          class="venue-item"
        >
          <div class="venue-details">
            <h2 class="venue-name">{{ venue.venue_name }}</h2>
            <div>
              <p class="venue-location">{{ venue.location }}</p>
              <p class="venue-capacity">Capacity: {{ venue.capacity }}</p>
            </div>
            <p class="venue-description">{{ venue.venue_description }}</p>
           
          
            <div class="seats-container" >
                <router-link
                    v-if="venue.timings && venue.timings.length"
                  v-for="timing in venue.timings"
                  :key="timing.timing_id"
                  :to="'/showvenues/' + timing.timing_id + venue.capacity"
                  class="seat-box "
                  :class="['btn', 'btn-outline-' + getSeatColorClass(venue.capacity, timing.available_seats, venue.venue_name), 'btn-sm']"
              
                >
                
                  {{ timing.timing }} 
                  <br>
                  <p class="movie-price">Price: ₹ {{ timing.price }}</p>
                  
                
                </router-link>
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
    adminUsername: '',
      venues: [],
      error : '',
      availableSeatPercentage : 100,
      showOverlay: false,
      error: '',
   
    }
  },
  created() {
      // Get the admin's username from the route params
      this.adminUsername = this.$store.state.user.username;
      // Fetch the movies created by the admin
      this.fetchAdminMovieVenues();

    },
    methods : {
        async fetchAdminMovieVenues(){
          const token = this.$store.state.user.access_token
          if (!token) {
          this.$router.push('/login')
          return
        }
            const showId = this.$route.params.show_id;
    // Use the showId for further processing or API calls
            console.log(showId);
            try{
            const response = await axios.get(`/api/showvenue/${showId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      console.log(response.data)
      this.venues = response.data
    }catch(error){
        this.error = error.message;
    }
        },
       
    getSeatColorClass(capacity, availableSeats, venue_name) {

        const seatBoxElement = this.$refs.seatBoxes;
       
    const percentage = (availableSeats / capacity) * 100;
      console.log(venue_name, percentage)

    if (percentage > 75) {
        
        // const color = 'green'; 
      console.log("green")
        // boxElement.style.setProperty('--color', color);
      return 'success';
    } else if (percentage > 5 && percentage <= 75) {
      console.log("yellow")
      return 'warning';
    } else {
      console.log('red')
  
      return 'danger';
    }
  },
  clearMessage() {
        this.showOverlay = false;
        this.$router.push("/profile")
      }
    }

}
</script>

<style scoped>
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

</style>