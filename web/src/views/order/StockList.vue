<template>
  <table>
    <thead>
      <tr>
        <th>종목</th>
        <th>현재가</th>
        <th>전날 대비 등락</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(stock, index) in stocks" :key="index">
        <td>{{ stock.name }}</td>
        <td>{{ stock.price }}</td>
        <td>{{ stock.rate }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  stocks: Array
});
</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
}
table th,
table td {
  border: 1px solid #ddd;
  padding: 8px;
}
table tr:nth-child(even) {background-color: #f2f2f2;}
table tr:hover {background-color: #ddd;}
table th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}
</style>

