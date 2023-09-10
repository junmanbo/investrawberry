import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';
import { router } from '@/router';
import { useAlertStore, useUsersStore } from '@/stores';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        user: JSON.parse(sessionStorage.getItem('user')),
        returnUrl: null
    }),
    actions: {
        async login(username, password) {
            try {
                const user = await fetchWrapper.post(`${baseUrl}/login/access-token`, { username, password });    
                this.user = user

                // store user details and jwt in session storage to keep user logged in between page refreshes
                sessionStorage.setItem('user', JSON.stringify(user));

                // redirect to previous url or default to home page
                router.push(this.returnUrl || '/');

            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);                
            }
        },
        async refreshAccessToken() {
            try {
                const user = await fetchWrapper.post(`${baseUrl}/login/refresh-token`);
                this.user = user
                sessionStorage.setItem('user', JSON.stringify(user));

            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);
            }
        },
        async logout() {
            try {
                await fetchWrapper.post(`${baseUrl}/logout`);    
                this.user = null;
                sessionStorage.removeItem('user');
                router.push('/account/login');
            } catch (error) {
                const alertStore = useAlertStore();
                alertStore.error(error);                
            }
        }
    }
});

