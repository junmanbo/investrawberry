import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';
import { useAlertStore } from '@/stores';

const baseUrl = `${import.meta.env.VITE_API_URL}/order/simple`;

export const useOrderStore = defineStore({
  id: 'order',
  state: () => ({
    orders: []
  }),
  actions: {
    async postOrder(orderData) {
      try {
        const newOrder = await fetchWrapper.post(baseUrl, orderData);
        this.orders.push(newOrder);
        return newOrder;
      } catch (error) {
        const alertStore = useAlertStore();
        alertStore.error(error);
      }
    }
  }
});

