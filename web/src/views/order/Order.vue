<template>
  <div>
    <h3>주문</h3>
    <div>
      <input type="text" v-model="search" placeholder="종목 검색..." />
      <ul v-if="searchResult.length > 0">
        <li v-for="ticker in searchResult" :key="ticker.id" @click="selectTicker(ticker)">
          {{ ticker.ticker_knm }} - {{ ticker.symbol }}
        </li>
      </ul>
    </div>
    <div class="stocks">
      <h4>국내주식 top3</h4>
      <StockList :stocks="domesticStocks" />
    </div>
    <div class="stocks">
      <h4>해외주식 top3</h4>
      <StockList :stocks="foreignStocks" />
    </div>
    <div class="stocks">
      <h4>코인 top3</h4>
      <StockList :stocks="coins" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { debounce } from 'lodash';
import { useTickerStore } from '@/stores/ticker.store';
import StockList from '@/views/order/StockList.vue';
import { useRouter } from 'vue-router';

let search = ref('');
let selectedTicker = ref(null);

const tickerStore = useTickerStore();
const searchResult = computed(() => tickerStore.searchResult);
const router = useRouter();

let domesticStocks = ref([
  { name: '삼성전자', price: 70000, rate: '+1.2%' },
  { name: 'lg에너지솔루션', price: 550000, rate: '-2.5%' },
  { name: 'sk하이닉스', price: 113400, rate: '+2.8%' }
]);

let foreignStocks = ref([
  { name: '애플', price: 187.66, rate: '-0.5%' },
  { name: '마이크로소프트', price: 327.64, rate: '-1.26%' },
  { name: '알파벳', price: 116.94, rate: '+0.06%' }
]);

let coins = ref([
  { name: '비트코인', price: 40052000, rate: '0%' },
  { name: '이더리움', price: 2458000, rate: '-0.69%' },
  { name: '리플', price: 623, rate: '-0.8%' }
]);

const searchTicker = debounce(() => {
  tickerStore.searchTicker(search.value);
}, 500);

watch(search, () => {
  searchTicker();
});

const selectTicker = (ticker) => {
  ticker.price = 1000; // 가격 데이터 가져오기 전까지 임의로 설정
  console.log(ticker);
  router.push({ name: 'order-form', params: { ticker_data: ticker } });
};

</script>

<style scoped>
.stocks {
  margin-top: 20px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display:flex;
justify-content:center;
align-items:center;
}

.modal-content {
background-color:white;
padding :20px;
border-radius :10px;
}

ul {
position:absolute;
background-color:white;
width :100%;
border :1px solid #ccc;
border-radius :4px;
padding :0;
margin :0;
box-shadow :0px2px10px rgba(0,0,0,.2);
list-style:none;
z-index :1;
}

li{
padding :10px;
}

li:hover{
background-color:#f0f0f0;
}
</style>


