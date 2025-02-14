<template>
  <div class="product-card">
    <img :src="product.image" alt="Product Image" />
    <h3>{{ product.description }}</h3>
    <p>{{ product.price }} L.E</p>
    <p>Rating: {{ product.rating }}</p>
    <button @click="addToCart(product)">Add to Cart</button>
  </div>
</template>

<script>
import cartService from "@/cart-service"; // Import the cart service
export default {
  props: ["product"],
  methods: {
    addToCart(product) {
      console.log("Product added to cart (Product Card):", product);
      cartService.addItem(this.product);
      this.$emit("added-to-cart", product);
    },
  },
};
</script>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}
img {
  width: 100px;
  height: 100px;
}
button {
  background-color: #28a745;
  color: white;
  padding: 5px;
  cursor: pointer;
  border-radius: 15px; /* Make the corners rounded */
  border: 2px solid #ccc; /* Border color */
}
</style>
