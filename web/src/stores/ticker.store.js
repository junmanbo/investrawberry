import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}/ticker`;

export const useTickerStore = defineStore({
    id: 'ticker',
    state: () => ({
        searchResult: []
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
        }
    }
});

