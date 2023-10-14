<template>
    <div>
        <navbar></navbar>
        <h1>Your Bookings</h1>
    <div class="booking-details">
      <div v-if="bookings.length">
      
      <div v-for="booking in bookings" :key="booking.booking_id" class="booking-item card">
        <div class="row no-gutters">
          <div class="col-md-4">
            <img :src="booking.show_pic" alt="Show Image" class="card-img" />
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <h3 class="card-title">{{ booking.show_name }}</h3>
              <p class="card-text"><strong>Booking id :</strong> {{ booking.booking_id }}</p>
              <p class="card-text"><strong>Theatre name : </strong>{{ booking.venue_name }}</p>
              <div><strong>List of Seats:</strong> {{ booking.list_of_seats.join(', ') }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
     <h3>You have no Bookings done yet</h3> 
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
export default{
    data(){
        return{
            username : "",
            bookings : [],
            error : ''

        }
    },
    methods : {
        async fetchBookingDetails(){
          console.log("hello")
            const token = this.$store.state.user.access_token
        if(!token){
          this.$router.push('/login')
          return
        }
        try{
            const response = await axios.get(
                "/api/bookingDetails", {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
            )
            this.bookings = response.data
            const baseUrl = 'http://localhost:5000';
          const modifiedMovies = response.data.map((movie) => {
          return {
          ...movie,
          show_pic: baseUrl + "/static/shows" + movie.show_pic,
        };
      
        
});
        this.bookings = modifiedMovies;
        }catch(error){
            this.error = error
        }  
        },
        clearMessage() {
        this.showOverlay = false;
        this.error = ''
        window.location.reload();
      }
    },
    mounted(){
        this.fetchBookingDetails();
    },
    

}
</script>

<style>
.booking-details {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.booking-item {
  display: flex;
  align-items: center;
  background-color: #f1f1f1;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.booking-image {
    width: 200px;
    height: 300px;
  overflow: hidden;
  border-radius: 4px;
}

.booking-image img {
    width: 200px;
    height: 300px;
  object-fit: cover;
}

.booking-info {
  margin-left: 20px;
}

.booking-title {
  font-size: 20px;
  margin-bottom: 10px;
}

.booking-venue {
  font-size: 16px;
  margin-bottom: 10px;
}

.booking-seats {
  list-style: none;
  padding: 0;
  margin: 0;
}

.booking-seats li {
  font-size: 14px;
  margin-bottom: 5px;
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