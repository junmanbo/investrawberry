// portfolio.store.js
import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}/portfolio`;

export const usePortfolioStore = defineStore({
  id: 'portfolio',
  state: () => ({
    portfolio: null,
    portfolios: [] // all portfolios 를 저장할 변수 추가
  }),
  actions: {
    async getPortfolio(portfolio_id) {
      try {
        const response = await fetchWrapper.get(`${baseUrl}?portfolio_id=${portfolio_id}`);
        this.portfolio = response;
      } catch (error) {
        console.error(`Error getting portfolio with ID ${portfolio_id}:`, error);
      }
    },
    async getAllPortfolios() { // 모든 포트폴리오를 가져오는 액션 추가
      try {
        const response = await fetchWrapper.get(`${baseUrl}/all`);
        this.portfolios = response;
      } catch (error) {
        console.error('Error getting all portfolios:', error);
      }
    },
    async createPortfolio(payload) {
      try {
        const response = await fetchWrapper.post(baseUrl, payload);
        // 서버에서 생성된 포트폴리오 정보를 반환합니다.
        return response;
      } catch (error) {
        console.error('Error creating portfolio:', error);
        return null; // 오류 발생 시 null 반환
      }
    },
  }
});

