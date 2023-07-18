<template>
  <div v-if="ticker">
    <h3>{{ ticker.ticker_knm }}</h3>
    <p>현재가: {{ ticker.price }}</p>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
const ticker = route.params.ticker_data;
console.log(ticker);
</script>

