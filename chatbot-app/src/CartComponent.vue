<template>
  <div v-if="isVisible" class="cart-container">
    <div class="cart-header">
      <h2>Shopping Cart</h2>
      <button class="close-button" @click="$emit('close-cart')">X</button>
    </div>
    <div v-if="cartItems.length > 0">
      <div v-for="item in cartItems" :key="item.product._id" class="cart-item">
        <img :src="item.product.image" alt="Product Image" class="product-image" />
        <div class="product-details">
          <h3>{{ item.product.description }}</h3>
          <p>{{ item.product.price }} L.E</p>
          <p>Quantity: 
            <input type="number" v-model.number="item.quantity" @change="updateQuantity(item.product._id, $event.target.value)" min="1">
          </p>
          <button class="remove-button" @click="removeItem(item.product._id)">Remove Product</button>
        </div>
      </div>
      <p>Total: ${{ calculateTotal }}</p>
      <button class="checkout-button">Checkout</button>
      <button class="clear-button" @click="clearCart">Clear Cart</button>
    </div>
    <p v-else>Your cart is empty. Start Adding Products!</p>
  </div>
</template>

<script>
import cartService from "@/cart-service";

export default {
  props: {
    isVisible: {
      type: Boolean,
      required: true
    },
    cartItems: {
      type: Array,
      default: () => [] // Provide a default value
    }
  },
  methods: {
    updateQuantity(productId, quantity) {
      cartService.updateQuantity(productId, quantity);
      this.$emit('update-cart', cartService.getCartItems());
    },
    removeItem(productId) {
      cartService.removeItem(productId);
      this.$emit('update-cart', cartService.getCartItems());
    },
    clearCart() {
      cartService.clearCart();
      this.$emit('update-cart', cartService.getCartItems());
    }
  },
  computed: {
    calculateTotal() {
      return this.cartItems.reduce((total, item) => total + item.product.price * item.quantity, 0);
    }
  }
};
</script>

<style scoped>
.cart-container {
  position: fixed;
  right: 0;
  top: 0;
  width: 300px;
  height: 100%;
  background-color: white;
  box-shadow: -2px 0 5px rgba(0,0,0,0.1);
  padding: 20px;
  overflow-y: auto;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.cart-item {
  display: flex;
  margin-bottom: 10px;
}

.product-image {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.product-details {
  flex: 1;
}

.checkout-button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  text-align: center;
  border-radius: 15px; /* Make the corners rounded */
}

.checkout-button:hover {
  background-color: #45a049;
}

.clear-button {
  width: 100%;
  padding: 10px;
  background-color: #ff0000;
  color: white;
  border: none;
  cursor: pointer;
  text-align: center;
  border-radius: 15px; /* Make the corners rounded */
}

.clear-button:hover {
  background-color: #c23424;
};

.remove-button{
  background-color: #ff0000;
  color: white;
  padding: 5px;
  cursor: pointer;
  border: 2px solid #ccc; /* Border color */
  border-radius: 50px; /* Make the corners rounded */
}
.remove-button:hover{
  background-color: #c23424;
}
</style>