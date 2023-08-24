import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';
import { useAlertStore } from '@/stores';

const baseUrl = `${import.meta.env.VITE_API_URL}/balance`;

export const useBalanceStore = defineStore({
    id: 'balance',
    state: () => ({
        balances: {}
    }),
    actions: {
        async getBalances() {
            try {
                const response = await fetchWrapper.get(baseUrl);
                this.balances = response;
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        }
    }
});

