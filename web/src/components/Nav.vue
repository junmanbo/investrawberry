<script setup>
import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
</script>
<template>
    <div v-show="authStore.user" class="fixed-bottom">
        <div class="tab-menu">
            <div class="tab-menu-bg"></div>
            <router-link to="/" class="tab-menu-item">
                <i class="fas fa-home"></i>
            </router-link>
            <router-link to="/balance" class="tab-menu-item">
                <i class="fas fa-wallet"></i>
            </router-link>
            <router-link to="/order" class="tab-menu-item">
                <i class="fas fa-shopping-cart"></i>
            </router-link>
            <router-link to="/mypage" class="tab-menu-item">
                <i class="fas fa-user"></i>
            </router-link>
        </div>
    </div>
</template>

<style>
@import '@/assets/nav.css';
</style>
