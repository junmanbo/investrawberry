import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';
import { router } from '@/router';
import { useAlertStore } from '@/stores';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        user: null,
        returnUrl: null
    }),
    actions: {
        async login(username, password) {
            try {
                this.user = await fetchWrapper.post(`${baseUrl}/login/access-token`, { username, password });    
                // redirect to previous url or default to home page
                router.push(this.returnUrl || '/');
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);                
            }
        },
        async refreshAccessToken() {
            try {
                this.user = await fetchWrapper.post(`${baseUrl}/login/refresh-token`);
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        logout() {
            try {
                fetchWrapper.post(`${baseUrl}/logout`);    
                this.user = null;
                router.push('/account/login');
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);                
            }
        }
    }
});
