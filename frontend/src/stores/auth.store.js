import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';
import { router } from '@/router';
import { useAlertStore } from '@/stores';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from session storage to enable user to stay logged in
        user: JSON.parse(sessionStorage.getItem('user')),
        returnUrl: null
    }),
    actions: {
        async login(username, password) {
            try {
                this.user = await fetchWrapper.post(`${baseUrl}/login/access-token`, { username, password });    

                // store user details and jwt in session storage to keep user logged in between page refreshes
                sessionStorage.setItem('user', JSON.stringify(this.user));

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
                sessionStorage.setItem('user', JSON.stringify(this.user));
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        logout() {
            try {
                fetchWrapper.post(`${baseUrl}/logout`);    
                this.state.user = null;
                sessionStorage.removeItem('user');
                router.push('/account/login');
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);                
            }
        }
    }
});

