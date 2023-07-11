<template>
  <div>
    <h3>자산 현황</h3>
    <div v-if="Object.keys(balanceStore.balances).length === 0">
      등록된 자산이 없습니다.
    </div>
    <div v-else>
      <PieChart :data="chartData"/>
      <table class="assets">
        <thead>
          <tr>
            <th>자산</th>
            <th>비율(%)</th>
            <th>수량</th>
            <th>평가금액(Won)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in chartData" :key="index">
            <td>
              <span :style="{ backgroundColor: item.color, display: 'inline-block', width: '10px', height: '10px' }"></span>
              {{ item.label }}
            </td>
            <td>{{ item.value }}%</td>
            <td>{{ item.quantity }}</td>
            <td>{{ Math.floor(item.notional) }}</td>
          </tr>
        </tbody>
      </table>
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
                        label: `${exchange} ${asset}`,
                        value: weight,
                        color: colors[`${exchange} ${asset}`],
                        quantity: amount.toFixed(6),
                        notional,
                    };
                })
                .filter(({ value }) => value > 0)
        );
    } catch (error) {
        console.error(error);
    }
}

</script>

<style scoped>
.assets {
    margin-top: 20px;
    border-collapse: collapse;
}
.assets th,
.assets td {
    border: 1px solid #ddd;
    padding: 8px;
}
.assets tr:nth-child(even) {background-color: #f2f2f2;}
.assets tr:hover {background-color: #ddd;}
.assets th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}
</style>

