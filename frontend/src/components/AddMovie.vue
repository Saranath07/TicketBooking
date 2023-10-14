<template>
  <div>
    <navbar></navbar>
  
  <div class="container">
    <div class="box">
      <h2>Add a Movie</h2>
      <form @submit.prevent="addMovie">
        <div class="form-row">
          <div class="form-col">
        <div class="form-group">
          <label for="showName">Show Name</label>
          <input type="text" class="form-control" id="showName" v-model="showName" required>
        </div>
        </div>
        <div class="form-col">
          <div class="form-group">
            <label for="showName">Language</label>
            <input type="text" class="form-control" id="lang" v-model="lang" required>
          </div>
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
        <div class="form-row">
          <div class="form-col">
          <div class="form-group">
            <label for="genre">Genre</label>
            <input type="text" class="form-control" id="genre" v-model="tags" required>
          </div>
          </div>
        <div class="form-col">
        <div class="form-group">
          <label for="venues">Venues</label>
          <select multiple class="form-control" id="venues" v-model="selectedVenues" required>
            <option v-for="venue in venues" :value="venue.id" :key="venue.id">{{ venue.name }}</option>
          </select>
        </div>
        </div>
        <div class="form-col">
        <div class="form-group">
          <label for="price">Price</label>
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text">₹</span>
            </div>
            <input type="number" class="form-control" id="price" v-model="price" step="0.01" required>
          </div>
          </div>
        </div>
        </div>
        <div class="form-group">
          <label for="price">Add an Image</label>
         
          <div>
            <input type="file" @change="handleFileUpload">
           
         
            <img :src="imageUrl" alt="Movie Image" v-if="imageUrl">
          </div>
          </div>
          
        <div class="form-group">
          <div class="description-box">
            <label for="description">Description about the Movie</label>
            <textarea class="form-control" id="description" v-model="description" rows="4" required></textarea>
          </div>
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-primary">Add Movie</button>
        </div>
      </form>

      <!-- Prompt overlay -->
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
      <div v-if="error" class="overlay">
        <div class="box">
          <div class="error-message" style="color:red">{{ error }}</div>
          <button class="btn btn-primary" @click="clearErrorMessage">OK</button>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>





<script>
  import axios from 'axios';
 
  
  // Set the base URL for all Axios requests
  axios.defaults.baseURL = 'http://localhost:5000';
  
  export default {
    name: 'AddMovie',
    data() {
      return {
        showName: '',
        ratings: '0',
        tags : '',
        price : '',
        genre : '',
        description : '',
        selectedVenues: [],
        venues:  [],
        error: '',
        message : '',
        startTime : '',
        endTime : '',
        showOverlay: false,
        error: '',
        moviePicture : null,
        imageUrl : '',
        lang : ''
        
      }
    },
    mounted() {
    // Fetch the venues from the backend API and populate the 'venues' array
    this.fetchVenues();
  },
    methods: {
       async addMovie(){
        const token = this.$store.state.user.access_token
        if (!token) {
        this.$router.push('/login')
        return
      }
      const timings = `${this.startTime} - ${this.endTime}`;
      console.log(this.selectedVenues)
      // return 1;
      const show_attributes = [
        {name :  'show_name', value : this.showName},
        {name :  'ratings', value : this.ratings},
        {name :  'timings', value : timings},
        {name :  'tags', value : this.tags},
        {name :  'price', value : this.price},
        {name :  'venues', value : this.selectedVenues},
        {name :  'description', value : this.description},
        {name : 'lang', value : this.lang}

      ]
      
      const formData = new FormData();
      show_attributes.forEach(attribute => {
        formData.append(attribute.name, attribute.value);
      });
      console.log(formData)
      formData.append('show_pic', this.moviePicture);
      
        try{
            const response = await axios.post('/api/show', formData,{
        headers: {
            Authorization: `Bearer ${token}`
        }
        })
        this.message = response.data.message;
        this.showOverlay = true
        
        
    

        }catch(error){
          console.log(error)
            this.error = error.response.data.message;
        }
       }, 
       clearMessage() {
      this.showOverlay = false;
      this.$router.push("/profile")
    },
    clearErrorMessage() {
      this.error = '';
    },
    async fetchVenues(){
      const token = this.$store.state.user.access_token
        if (!token) {
        this.$router.push('/login')
        return
        }
        const response = await axios.get('/api/venue', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        
      })
      const my_venues = response.data
      
      for(let i = 0; i < my_venues.length; i++ ){
        this.venues.push({
          'id' : my_venues[i].venue_id,
          'name' : my_venues[i].venue_name
        })
      }
      console.log(this.venues)

    },
    handleFileUpload(event) {
      this.moviePicture = event.target.files[0];
      const file = event.target.files[0];
      this.imageUrl = URL.createObjectURL(file);
    
    },


  },
  
  }

  </script>

<style>
.error-box{
    color:red;
}
.description-box {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}

.description-box label {
  display: block;
  font-weight: bold;
}

.description-box textarea {
  width: 100%;
  height: 150px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.container {
  max-width: 600px;
  margin: auto;
  margin-top: 50px;
}

.box {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  height: 150px;
}

textarea {
  resize: horizontal;
}

.time-input-group {
  display: flex;
  align-items: center;
}

.time-input-separator {
  margin: 0 10px;
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
.image-upload {
  display: inline-block;
  position: relative;
}

.upload-label {
  display: block;
  width: 200px; /* Adjust the width as needed */
  height: 200px; /* Adjust the height as needed */
  border: 2px dashed #ccc;
  border-radius: 4px;
  overflow: hidden;
  text-align: center;
  cursor: pointer;
}

.upload-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 48px; /* Adjust the icon size as needed */
  color: #ccc;
  height: 100%;
}
.uploaded-image {
  width: 100%;
  height: auto;
  object-fit: cover;
}
</style>
