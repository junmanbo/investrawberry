// ticker.store.js
import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}/ticker`;

export const useTickerStore = defineStore({
    id: 'ticker',
    state: () => ({
        searchResult: [],
        selectedTicker: null // 선택한 ticker 정보를 저장하는 상태 추가
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
        selectTicker(ticker) { // 선택한 ticker 정보를 저장하는 액션 추가
            this.selectedTicker = ticker;
        }
    }
});

