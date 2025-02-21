<template>
  <div id = "app">
    <Header @products-received="updateProductList"/>
    <AIComponent @products-received="updateProductList"/>
    <ProductList ref="productListComponent" @added-to-cart="addToCart"/>
    <CartComponent :isVisible="isCartVisible" :cartItems="cartItems" @close-cart="hideCart" @update-cart="updateCartItems"/>
    
  </div>
</template>

<script>
import Header from "./HeaderComponent.vue";
import AIComponent from "./AIComponent.vue";
import ProductList from "./ProductList.vue";
import CartComponent from "./CartComponent.vue";
import axios from "axios";
import cartService from "@/cart-service";

export default {
  components: { Header, AIComponent, ProductList, CartComponent },
  data() {
    return { 
      products: [],
      pageName : 'LeftOvers',
      isCartVisible: false, 
      cartItems: [],
    };
  },
  methods: {
    async fetchProducts() {
      console.log("fetchProducts() is being called...");
      try {
        const response = await axios.get(
        //`http://127.0.0.1:8000/api/Homepage/`
        `https://leftovers-deployed-apis-pias8ddje-abdelaziz-mohammads-projects.vercel.app/api/Homepage/`
      );
      console.log("Response from API:", response.data);
      //console.log("Request:", this.query);
      
      // Store search results
      this.results = response.data.results; 
      //this.$emit("products-received", response.data);
      this.updateProductList(response.data)

      } catch (error) {
      console.error("Error:", error);
      this.$emit("products-received", []); // Emit an empty array on error
    }
    },
    updateProductList(products) {
        // Access the ProductList component using a ref
        this.$refs.productListComponent.updateProducts(products);
    }, 
    showCart() {
      console.log("Working"); 
      this.isCartVisible = true;
    },
    hideCart() {
      this.isCartVisible = false;
    },  
    addToCart(product) {
      cartService.addItem(product);
      this.cartItems = cartService.getCartItems();
      this.showCart();
      console.log("Updated cart items:", this.cartItems.length);
      //this.$emit('update-cart', this.cartItems);
      this.updateCartItems(this.cartItems);
    },
    updateCartItems(items) {
      this.cartItems = items;
    },
  },
  mounted() {
    this.fetchProducts();
    document.title = `${this.pageName}`;
  },
  created() {
     //this.fetchProducts();
  },

};
</script>



<style scoped>
header {
  /* Basic header styling */
  background-color: #f0f0f0; /* Example background color */
  padding: 10px;
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
</style>
