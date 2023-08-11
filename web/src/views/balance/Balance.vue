<template>
  <div class="container">
    <h3 class="text-center my-3">자산 현황</h3>
    <div v-if="Object.keys(balanceStore.balances).length === 0" class="text-center">
      등록된 자산이 없습니다.
    </div>
    <div v-else>
      <div class="row">
        <div class="col-md-6">
          <table>
            <tbody>
              <tr>
                <td><PieChart :data="chartData" :size="150"/></td>
                <td>
                  <div style="height: 100px; overflow-y: auto;">
                    <div v-for="(item, index) in chartData" :key="index" class="d-flex align-items-center mb-2">
                      <span :style="{ backgroundColor: item.color, display: 'inline-block', width: '20px', height: '20px' }"></span>
                      <small><span class="ml-2">{{ item.asset }}</span></small>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="col-md-6">
          <table class="table table-striped table-hover mt-3 d-none d-md-block">
            <thead class="thead-dark">
              <tr>
                <th>자산</th>
                <th>비율(%)</th>
                <th>수량</th>
                <th>평가금액(Won)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in chartData" :key="index">
                <td>{{ item.asset }}<br><small>{{ item.exchange }}</small></td>
                <td>{{ item.value }}%</td>
                <td>{{ item.quantity }}</td>
                <td>{{ Math.floor(item.notional) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="d-md-none">
            <div v-for="(item, index) in chartData" :key="index" class="card mb-3">
              <div class="card-header" :style="{ backgroundColor: item.color }">{{ item.asset }}<br><small>{{ item.exchange }}</small></div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item">비율: {{ item.value }}%</li>
                <li class="list-group-item">수량: {{ item.quantity }}</li>
                <li class="list-group-item">평가금액: {{ Math.floor(item.notional) }} Won</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive } from 'vue';
import { useBalanceStore } from '@/stores';
import PieChart from '@/components/PieChart.vue'; // 원형 그래프 컴포넌트를 임포트합니다.

const balanceStore = useBalanceStore();

let chartData = ref([]);
const colors = reactive({});

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

onMounted(async () => {
    try {
        // Get balances data
        await balanceStore.getBalances();

        calculateChartData();

    } catch (error) {
        console.error(error);
    }
});

function calculateChartData() {
    try {
        let total = 0;
        for (let exchange in balanceStore.balances) {
            for (let asset in balanceStore.balances[exchange]) {
                total += balanceStore.balances[exchange][asset].notional;
            }
        }
        chartData.value = Object.entries(balanceStore.balances).flatMap(([exchange, assets]) =>
            Object.entries(assets)
                .map(([asset, { amount, notional }], index) => {
                    const weight = ((notional / total) * 100).toFixed(2);
                    if (!colors[`${exchange} ${asset}`]) {
                        colors[`${exchange} ${asset}`] = getRandomColor();
                    }
                    return {
                        exchange,
                        asset,
                        value: weight,
                        color: colors[`${exchange} ${asset}`],
                        quantity: amount.toFixed(6),
                        notional,
                    };
                })
                .filter(({ value }) => value > 0)
        );
        chartData.value.sort((a, b) => b.notional - a.notional);
    } catch (error) {
        console.error(error);
    }
}

</script>

<style scoped></style>


