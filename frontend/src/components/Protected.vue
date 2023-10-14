<template>
  <div>
    <navbar></navbar>
  
    <div>
        <div v-if="error">
            {{ error }}, Something went wrong
        </div>
    <div v-if="username">
        
     
     
      <div class="registration-container">
        <div class="welcome-section">
          <h1>Welcome, {{ username }}!</h1>
      
          <p>{{ message }}
            <p >Your role: {{role}}</p>
          </p>
        </div>
    
        <div class="registration-box">
          <h2>Edit your Profile:</h2>
          <form>
            <div class="form-group">
              <div class="input-icon">
                <img src="https://icons.getbootstrap.com/assets/icons/person-fill.svg" alt="Username" class="input-icon-img">            
                <input type="text" class="form-control" id="username" v-model="username_edited" placeholder="Enter your username">
              </div>
            </div>
            
            <div class="form-group">
              <div class="input-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-flag-fill input-icon-img" viewBox="0 0 16 16">
                  <path d="M1.5 3.5a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0v-8a.5.5 0 0 1 .5-.5zm13-1a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0v-8a.5.5 0 0 1 .5-.5zM2 14h12a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-1 0v-1h-12a.5.5 0 0 1 0-1h12a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-1 0v-1H2z"/>
                  <path d="M1.707 2.793l1.5 1.5-.707.707-1.5-1.5a.5.5 0 0 1 0-.707l1.5-1.5.707.707zM2.5 4.5L4 6l-1.5 1.5-.707-.707L3.586 6l-1.293-1.293.707-.707zm1.5 1.5l1.5 1.5-.707.707-1.5-1.5a.5.5 0 0 1 0-.707l1.5-1.5.707.707zM4.5 6.5L6 8l-1.5 1.5-.707-.707L5.586 8l-1.293-1.293.707-.707zm1.5 1.5l1.5 1.5-.707.707-1.5-1.5a.5.5 0 0 1 0-.707l1.5-1.5.707.707zm1.5 1.5L9 11l-1.5 1.5-.707-.707L8.586 11l-1.293-1.293.707-.707zM7.5 9.5L9 11l-1.5 1.5-.707-.707L8.586 11l-1.293-1.293.707-.707zm1.5 1.5l1.5 1.5-.707.707-1.5-1.5a.5.5 0 0 1 0-.707l1.5-1.5.707.707zm2.5 0l1.5 1.5-.707.707-1.5-1.5a.5.5 0 0 1 0-.707l1.5-1.5.707.707zM12.5 9.5L14 11l-1.5 1.5-.707-.707L13.586 11l-1.293-1.293.707-.707z"/>
                </svg>
                                      
                <input type="text" class="form-control" id="favorite-city" v-model="lang" placeholder="Enter your preffered Language">
              </div>
            </div>
            <div class="form-group">
              <div class="input-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-globe-central-south-asia input-icon-img" viewBox="0 0 16 16">
                  <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0ZM4.882 1.731a.482.482 0 0 0 .14.291.487.487 0 0 1-.126.78l-.291.146a.721.721 0 0 0-.188.135l-.48.48a1 1 0 0 1-1.023.242l-.02-.007a.996.996 0 0 0-.462-.04 7.03 7.03 0 0 1 2.45-2.027Zm-3 9.674.86-.216a1 1 0 0 0 .758-.97v-.184a1 1 0 0 1 .445-.832l.04-.026a1 1 0 0 0 .152-1.54L3.121 6.621a.414.414 0 0 1 .542-.624l1.09.818a.5.5 0 0 0 .523.047.5.5 0 0 1 .724.447v.455a.78.78 0 0 0 .131.433l.795 1.192a1 1 0 0 1 .116.238l.73 2.19a1 1 0 0 0 .949.683h.058a1 1 0 0 0 .949-.684l.73-2.189a1 1 0 0 1 .116-.238l.791-1.187A.454.454 0 0 1 11.743 8c.16 0 .306.084.392.218.557.875 1.63 2.282 2.365 2.282a.61.61 0 0 0 .04-.001 7.003 7.003 0 0 1-12.658.905Z"/>
                </svg>                       
                <input type="text" class="form-control" id="favorite-city" v-model="region" placeholder="Enter your preffered region">
              </div>
            </div>
            <button type="button" class="btn btn-primary" @click="updateUser">Confirm Edit</button>
          </form>
         
        </div>
       
      
      <div>
        <button class="btn btn-danger" @click="openDeleteModal">Delete User</button>
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
           Are you sure you want to delete your account? 
           This cannot be changed later.
           </div>
           <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="deleteUserApi(currentEditId)">Delete</button>
            <button type="button" class="btn btn-success" @click="closeDeleteModal">No, I have changed my mind</button>
          </div>
          </div>
        </div> 

      <p v-if="admin">Only Admin Can view this</p>
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
  import axios from 'axios'
  axios.defaults.baseURL = 'http://localhost:5000';
  export default {
    data() {
      return {
        loading: true,
        message: '',
        username: this.$store.state.user.username,
        error: "",
        role : this.$store.state.user.role,
        profile_pic : this.$store.state.user.profile_pic,
        admin : this.$store.state.user.admin,
        showOverlay: false,
        error: '',
        lang : '',
        region : '',
        token : '',
        message : '',
        username_edited : '',
        deleteOverlay : false,
      }
    },
    
    mounted() {
      this.token = this.$store.state.user.access_token
          if (!this.token) {
          this.$router.push('/login')
          return
        }
    },
    methods : {
      clearMessage() {
        this.showOverlay = false;
        window.location.reload();
      },
      async updateUser(){
        const show_attributes = [
        {name :  'username', value : this.username_edited},
        {name :  'lang', value : this.lang},
        {name :  'region', value : this.region},

      ]
      
      const formData = new FormData();
      show_attributes.forEach(attribute => {
        formData.append(attribute.name, attribute.value);
      });
      console.log(formData)
      try{
        const response = await axios.put(`/api/user`, formData,{
        headers: {
            Authorization: `Bearer ${this.token}`
        }
        })
        const user = {
            username : response.data.username,
            role : response.data.role
          }
          console.log(user)
          this.$store.dispatch('setUser', user);
        this.message = response.data.message;
        this.showOverlay = true
      }catch(error){
        this.error = error
      }
      },
      closeDeleteModal() {
      
      this.deleteOverlay = false;
      
    },
    openDeleteModal(){
      this.deleteOverlay = true;
    },
    async deleteUserApi(){
      const url = "/api/user"
      console.log(url)
      try{
        const response = await axios.delete(url, {
        headers: {
            Authorization: `Bearer ${this.token}`
        }
        })
        this.message = response.data.message;
        this.deleteOverlay = false
        this.showOverlay = true
        this.$router.push("/login")
      }catch(error){
        this.error = error
      }
    }
      
    }

  }
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
  
  .error-message {
    color: red;
  }
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
   
  }
  .registration-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    gap: 10px;
  }
 
  
  
  .registration-box {
    width: 400px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    font-family: 'Roboto', sans-serif;
  }
  
  .registration-box h2 {
    margin-bottom: 20px;
    font-weight: 400;
    font-size: 24px;
    text-align: center;
  }
  
  .registration-box .form-group {
    margin-bottom: 20px;
  }
  
  .registration-box .input-icon {
    display: flex;
    align-items: center;
  }
  
  .registration-box .input-icon-img {
    margin-right: 5px;
  }
  
  .registration-box .form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
  }
  
  .registration-box .btn-primary {
    width: 100%;
  }
  .login-message {
    margin-top: 20px;
    font-size: 14px;
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