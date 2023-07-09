<template>
  <div>
    <h3>나의 소중한 자산</h3>
    <div v-if="Object.keys(balanceStore.balances).length === 0">
      등록된 자산이 없습니다.
    </div>
    <div v-else>
      <PieChart :data="chartData"/>
      <table class="assets">
        <thead>
          <tr>
            <th>항목</th>
            <th>비율</th>
            <th>수량</th>
            <th>가격</th>
            <th>평가금액</th>
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
            <td>{{ item.price }}</td>
            <td>{{ item.quantity * item.price }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import { ref, onMounted, watch, reactive } from 'vue';
import { useBalanceStore } from '@/stores';
import PieChart from '@/components/PieChart.vue'; // 원형 그래프 컴포넌트를 임포트합니다.

const balanceStore = useBalanceStore();

let chartData = ref([]);
const prices = reactive({});
const colors = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'magenta', 'lime', 'pink', 'teal', 'lavender', 'brown', 'beige', 'maroon', 'mint', 'olive', 'coral', 'navy', 'grey', 'white'];

onMounted(async () => {
    try {
        // Get balances data
        await balanceStore.getBalances();

        // Connect to Upbit websocket API
        const client = new W3CWebSocket('wss://api.upbit.com/websocket/v1');

        // Handle websocket open event
        client.onopen = () => {
            console.log('Websocket opened!')
            // Get asset codes from balances data
            const symbols = Object.values(balanceStore.balances)
                .flatMap((assets) => Object.keys(assets))
                .map((asset) => `KRW-${asset}`);

            // Subscribe to ticker data for specified markets
            client.send(
                JSON.stringify([
                    {
                        ticket: 'test',
                    },
                    {
                        type: 'ticker',
                        codes: symbols,
                    },
                ])
            );
        };

        // Handle websocket message event
        client.onmessage = async (event) => {
            // Convert Blob to ArrayBuffer
            const arrayBuffer = await event.data.arrayBuffer();
            // Convert ArrayBuffer to string
            const dataString = new TextDecoder().decode(arrayBuffer);
            // Parse JSON string
            const data = JSON.parse(dataString);
            if (data.type === 'ticker') {
                prices[data.code] = data.trade_price;
            }
        };

        // Handle websocket close event
        client.onclose = () => {
            console.log('Upbit websocket connection closed');
        };
    } catch (error) {
        console.error(error);
    }
});


watch(prices, () => {
    try {
        let total = 0;
        for (let exchange in balanceStore.balances) {
            for (let asset in balanceStore.balances[exchange]) {
                const quantity = balanceStore.balances[exchange][asset];
                const price = asset === 'KRW' ? 1 : prices[`KRW-${asset}`] || 0;
                total += quantity * price;
            }
        }
        chartData.value = Object.entries(balanceStore.balances).flatMap(([exchange, assets]) =>
            Object.entries(assets)
                .map(([asset, quantity], index) => {
                    const price = asset === 'KRW' ? 1 : prices[`KRW-${asset}`] || 0;
                    const weight = ((quantity * price / total) * 100).toFixed(2);
                    const item = {
                        label: `${exchange} ${asset}`,
                        value: weight,
                        quantity,
                        price,
                        color: colors[index % colors.length],
                    };
                    return item;
                })
                .filter(({ value }) => value > 0)
        );
    } catch (error) {
        console.error(error);
    }
});

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

