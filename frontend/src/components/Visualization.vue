<template>
    <div>
      <navbar></navbar>
      
        
     
      
      
      
        
      <div  class="chart-container">
        <div class="chart-wrapper">
            <div class="chart-title"><h3> Movie Analysis Chart</h3></div>
          <canvas id="myMovieChart" class="chart"></canvas>
         
        </div>
     

      </div>
      <br>
      <br>
      <div  class="chart-container">
        <div class="chart-wrapper">
            <div class="chart-title"><h3> Venue Analysis Chart</h3></div>
          <canvas id="myVenueChart" class="chart"></canvas>
          
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
    import { Chart, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js';

    Chart.register(BarController, BarElement, CategoryScale, LinearScale);
  
  export default {
    data(){
        return {
            chartMovieData: {
                labels: [], // movies
                datasets: [{
                label: 'My Dataset',
                data: [], // no of people
                backgroundColor: [],
                
        }]
        },
        chartVenueData: {
                labels: [], // venues
                datasets: [{
                label: 'My Dataset',
                data: [], // no of people
                backgroundColor: [],
                
        }]
        },
      
        
        error : null
    }
    },
    mounted() {
        this.fetchMovieDetails()
      this.fetchVenueDetails()
      
     },
     methods : {
        createMovieChart(){
            const ctx = document.getElementById('myMovieChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: this.chartMovieData,
        options: {
            responsive: false,
            scales: {
                y: {
                ticks: {
                    beginAtZero: true
                }
                }
            }
            }
      });
        },
        createVenueChart(){
            const ctx = document.getElementById('myVenueChart').getContext('2d');
            new Chart(ctx, {
        type: 'bar',
        data: this.chartVenueData,
        options: {
            responsive: false,
            scales: {
                y: {
                ticks: {
                    beginAtZero: true
                }
                }
            }
            }
      });
        },
       
       async fetchMovieDetails(){
        console.log("Hello")
        const token = this.$store.state.user.access_token
        try{
            const res = await axios.get("/api/showanalytics", {headers : {
          'Authorization': `Bearer ${token}`
        }})
        console.log(res.data)
        this.chartMovieData.labels = res.data.movies;
        this.chartMovieData.datasets[0].data = res.data.viewers;
        
        const colors = this.chartMovieData.datasets[0].data.map((_, i) => {
      return `hsl(${i / this.chartMovieData.datasets[0].data.length * 360}, 100%, 50%)`;
    });
    this.chartMovieData.datasets[0].backgroundColor = colors;
        
        this.createMovieChart()
        }catch(e){
            this.error = e
        }
        
        



       } ,
       async fetchVenueDetails(){
        const token = this.$store.state.user.access_token
        try{
            const res = await axios.get("/api/venueanalytics", {headers : {
          'Authorization': `Bearer ${token}`
        }})
        console.log(res.data)
        this.chartVenueData.labels = res.data.venues;
        this.chartVenueData.datasets[0].data = res.data.viewers;
        
        const colors = this.chartVenueData.datasets[0].data.map((_, i) => {
      return `hsl(${i / this.chartVenueData.datasets[0].data.length * 360}, 100%, 50%)`;
    });
    this.chartVenueData.datasets[0].backgroundColor = colors;
        
        this.createVenueChart()
        }catch(e){
            this.error = e
        }
        
        

},
    clearMessage() {
        this.error= null;
       
      },
     }
  }
  </script>
  
  <style>
  .chart-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }
  
  
  .chart-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .chart {
    width: 400px;
    height: 400px;
  }
  
  .chart-title {
    margin-top: 10px;
  }
  
  </style>