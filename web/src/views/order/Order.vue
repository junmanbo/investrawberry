<template>
  <div>
    <h3>주문</h3>
    <div>
      <input type="text" v-model="search" placeholder="종목 검색..." />
    </div>
    <div class="stocks">
      <h4>국내주식 TOP3</h4>
      <StockList :stocks="domesticStocks" />
    </div>
    <div class="stocks">
      <h4>해외주식 TOP3</h4>
      <StockList :stocks="foreignStocks" />
    </div>
    <div class="stocks">
      <h4>코인 TOP3</h4>
      <StockList :stocks="coins" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import StockList from '@/views/order/StockList.vue';

let search = ref('');

let domesticStocks = ref([
  { name: '삼성전자', price: 70000, rate: '+1.2%' },
  { name: 'LG에너지솔루션', price: 550000, rate: '-2.5%' },
  { name: 'SK하이닉스', price: 113400, rate: '+2.8%' }
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
</script>

<style scoped>
.stocks {
  margin-top: 20px;
}
</style>

