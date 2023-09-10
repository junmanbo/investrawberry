import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';
import { useAuthStore } from '@/stores';

const baseUrl = `${import.meta.env.VITE_API_URL}/users`;

export const useUsersStore = defineStore({
    id: 'users',
    state: () => ({
        user: JSON.parse(sessionStorage.getItem('user')),
    }),
    actions: {
        async register(user) {
            await fetchWrapper.post(`${baseUrl}/open`, user);
        },
        async getUserInfo() {
            const userInfo = await fetchWrapper.get(`${baseUrl}/me`);
            this.user = {...this.user, user_name: userInfo.full_name};
            sessionStorage.setItem('user', JSON.stringify(this.user));
        }
    }
});

