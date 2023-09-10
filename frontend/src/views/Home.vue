<template>
    <div v-if="user">
        <div class="jumbotron text-center">
            <h1 class="display-8 fs-4">{{user.user_name}}님, 안녕하세요!</h1>
            <p class="lead fs-6">오늘도 투자 성공하세요 :)</p>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <div class="card text-white bg-info mb-3">
                        <div class="card-header">총자산</div>
                        <div class="card-body">
                            <h5 class="card-title">{{totalBalance}}</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th colspan="4">국내주식 TOP3</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(ticker, index) in domesticStockTopTickers" :key="index">
                    <td>{{ticker.ticker_knm}}<br><small>{{ticker.symbol}}</small></td>
                    <td>{{ticker.marketcap.toLocaleString()}} 억원</td>
                </tr>
            </tbody>
        </table>
        <table class="table">
            <thead>
                <tr>
                    <th colspan="4">코인 TOP3</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(ticker, index) in coinTopTickers" :key="index">
                    <td>{{ticker.ticker_knm}}<br><small>{{ticker.symbol}}</small></td>
                    <td>{{ticker.marketcap.toLocaleString()}} 억원</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useAuthStore, useBalanceStore, useTickerStore } from '@/stores';
import { ref, onMounted, computed } from 'vue';

const authStore = useAuthStore();
const balanceStore = useBalanceStore();
const tickerStore = useTickerStore();
const { user } = storeToRefs(authStore);
const { balances } = storeToRefs(balanceStore);
const { topTickers } = storeToRefs(tickerStore);

onMounted(async () => {
    await balanceStore.getBalances();
    await tickerStore.getTopTickers();
});

const totalBalance = computed(() => {
    let total = 0;
    for (const exchange in balances.value) {
        for (const asset in balances.value[exchange]) {
            total += balances.value[exchange][asset].notional;
        }
    }
    return `₩${Math.floor(total).toLocaleString()}`;
});

const domesticStockTopTickers = computed(() => {
    return topTickers.value.filter(ticker => ticker.asset_type === 'kr_stock');
});

const coinTopTickers = computed(() => {
    return topTickers.value.filter(ticker => ticker.asset_type === 'crypto');
});

const message = ref('');
const showMenu = ref(false);
const showMessage = () => {
    message.value = '알림 메시지입니다!';
    showMenu.value = true;
};
const hideMenu = () => {
    showMenu.value = false;
};
</script>

<style>
@import '@/assets/home.css';
</style> 

