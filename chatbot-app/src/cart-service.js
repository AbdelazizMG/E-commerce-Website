// cart-service.js
class CartService {
    constructor() {
      this.cartItems = JSON.parse(localStorage.getItem('cart')) || []; // Load from local storage
    }
  
    getCartItems() {
      return this.cartItems;
    }
  
    addItem(product) {
      const existingProduct = this.cartItems.find(item => item.product._id === product._id);
  
      if (existingProduct) {
        existingProduct.quantity++;
      } else {
        this.cartItems.push({ product, quantity: 1 });
      }
  
      this.saveCart();
    }
  
    removeItem(productId) {
      this.cartItems = this.cartItems.filter(item => item.product._id !== productId);
      this.saveCart();
    }
  
    updateQuantity(productId, quantity) {
      const item = this.cartItems.find(item => item.product._id === productId);
      if (item) {
          item.quantity = quantity;
      }
      this.saveCart();
    }
  
    saveCart() {
      localStorage.setItem('cart', JSON.stringify(this.cartItems));
    }
  
    clearCart() {
      this.cartItems = [];
      localStorage.removeItem('cart');
    }
  }
  
  export default new CartService(); // Export a singleton instance