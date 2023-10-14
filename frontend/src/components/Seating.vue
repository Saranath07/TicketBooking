<template>
    <div>
        <navbar></navbar>
        <div class="statistics" v-if="admin">

            <p>Booked Seats: {{ bookedSeats.length }}</p>
            <p>Available Seats: {{totalSeats -  bookedSeats.length }}</p>
          
          </div>
      <div class="seating-plan">
      <div style="color:blue">Screen</div>
        <p></p>
       
          <div v-for="row in rows" :key="row" class="seating-row">
            <div v-for="seat in seatsPerRow" :key="seat" class="seat">
              <div
              :class="['seat-status', { 'available': isSeatAvailable(row, seat), 'booked': isSeatBooked(row, seat), 'selected' : isSeatSelected(row, seat) }]"
              @click="toggleSeatSelection(row, seat)"
              :disabled="isSeatBooked(row, seat)"
                
              >
              <svg class="seat-svg">
                 
                <circle :class="['seat-circle', { 'selected': isSeatSelected(row, seat) }]" cx="20" cy="20" r="15" />
                </svg>
                <div class="seat-label">{{ row }}{{ seat }}</div>
                <!-- {{ isSeatBooked(row, seat) }} -->
              </div>
            </div>
          </div>
        
        
      
      </div>
      <div v-if="!admin">
        <button type="button" class="btn btn-primary" @click="book">Book Now</button>
      </div>
      <div v-if="showOverlay" class="overlay">
        <div class="overlay-content">
          <p class="success-message">Booking Confirmed!</p>
         
          <div v-if="showOverlay" class="error-overlay">
            <div class="error-box">
              <div class="success-message">{{ message }}</div>
              <button class="btn btn-primary" @click="clearMessage">OK</button>
            </div>
          </div>
          
        </div>
      </div>
      <div v-if="error" class="error-overlay">
        <div class="error-box">
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
        rows: [], 
        seatsPerRow: 10, 
        bookedSeats: [], 
        adminUsername : '' ,
        error : ''  ,
        showvenueId : '',
        totalSeats : 0,
        admin : this.$store.state.user.admin,
        selectedSeats : [],
        showOverlay : false,
        error : false
    };
    },
    created() {
      this.adminUsername = this.$store.state.user.username;
      
    },
    mounted(){
        
        this.getBookingDetails();
        
        
    },

    methods: {

    async getBookingDetails(){
        const token = this.$store.state.user.access_token
          if (!token) {
          this.$router.push('/login')
          return
        }
        this.totalSeats = this.$route.params.showvenue_id.slice(-2)
        const n = Math.floor(this.totalSeats / this.seatsPerRow)
        this.rows = this.generateAlphabetList(n)
        
        
        this.showvenueId = this.$route.params.showvenue_id.slice(0, -2);
        this.totalSeats = this.$route.params.showvenue_id.slice(-2)
        // console.log(this.showvenueId);
        
        try{
            const response = await axios.get(`/api/booking/${this.showvenueId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      this.bookedSeats = response.data
      console.log(this.bookedSeats)
    }catch(error){
        this.error = error.message;
        console.log(error)
    }

    },
     generateAlphabetList(n) {
  let alphabetList = [];

  
  let asciiCodeA = 65;

  for (let i = 0; i < n; i++) {
    let alphabet = String.fromCharCode(asciiCodeA + i);
    alphabetList.push(alphabet);
  }

  return alphabetList;
},
      isSeatAvailable(row, seat) {
        // Check if seat is available (modify with your own logic)
        
        for (let i = 0; i < this.bookedSeats.length; i++) {
            const item = this.bookedSeats[i];
            // Access the properties of each item
            const seatNumber = item.seat_number.trim()
            const row1 = seatNumber[0];
            const col1 = seatNumber.slice(1);
            if((row1 == row) && (col1 == seat)){
                return false
            }
        }     
        return true
      },
      isSeatBooked(row, seat) {
        for (let i = 0; i < this.bookedSeats.length; i++) {
            const item = this.bookedSeats[i];
            // Access the properties of each item
            const seatNumber = item.seat_number.trim()
            const row1 = seatNumber[0];
            const col1 = seatNumber.slice(1);
            // console.log(item)
            // console.log(row, seat)
            if((row1 == row) && (col1 == seat)){
                return true
            }
        }     
        return false
      },
      isSeatSelected(row, seat) {
      // Check if seat is selected
      return this.selectedSeats.some((selectedSeat) => {
        return selectedSeat.row === row && selectedSeat.seat === seat;
      });
    },
    toggleSeatSelection(row, seat) {
      // Toggle seat selection
      if(!(this.isSeatBooked(row, seat))){
      const seatIndex = this.selectedSeats.findIndex(
        (selectedSeat) => selectedSeat.row === row && selectedSeat.seat === seat
      );
      console.log(seatIndex)
      if ((seatIndex > -1)) {
        this.selectedSeats.splice(seatIndex, 1); // Deselect the seat
      } else {
        this.selectedSeats.push({ row, seat }); // Select the seat
      }
    }
    },
     
      async book(){
        console.log("Working")
        console.log(this.selectedSeats)
        const seats_booked = []
        for(let i = 0; i < this.selectedSeats.length; i++){
          const seat = `${this.selectedSeats[i]['row']}${this.selectedSeats[i]['seat']}`
          seats_booked.push(seat)
        }
        
        console.log(seats_booked)
        const data = {
          "showvenue_id" : this.showvenueId,
          "seat_numbers" : seats_booked
        }
        const token = this.$store.state.user.access_token
        try{
          const response = await axios.post("/api/booking", data,{
        headers: {
            Authorization: `Bearer ${token}`
        }
        })
        this.message = response.data.message;
        this.showOverlay = true
        }catch(error){
          console.log(error)
        }
        
        return 1
      },
      clearMessage() {
      this.showOverlay = false;
      location.reload();
    },
    clearErrorMessage() {
      this.error = '';
    },
      handleSeatClick(row, seat) {
        
      const isSelected = this.selectedSeats.some(selectedSeat => selectedSeat.row === row && selectedSeat.seat === seat);
      if (isSelected) {
        this.selectedSeats = this.selectedSeats.filter(selectedSeat => !(selectedSeat.row === row && selectedSeat.seat === seat));
      } else {
        this.selectedSeats.push({ row, seat });
        console.log(this.selectedSeats)
      }
},
      
    },
  };
  </script>

<style>
.seating-plan {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.seating-row {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.seat {
  margin: 5px;
  color: red;
}

.seat-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 60px;
  height: 60px;
  cursor: pointer;
}

.seat-svg {
    width: 40px;
    height: 40px;
  }
  
  .seat-circle {
    fill: currentColor;
  }
  
  .seat-label {
    margin-top: 5px;
  }
  
  .available {
    color: grey;
  }
  
  .booked {
    color: red;
  }
  .selected{
    color : green
  }
  .seat-status[disabled] {
    cursor: not-allowed;
  }
  .success-message{
    color: green;
    margin-bottom: 10px;
  }
  .error-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Adjust the background color and opacity as needed */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999; /* Ensure the overlay is displayed above other elements */
  }
  
  .error-box {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
  }
  
  .error-message {
    color: red;
    margin-bottom: 10px;
  }
</style>