<script setup>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores';
import { ref } from 'vue';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const message = ref('');
const showMenu = ref(false);
const showMessage = () => {
    message.value = '알림 메시지입니다!';
    showMenu.value = true;
};
const hideMenu = () => {
    showMenu.value = false;
};
</script>

<template>
    <div v-if="user">
        <div class="greeting">
            <button class="greeting-icon" @click="showMessage">
                <div class="greeting-icon-bg"></div>
                <i class="fas fa-bell"></i>
            </button>
            <div class="greeting-alert"></div>
            <div class="greeting-text"> {{user.token_type}}님, 안녕하세요!</div>
            <div class="greeting-subtext">오늘도 즐거운 투자하세요 😉</div>
        </div>
        <div v-if="showMenu" @click="hideMenu" class="menu">
            {{ message }}
        </div>
        <div class="total-assets">
            <div class="total-assets-label">총 자산</div>
            <div class="total-assets-value">₩ 10,627,992.28</div>
        </div>
    </div>
</template>

<style>
@import '@/assets/home.css';
</style>
