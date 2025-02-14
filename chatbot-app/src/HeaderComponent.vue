<template>
  <header class="header">
    <div class ="container">
      <header>
      <div class="header-content">  <router-link to="/"> <img src="./assets/logo.png" alt="Your Logo" class="logo"> </router-link> </div>
      </header>      
      <h1>LeftOvers Store</h1>
      <input
      v-model="query"
      @keyup.enter="searchProducts"
      placeholder="Search for products..."
    />
    <button @click="searchProducts">Search</button>
    <h2 class="support">Support? +201158172978</h2>
    </div>
  </header>

</template>

<script>
import axios from "axios";
export default {
  data() {
    return { 
        query: "",
        selectedOption: "",
        results: [] // Store API response 
      };
  },
  methods: {
    async searchProducts() {
      try {
        const response = await axios.get(
        `http://127.0.0.1:8000/api/Normalsearch/?query=${this.query}`
      );
      console.log("Response from API:", response.data);
      console.log("Request:", this.query);
      
      // Store search results
      this.results = response.data.results; 
      this.$emit("products-received", response.data);

  } catch (error) {
    console.error("Error:", error);
    this.$emit("products-received", []); // Emit an empty array on error
  }
},
async searchCategory() {
      if (!this.selectedOption) return;
      try {
        const response = await axios.get(
        `http://127.0.0.1:8000/api/Categorysearch/?query=${this.selectedOption}`
      );
      console.log("Response from API:", response.data);
      console.log("Request:", this.query);
      
      // Store search results
      this.results = response.data.results; 
      this.$emit("products-received", response.data);

  } catch (error) {
    console.error("Error:", error);
    this.$emit("products-received", []); // Emit an empty array on error
  }
},
},
};
</script>

<style scoped>
.header {
  background-color: #333;
  color: white;
  padding: 1rem;
  text-align: left;
}
.container{
  display: flex;
  gap: 20px;
}
h1{
  display: inline;
  margin-right: 250px;
  align-self: center;
}
h2{
  margin-left: 450px;  
  align-self: center;
}
input{
  width: 520px; /* Extend the width of the input */
  height: 30px;
  padding: 7px; /* Add padding for more space inside */
  border-radius: 15px; /* Make the corners rounded */
  border: 2px solid #ccc; /* Border color */
  font-size: 16px; /* Adjust the font size */
  align-self: center;
  margin-left: 250px;
}
button{
  width: auto;
  height: 45px;
  padding: 10px; /* Add padding for more space inside */
  border-radius: 15px; /* Make the corners rounded */
  border: 2px solid #ccc; /* Border color */
  font-size: 16px; /* Adjust the font size */
  align-self: center;
}
button:hover{
  background-color:orange;
}

button:focus{
  background-color:red;
}
.header-content {
    display: flex;
    align-items: center; /* Vertically center the logo and title */
    justify-content: flex-start; /* Align items to the start of the container */
}

.logo {
  max-height: 50px; /* Adjust as needed */
  margin-right: 10px; /* Space between logo and title */
}
h1 {
  /* Basic title styling */
  margin: 0; /* Remove default margins */
}
select {
  width: 200px;
  height: 30px;
  border-radius: 15px; /* Make the corners rounded */
  align-self: center;
  padding: 2px;

}
</style>
