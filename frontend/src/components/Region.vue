<template>
    <div>
        <navbar></navbar>
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
</template>

<script>
 import axios from 'axios';


axios.defaults.baseURL = 'http://localhost:5000';
export default{
    data(){
        return {
            region : this.$route.params.name,
            venues: [],
        }
    },
    mounted(){
        this.fetchVenuesRegion()
    },
    methods : {
       async fetchVenuesRegion(){
        try{
            const res = await axios.get(`/api/search_region/${this.region}`)
            this.venues = res.data
            console.log(res.data)

        }catch(e){
            this.error = e
        }
       }
    }
}
</script>