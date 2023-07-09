<script setup>
import { storeToRefs } from 'pinia';

import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);
</script>

<template>
    <div v-if="user">
        <h1>Hi {{user.full_name}}!</h1>
        <p>인베스트로베리에 오신 것을 환영합니다!</p>
    </div>
</template>
