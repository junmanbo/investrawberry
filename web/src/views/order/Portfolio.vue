<template>
  <div>
    <h3>포트폴리오 주문</h3>
    <OrderMenu :selected-menu="selectedMenu" @update:selected-menu="selectedMenu = $event" />
    <div class="form-group">
      <button class="btn btn-primary mb-2">포트폴리오 가져오기</button>
      <br>
      <button class="btn btn-primary">+ 종목추가</button>
    </div>
    <div class="form-group">
      <label for="investment-amount">투자 금액:</label>
      <input id="investment-amount" type="number" class="form-control" />
    </div>
    <div class="form-group">
      <label for="rebalancing-period">리밸런싱 주기:</label>
      <input id="rebalancing-period" type="number" class="form-control" />
    </div>
    <div class="form-group">
      <button class="btn btn-success mr-2">생성</button>
      <button class="btn btn-success">실행</button>
    </div>
  </div>
</template>

<script setup>
import { OrderMenu } from '@/views/order';
import { ref } from 'vue';

const selectedMenu = ref('PORTFOLIO');
</script>

<style scoped></style>
