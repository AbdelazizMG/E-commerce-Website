<template>
    <header class="AIHeader">
      <h1>AI ChatBot</h1>
      <textarea
      v-model="query"
      placeholder="What do you look for ?..."
    />
    <button @click="searchProducts">Send</button>


    </header>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    data() {
      return { 
        query: "",
        results: [] // Store API response 
      };
    },
    methods: {
      async searchProducts() {
        try {
          const response = await axios.get(
          //`http://127.0.0.1:8000/api/AIsearch/?query=${this.query}`
          `https://leftovers-deployed-apis-ribydk68y-abdelaziz-mohammads-projects.vercel.app//api/AIsearch/?query=${this.query}`
        );
        // console.log("Response from API:", response);
        // console.log("Response Data from API:", response.data);
        // console.log(typeof response.data);
        // console.log("Request:", this.query);

        // Store search results
        this.results = response.data;  

        // Emit the 'products-received' event with the data
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
  .AIHeader {
    background-color: #cbb67b;
    color: white;
    padding: 1rem;
    text-align: center;
  }
  h1{
    align-self: center;
  }
  textarea{
  width: 680px; /* Extend the width of the input */
  height: 100px;
  padding: 7px; /* Add padding for more space inside */
  border-radius: 15px; /* Make the corners rounded */
  border: 2px solid #ccc; /* Border color */
  font-size: 16px; /* Adjust the font size */
  align-self: center;
}
button{
  width: auto;
  height: auto;
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

  </style>
  