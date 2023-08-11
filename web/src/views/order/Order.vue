<template>
  <div>
    <h5>단순 주문</h5>
    <OrderMenu :selected-menu="selectedMenu" @update:selected-menu="selectedMenu = $event" />
      <div v-if="selectedMenu === 'SIMPLE'">
        <div class="form-group">
          <div class="input-group">
            <input type="text" class="form-control" v-model="search" placeholder="종목 검색..." />
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" @click="search = ''">x</button>
            </div>
          </div>
          <ul class="list-group" v-if="searchResult.length > 0 && search.length > 0">
            <li class="list-group-item" v-for="ticker in searchResult" :key="ticker.id" @click="selectTicker(ticker)">
              {{ ticker.ticker_knm }} - {{ ticker.symbol }}
            </li>
          </ul>
        </div>

        <!-- 주문 폼 -->
        <div v-if="selectedTicker">
          <h3>{{ selectedTicker.ticker_knm }}</h3>
          <p>현재가: {{ selectedTicker.current_price }} 원</p>
          <div class="btn-group" role="group">
            <button type="button" class="btn btn-primary" @click="buy">Buy</button>
            <button type="button" class="btn btn-danger" @click="sell">Sell</button>
          </div>
          <div class="form-group">
            <label for="order-type">주문유형:</label>
            <select id="order-type" v-model="orderType" class="form-control">
              <option value="market">Market</option>
              <option value="limit">Limit</option>
            </select>
          </div>
          <div v-if="orderType === 'market' || orderType === 'limit'">
            <div class="form-group">
              <label for="quantity">수량:</label>
              <input id="quantity" type="number" v-model.number="quantity" class="form-control" />
            </div>
            <div v-if="orderType === 'limit'">
              <div class="form-group">
                <label for="limit-price">지정가격:</label>
                <input id="limit-price" type="number" v-model.number="limitPrice" class="form-control" />
              </div>
            </div>
            <p>추정 가격: {{ estimatedPrice }}</p>
            <button @click="placeOrder" class="btn btn-success">주문</button>
          </div>
        </div>

        <!-- Alert component -->
        <div v-if="alertStore.alert" class="container">
          <div class="m-3">
            <div class="alert alert-dismissable fade show" :class="[alertStore.alert.type, 'alert-dismissible']">
              <button @click="alertStore.clear()" type="button" class="close">×</button>
              {{alertStore.alert.message}}
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { debounce } from 'lodash';
import { useTickerStore } from '@/stores/ticker.store';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/stores/order.store';
import { useAlertStore } from '@/stores/alert.store'; // Add this line
import { OrderMenu } from '@/views/order';

const tickerStore = useTickerStore();
const searchResult = computed(() => tickerStore.searchResult);
const orderStore = useOrderStore();
const alertStore = useAlertStore();

let search = ref('');
const router = useRouter();
const selectedTicker = ref(null);
const orderType = ref('market');
const quantity = ref(0);
const limitPrice = ref(0);
const side = ref(null);

const selectedMenu = ref('SIMPLE');

const searchTicker = debounce(() => {
  tickerStore.searchTicker(search.value);
}, 500);

watch(search, () => {
  if (!search) {
    // 검색 키워드가 비어 있으면 선택된 종목과 검색 결과를 초기화합니다.
    selectedTicker.value = null;
    tickerStore.clearSearchResult();
  } else {
    searchTicker();
  }
});

const selectTicker = (ticker) => {
  selectedTicker.value = ticker;
};

const estimatedPrice = computed(() => {
  if (!selectedTicker.value) return 0;
  if (orderType.value === 'market') {
    return quantity.value * selectedTicker.value.current_price;
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
  if (!selectedTicker.value) return;

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
@media (max-width: 576px) {
  .form-group {
    margin-bottom: 1rem;
  }
}
</style>

