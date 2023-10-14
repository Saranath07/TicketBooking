<template>
  <div id="app">
    
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

.nav-link.router-link-exact-active {
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #42b983;
}
.profile-picture-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #e9ecef;
}
</style>
