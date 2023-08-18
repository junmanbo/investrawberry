<template>
  <div>
    <h3>포트폴리오 주문</h3>
    <OrderMenu :selected-menu="selectedMenu" @update:selected-menu="selectedMenu = $event" />
    <div class="form-group">
      <PortfolioModal @portfolio-selected="portfolioSelected" /><br />
      <SearchModal @ticker-selected="tickerSelected"/>
    </div>
    <!-- 종목 정보 표시 -->
    <div class="ticker-row" v-for="(ticker, index) in selectedTickers" :key="ticker.id">
      <div class="ticker-info">
        {{ ticker.ticker_knm }} - {{ ticker.symbol }}
      </div>
      <button @click.stop="removeTicker(index)" class="btn btn-outline-danger btn-sm remove-button">
        <i class="fas fa-trash-alt"></i> <!-- 삭제 아이콘 -->
      </button>
    </div>
    <div class="form-group">
      <label for="investment-amount">투자 금액(단위 원):</label>
      <input id="investment-amount" type="number" class="form-control" min="1" step="1" oninput="validity.valid||(value='')" />
    </div>
    <div class="form-group">
      <label for="rebalancing-period">리밸런싱 주기(단위 일):</label>
      <input id="rebalancing-period" type="number" class="form-control" min="1" step="1" oninput="validity.valid||(value='')" />
    </div>
    <!-- 메모 추가 -->
    <div class="form-group">
      <label for="memo">메모:</label>
      <textarea id="memo" class="form-control" rows="3"></textarea>
    </div>
    <div class="form-group">
      <button class="btn btn-success mr-2">생성</button>
      <button class="btn btn-success mr-2">수정</button>
      <button class="btn btn-danger mr-3">삭제</button>
      <button class="btn btn-primary">실행</button>
    </div>
  </div>
</template>

<script setup>
import { OrderMenu } from '@/views/order';
import { SearchModal } from '@/views/order';
import { PortfolioModal } from '@/views/order';
import { ref, reactive } from 'vue';

// 선택 메뉴 값 가져오기
const selectedMenu = ref('PORTFOLIO');

// ticker 값 가져오기
//const selectedTickers = reactive([]);
const selectedTickers = ref([]);
// portfolio 값 가져오기
const selectedPortfolio = ref(null);

// 선택한 portfolio 와 선택한 ticker 를 누적하여 표시
const portfolioSelected = (portfolio) => {
  const newTickers = portfolio.portfolio_ticker.map(
    (portfolioTicker) => portfolioTicker.ticker
  );
  selectedTickers.value.push(...newTickers);
};

const tickerSelected = (ticker) => {
  selectedTickers.value.push(ticker);
};
const removeTicker = (index) => {
  selectedTickers.value.splice(index, 1);
};


</script>

<style scoped>
.ticker-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  background-color: #f0f0f0; /* 배경색 추가 */
  padding: 10px; /* 패딩 추가 */
  border-radius: 5px; /* 둥글게 처리 */
}

.ticker-info {
  flex: 1;
  font-family: 'Noto Sans KR', sans-serif; /* 폰트 변경 */
  font-weight: 700; /* 볼드체 설정 */
}

.remove-button {
  margin-left: 10px;
}
</style>
