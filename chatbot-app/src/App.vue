<template>
  <div id="app">
    <!-- Chatbot Container -->
    <div class="chatbot-container">
      <!-- Chat Window -->
      <div class="chat-window">
        <div v-for="(message, index) in chatHistory" :key="index" :class="['message', message.sender]">
          {{ message.text }}
        </div>
      </div>

      <!-- Chat Input -->
      <div class="chat-input">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your query..." />
        <button @click="sendMessage">Send</button>
      </div>
    </div>

    <!-- Product Side Panel -->
    <div class="side-panel">
      <h3>Products</h3>
      <div v-if="products && products.length > 0">
        <div v-for="(product, index) in products" :key="index" class="product">
          <img :src="product.image" alt="Product Image" />
          <p>{{ product.name }}</p>
          <p>{{ product.price }}</p>
        </div>
      </div>
      <div v-else>
        <p>No products found. Try searching!</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: "", // User's chat input
      chatHistory: [], // Chat history
      products: [], // List of products fetched from web scraping
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) return;

      // Add user's message to chat history
      this.chatHistory.push({ sender: "user", text: this.userInput });

      // Call your web scraping function here
      const query = this.userInput;
      this.userInput = ""; // Clear input box

      // Simulate a bot response (replace this with your web scraping logic)
      this.chatHistory.push({ sender: "bot", text: `Searching for "${query}"...` });

      // Fetch products (replace this with your web scraping logic)
      const products = await this.fetchProducts(query);
      this.products = products;
    },
    async fetchProducts(query) {
      try {
        const response = await fetch(`http://localhost:5000/search?query=${query}`);
        const products = await response.json();
        return products;
      } catch (error) {
        console.error("Error fetching products:", error);
        return []; // Return an empty array in case of error
      }
    }

  },
};
</script>

<style>
#app {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

.chatbot-container {
  flex: 3;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #ccc;
}

.chat-window {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  border-bottom: 1px solid #ccc;
}

.message {
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  max-width: 70%;
}

.message.user {
  background-color: #e1ffc7;
  align-self: flex-end;
}

.message.bot {
  background-color: #f1f1f1;
  align-self: flex-start;
}

.chat-input {
  display: flex;
  padding: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.chat-input button {
  margin-left: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.side-panel {
  flex: 1;
  padding: 10px;
  background-color: #f9f9f9;
}

.product {
  margin-bottom: 20px;
}

.product img {
  width: 100%;
  height: auto;
  border-radius: 5px;
}

.product p {
  margin: 5px 0;
}
</style>