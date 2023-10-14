<template>
  <div>
    
  
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <div class="input-icon form-outline mb-4">
            <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/icons/person-circle.svg" alt="Email" class="input-icon-img">
            <input type="text" class="form-control" id="emal" v-model="email" placeholder="Enter your email">
          </div>
        </div>
        <div class="form-group">
          <div class="input-icon form-outline mb-4">
            <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/icons/key.svg" alt="Password" class="input-icon-img">
            <input type="password" id="password" class="form-control" v-model="password" placeholder="Password"/>
            
          </div>
        </div>
        <button type="button" class="btn btn-primary" @click="login" >Login</button>
      </form>
      <p class="register-message">
        Do not have an account? <router-link to="/register">Register</router-link>
      </p>
      
    </div>
    
    <div v-if="error" class="error-overlay">
      <div class="error-box">
        <div class="error-message" style="color:red">{{ error }}</div>
        <button class="btn btn-primary" @click="clearErrorMessage">OK</button>
      </div>
    </div>
    
  </div>
</div>
</template>



<!-- <template>
  <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/icons/person-circle.svg" alt="Username" class="input-icon-img">
<img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/icons/key.svg" alt="Password" class="input-icon-img">
  <div>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <label>
          Username:
          <input type="text" v-model="username">
        </label>
        <label>
          Password:
          <input type="password" v-model="password">
        </label>
        <button type="submit">Login</button>
      </form>
      <p v-if="error">{{ error }}</p>
    </div>
  </template> -->
  
  <script>
  import axios from 'axios';

 
  // Set the base URL for all Axios requests
  axios.defaults.baseURL = 'http://localhost:5000';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
        error: '',
        admin: false,
      }
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('/api/auth', {
            email: this.email,
            password: this.password
          });
          
          // localStorage.setItem('access_token', response.data.access_token);
          if(response.data.role == "admin"){
            this.admin = true
          }
         
          const user = {
            username : response.data.username,
            role : response.data.role,
            admin : this.admin,
            access_token : response.data.access_token
          }
          console.log(user)
          this.$store.dispatch('setUser', user);
          
          this.$router.push('/');
          
         
          // location.reload();
        } catch (error) {
          this.error = error.response.data.error;
        }
        
      },
      clearErrorMessage() {
      this.error = '';
    }
    }
  }
  </script>
  
  <style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');
  
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .login-box {
    width: 300px; /* Adjust the width as desired */
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    font-family: 'Roboto', sans-serif;
    margin-top: 20px; /* Add margin to separate from the navbar */
  }
  
  .login-box h2 {
    margin-bottom: 20px;
    font-weight: 400;
    font-size: 24px;
    text-align: center;
  }
  
  .login-box .form-group {
    position: relative;
    margin-bottom: 25px; /* Added margin for the form-group */
  }
  
  .login-box .input-icon {
    display: flex;
    align-items: center;
  }
  
  .login-box .input-icon-img {
    margin-right: 5px;
  }
  
  .login-box .form-control {
    width: 100%;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #ccc;
    outline: none;
    background-color: transparent;
    transition: all 0.3s;
  }
  
  .login-box .form-control:focus {
    border-bottom-color: #007bff;
  }
  
  .login-box label {
    position: absolute;
    top: 0;
    left: 0;
    font-size: 12px;
    color: #999;
    pointer-events: none;
    transition: all 0.3s;
  }
  
  .login-box .form-control:focus ~ label,
  .login-box .form-control:valid ~ label {
    top: -15px;
    font-size: 10px;
    color: #007bff;
  }
  .error-overlay {
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
  .register-message {
    margin-top: 20px;
    font-size: 14px;
  }
  </style>