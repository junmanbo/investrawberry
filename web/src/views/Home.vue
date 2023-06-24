<script setup>
import { storeToRefs } from 'pinia';

import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);
</script>

<template>
    <div v-if="user">
        <h1>Hi {{user.fullName}}!</h1>
        <p>인베스트로베리에 오신 것을 환영합니다!</p>
        <p><router-link to="/users">유저 관리</router-link></p>
    </div>
</template>
