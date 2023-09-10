import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';
import { useAlertStore } from '@/stores';

const baseUrl = `${import.meta.env.VITE_API_URL}/exchangekeys`;

export const useApiKeyStore = defineStore({
    id: 'apikey',
    state: () => ({
        apiKeys: []
    }),
    actions: {
        async getApiKeys() {
            try {
                const keys = await fetchWrapper.get(baseUrl);
                this.apiKeys = keys;
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        async deleteKey(id) {
            try {
                await fetchWrapper.delete(`${baseUrl}${id}`);
                // Refresh the list after successful deletion
                this.getApiKeys();
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        async postKey(exchange_nm, access_key, secret_key, account = null) {
            try {
                const keyData = {
                    exchange_nm: exchange_nm,
                    exchange_key_in: {
                        access_key: access_key,
                        secret_key: secret_key,
                    }
                };

                if (account) {
                    keyData.exchange_key_in.account = account;
                }

                const newKey = await fetchWrapper.post(baseUrl, keyData);

                // Refresh the list after successful addition
                this.getApiKeys();

                return newKey;
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        }
    }
});

