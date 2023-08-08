// ticker.store.js
import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}/ticker`;

export const useTickerStore = defineStore({
    id: 'ticker',
    state: () => ({
        searchResult: [],
        topTickers: [], // 시가총액 상위 3개의 종목을 저장하는 상태 추가
        selectedTicker: null
    }),
    actions: {
        async searchTicker(query) {
            if (query) {
                try {
                    const response = await fetchWrapper.get(`${baseUrl}?keyword=${query}`);
                    this.searchResult = response;
                } catch (error) {
                    console.error(`Error searching for ${query}:`, error);
                }
            } else {
                this.searchResult = [];
            }
        },
        async getTopTickers() { // 시가총액 상위 3개의 종목을 조회하는 액션 추가
            try {
                const response = await fetchWrapper.get(`${baseUrl}/top`);
                this.topTickers = response;
            } catch (error) {
                console.error('Error getting top tickers:', error);
            }
        },
        selectTicker(ticker) {
            this.selectedTicker = ticker;
        }
    }
});

