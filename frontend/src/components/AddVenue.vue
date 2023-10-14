<template>
    <div>
      <navbar></navbar>
    
    <div class="container">
      <div class="box">
      <h2>Add a Theatre</h2>
      <form @submit.prevent="addVenue">
        <div class="form-row">
          <div class="form-col">
        <div class="form-group">
          <label for="movieName">Venue Name</label>
          <input type="text" class="form-control" id="movieName" v-model="venueName" required>
        </div>
      </div>
      <div class="form-col">
        <div class="form-group">
            <label for="movieName">Venue Location</label>
            <input type="text" class="form-control" id="movieName" v-model="location" required>
          </div>
      </div>
        </div>
        
        
          <div class="form-row">
            
      <div class="form-col">
        <div class="form-group">
          <label for="price">Capacity</label>
          <div class="input-group">
            <div class="input-group-prepend">
             
            </div>
            <input type="number" class="form-control" id="price" v-model="capacity" step="0.01" required>
          </div>
        </div>
        </div>
        </div>
        <div class="form-group">
            <div class="description-box">
              <label for="description">Description about the Venue</label>
              <textarea class="form-control" id="description" v-model="description" rows="4" required></textarea>
            </div>
          </div>
        <div class="form-group">
        <button type="submit" class="btn btn-primary">Add Venue</button>
        </div>
      </form>
      <div v-if="showOverlay" class="overlay">
        <div class="box">
          <div class="success-message">{{ message }}</div>
          <button class="btn btn-primary" @click="clearMessage">OK</button>
        </div>
      </div>
      <div v-if="error" class="overlay">
        <div class="box">
          <div class="error-message">{{ error }}</div>
          <button class="btn btn-primary" @click="clearMessage">OK</button>
        </div>
      </div>
    </div>
    </div>
  </div>
  </template>
  
  <!-- <template>
      <div>
          <navbar></navbar>
          <h1>Add a Movie</h1>
          <form @submit.prevent="addMovie">
            <label>
              Show Name:
              <input type="text" v-model="showName">
            </label>
            <label>
              Ratings:
              <input type="text" v-model="ratings">
            </label>
            <label>
              Timings:
              <input type="text" v-model="timings">
            </label>
            <label>
              Genre:
              <input type="text" v-model="tags">
            </label>
            <label>
              Price:
              <input type="text" v-model="price">
            </label>
            <button type="submit">Add Movie</button>
          </form>
          <p class="error-box" v-if="error">{{ error }}</p>
        </div>
  </template> -->
  
  <script>
    import axios from 'axios';
    axios.defaults.baseURL = 'http://localhost:5000';
    
    export default {
      name: 'AddVenue',
      data() {
        return {
          venueName: '',
          location : '',
          capacity : '',          
          error: '',
          message : '',
          description : '',
          
          showOverlay: false
          
        }
      },
      methods: {
         async addVenue(){
          const token = this.$store.state.user.access_token
          if (!token) {
          this.$router.push('/login')
          return
        }
        const venueData = {
                  venue_name : this.venueName,
                  location : this.location,
                  capacity : this.capacity,
                  description : this.description
              }
          try{
              const response = await axios.post('/api/venue', venueData,{
          headers: {
              Authorization: `Bearer ${token}`
          }
          })
          this.message = response.data.message;
          this.showOverlay = true
          
          
      
  
          }catch(error){
              this.error = "Something went wrong";
          }
         }, 
         clearMessage() {
        this.showOverlay = false;
        this.$router.push("/profile")
      }
  
    },
    
    }
  
    </script>
  
  <style>
  .error-box{
      color:red;
  }
  .box {
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 10px;
  }
  
  .container {
    max-width: 400px;
    margin: auto;
    margin-top: 50px;
  }
  .form-row {
    display: flex;
    justify-content: space-between;
  }
  
  .form-col {
    flex: 1;
    margin-right: 10px;
  }
  
  .form-col:last-child {
    margin-right: 0;
  }
  input[type="range"] {
    width: 100%;
  }
  
  input[type="number"] {
    padding-left: 10px;
  }
  
  .input-group-text {
    background-color: #fff;
  }
  .time-input-group {
    display: flex;
    align-items: center;
  }
  
  .time-input-separator {
    margin: 0 10px;
  }
  .form-group button {
    margin-top: 10px;
  }
  .overlay {
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
  
  .box {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
  }
  
  .error-message {
    color: red;
    margin-bottom: 10px;
  }
  .success-message{
    color: green;
    margin-bottom: 10px;
  }
  </style>