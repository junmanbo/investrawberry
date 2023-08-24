<template>
  <div>
    <button @click="showModal = true" class="btn btn-primary">
      포트폴리오 가져오기
    </button>
    <div class="modal" tabindex="-1" role="dialog" :class="{ 'd-block': showModal, 'd-none': !showModal }">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">포트폴리오 전체보기</h5>
            <button type="button" class="close" @click.stop="showModal = false">
              <span>&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <ul class="list-group list-group-flush">
              <li
                class="list-group-item"
                v-for="(portfolio, index) in portfolios"
                :key="index"
                @click="selectPortfolio(portfolio)"
              >
              <div>
                <input
                  type="checkbox"
                  :id="'toggle-' + index"
                  @change="toggleDetails(index)"
                />
                <label :for="'toggle-' + index" class="mr-2">{{ portfolio.memo }}</label><br />
                <small class="text-muted">
                (금액: {{ portfolio.amount }}원
                / 주기: {{ portfolio.rebal_period }}일)
                </small>
              </div>
              <div
              v-for="(portfolio_ticker, ticker_index) in portfolio.portfolio_ticker"
              :key="ticker_index"
              :class="{ 'd-none': !portfolio.showDetails }"
              >
              {{ portfolio_ticker.ticker.ticker_knm }}
              ({{ portfolio_ticker.ticker.symbol }}) -
              {{ portfolio_ticker.weight }}%
              </div>
              </li>
            </ul>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click.stop="showModal = false">닫기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { watch } from 'vue';
import { usePortfolioStore } from '@/stores';


export default {
  data() {
    return {
      showModal: false,
      portfolios: [],
    };
  },
  watch: {
    showModal: async function (newValue, oldValue) {
      if (newValue) {
        // showModal 값이 true일 때 포트폴리오를 로드합니다.
        const portfolioStore = usePortfolioStore();
        try {
          await portfolioStore.getAllPortfolios();
          this.portfolios = portfolioStore.portfolios;
        } catch (error) {
          console.error('포트폴리오 로딩 오류:', error);
        }
      }
    },
  },
  methods: {
    toggleDetails(index) {
      this.portfolios[index].showDetails = !this.portfolios[index].showDetails;
    },
    selectPortfolio(portfolio) {
      this.$emit('portfolio-selected', portfolio);
    },
  },
};
</script>

