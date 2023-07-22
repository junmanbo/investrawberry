<template>
  <div v-if="selectedTicker">
    <h3>{{ selectedTicker.ticker_knm }}</h3>
    <p>현재가: {{ selectedTicker.price }}</p>
    <button class="buy-button" @click="buy">Buy</button>
    <button class="sell-button" @click="sell">Sell</button>
    <div>
      <label for="order-type">주문유형:</label>
      <select id="order-type" v-model="orderType">
        <option value="market">Market</option>
        <option value="limit">Limit</option>
      </select>
    </div>
    <div v-if="orderType === 'market'">
      <label for="quantity">수량:</label>
      <input id="quantity" type="number" v-model.number="quantity" />
      <p>추정 가격: {{ estimatedPrice }}</p>
    </div>
    <div v-else-if="orderType === 'limit'">
      <label for="quantity">수량:</label>
      <input id="quantity" type="number" v-model.number="quantity" />
      <label for="limit-price">지정가격:</label>
      <input id="limit-price" type="number" v-model.number="limitPrice" />
      <p>추정 가격: {{ estimatedPrice }}</p>
    </div>
    <button @click="placeOrder">주문</button>
  </div>
  <!-- Alert component -->
  <div v-if="alertStore.alert" class="container">
    <div class="m-3">
      <div class="alert alert-dismissable" :class="alertStore.alert.type">
        <button @click="alertStore.clear()" class="btn btn-link close">&times;</button>
        {{alertStore.alert.message}}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useTickerStore } from '@/stores/ticker.store';
import { useAlertStore } from '@/stores/alert.store'; // Add this line
import { useOrderStore } from '@/stores/order.store';

const orderStore = useOrderStore();
const tickerStore = useTickerStore();
const selectedTicker = computed(() => tickerStore.selectedTicker);

const alertStore = useAlertStore();

const orderType = ref('market');
const quantity = ref(0);
const limitPrice = ref(0);
const time = ref(0);
const side = ref(null);

const estimatedPrice = computed(() => {
  if (orderType.value === 'market') {
    return quantity.value * selectedTicker.value.price;
  } else if (orderType.value === 'limit') {
    return quantity.value * limitPrice.value;
  }
});

const buy = () => {
  side.value = 'buy';
};

const sell = () => {
  side.value = 'sell';
};

const placeOrder = async () => {
  const orderData = {
    ticker_id: selectedTicker.value.id,
    order_type: orderType.value,
    side: side.value,
    quantity: quantity.value,
    price: limitPrice.value,
  };

  try {
    await orderStore.postOrder(orderData);
    alertStore.success('주문 요청을 보냈습니다.');
  } catch (error) {
    alertStore.error('주문 요청에 실패하였습니다.');
  }
};
</script>

<style scoped>
.buy-button {
  background-color: red;
}

.sell-button {
  background-color: blue;
}
</style>

