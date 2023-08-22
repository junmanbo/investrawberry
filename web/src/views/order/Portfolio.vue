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
        {{ ticker.ticker_knm }}
      </div>
      <div class="ticker-weight">
        <input v-model="ticker.weight" type="number" class="form-control ticker-weight-input" placeholder="Weight" step="0.01" />
      </div>
      <button @click.stop="removeTicker(index)" class="btn btn-outline-danger btn-sm remove-button">
        <i class="fas fa-trash-alt"></i> <!-- 삭제 아이콘 -->
      </button>
    </div>
    <div class="form-group">
      <label for="investment-amount">투자 금액(단위 원):</label>
      <input v-model="investmentAmount" id="investment-amount" type="number" class="form-control" min="1" step="1" oninput="validity.valid||(value='')" />
    </div>
    <div class="form-group">
      <label for="rebalancing-period">리밸런싱 주기(단위 일):</label>
      <input v-model="rebalancingPeriod" id="rebalancing-period" type="number" class="form-control" min="1" step="1" oninput="validity.valid||(value='')" />
    </div>
    <!-- 메모 추가 -->
    <div class="form-group">
      <label for="memo">메모:</label>
      <textarea v-model="memo" id="memo" class="form-control" rows="3"></textarea>
    </div>
    <div class="form-group">
      <button @click="createAndShowModal" class="btn btn-success mr-2">생성</button>
      <button class="btn btn-success mr-2">수정</button>
      <button class="btn btn-danger mr-3">삭제</button>
      <button class="btn btn-primary">실행</button>
    </div>
    <!-- 생성 결과를 보여주는 모달 -->
    <Modal
      v-if="isModalVisible.value"
      :title="modalTitle.value"
      :body="modalBody.value"
      :modalId="'resultModal'"
      @close-modal="isModalVisible.value = false"
    />
  </div>
</template>

<script setup>
import { OrderMenu } from '@/views/order';
import { SearchModal } from '@/views/order';
import { PortfolioModal } from '@/views/order';
import { ref, reactive } from 'vue';
import { usePortfolioStore } from '@/stores';
import { Modal } from '@/components'

// 선택 메뉴 값 가져오기
const selectedMenu = ref('PORTFOLIO');

// ticker 값 가져오기
const selectedTickers = ref([]);

// portfolio 값 가져오기
const selectedPortfolio = ref(null);

// 선택한 portfolio 와 선택한 ticker 를 누적하여 표시
const portfolioSelected = (portfolio) => {
  const newTickers = portfolio.portfolio_ticker.map(
    (portfolioTicker) => ({
      ...portfolioTicker.ticker,
      weight: 0.0  // 초기 비중값을 0.0으로 설정
    })
  );
  selectedTickers.value.push(...newTickers);
};

const tickerSelected = (ticker) => {
  selectedTickers.value.push({
    ...ticker,
    weight: 0.0  // 초기 비중값을 0.0으로 설정
  });
};

const removeTicker = (index) => {
  selectedTickers.value.splice(index, 1);
};

// portfolio.store.js 함수 사용
const portfolioStore = usePortfolioStore();

const investmentAmount = ref(0);
const rebalancingPeriod = ref(7);
const memo = ref("");

const createPortfolio = async () => {
  const portfolioTicker = selectedTickers.value.map(ticker => ({ ticker_id: ticker.id, weight: ticker.weight }));
  
  const payload = {
    rebal_period: rebalancingPeriod.value,
    amount: investmentAmount.value,
    memo: memo.value,
    portfolio_ticker: portfolioTicker
  };
  
  try {
    const createdPortfolio = await portfolioStore.createPortfolio(payload);
    return createdPortfolio;
  } catch (error) {
    console.error("Error creating portfolio:", error);
    return null;
  }
};

// 모달 표시 여부를 관리하는 상태
const isModalVisible = ref(false);

// 모달에 표시할 내용을 저장하는 상태
const modalTitle = ref('');
const modalBody = ref('');

// 포트폴리오 모달에서 선택된 내용을 저장하는 상태
const selectedPortfolioInfo = ref(null);

// createAndShowModal 함수를 만듦
const createAndShowModal = async () => {
  // createPortfolio 함수를 실행하여 생성 결과를 받아옴
  const createdPortfolio = await createPortfolio();

  // 생성 결과를 모달에 표시하기 위해 정보 저장
  if (createdPortfolio) {
    selectedPortfolioInfo.value = createdPortfolio;
    modalTitle.value = '포트폴리오 생성 결과';
    modalBody.value = JSON.stringify(createdPortfolio, null, 2);
    isModalVisible.value = true;
  }
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
  border-radius: 4px; /* 둥글게 처리 */
  border: 1px solid #ccc;
}

.ticker-info {
  flex: 1;
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  font-size: 16px; /* 폰트 사이즈 추가 */
  border-right: 1px solid #ccc; /* 오른쪽 테두리 추가 */
  padding-right: 10px; /* 오른쪽 여백 추가 */
  margin-right: 10px; /* 오른쪽 마진 추가 */
}


.remove-button {
  margin-left: 10px;
}

.ticker-weight {
  margin-top: 5px;
}

.ticker-weight-input {
  width: 75px;
}
</style>
