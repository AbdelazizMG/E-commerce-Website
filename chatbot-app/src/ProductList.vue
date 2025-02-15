<template>
  <div class="product-list">
    <div class="product-grid">
      <ProductCard
        v-for="product in products"
        :key="product._id"
        :product="product"
        @added-to-cart="handleAddToCart"
      />
    </div>
    <p v-if="!products.length"></p>
  </div>
</template>

<script>
import ProductCard from "./ProductCard.vue";

export default {
  components: { ProductCard },
  data() {
    return {
      products: [],
    };
  },
  methods: {
    handleAddToCart(product) {
      console.log("Product added (Product List):", product);
      this.$emit("added-to-cart", product);
    },
    updateProducts(newProducts) {
      this.products = newProducts;
    },
  },
};
</script>

<style scoped>
.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Adjust minmax as needed */
  gap: 20px; /* Adjust gap as needed */
  padding: 20px; /* Adjust padding as needed */
}

/* Optional: Style the ProductCard to fit nicely in the grid */
.product-card { /* Or whatever your ProductCard class is */
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
  /* Add any other styles to make it look good in the grid */
}

/* Example media query for smaller screens (optional) */
@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* Adjust for smaller screens */
  }
}
</style>
