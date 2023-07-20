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
        <option value="twap">TWAP</option>
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
    <div v-else-if="orderType === 'twap'">
      <label for="quantity">수량:</label>
      <input id="quantity" type="number" v-model.number="quantity" />
      <label for="time">시간(단위 시):</label>
      <input id="time" type="number" v-model.number="time" />
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
  } else if (orderType.value === 'twap') {
    return quantity.value * selectedTicker.value.price;
  }
});

const buy = () => {
  side.value = 'BUY';
};

const sell = () => {
  side.value = 'SELL';
};

const placeOrder = async () => {
  const orderData = {
    side: side.value,
    orderType: orderType.value,
    quantity: quantity.value,
    limitPrice: limitPrice.value,
    time: time.value * 3600,
  };
  console.log(orderData);

  try {
    // Add your logic for sending the order request here.
    // If the request is successful, then the "success" method of "alertStore" will be called.

    alertStore.success('주문 요청을 보냈습니다.');
  } catch (error) {
    // If an error occurs while sending the request, then the "error" method of "alertStore" will be called.

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

