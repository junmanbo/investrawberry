<script setup>
import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
</script>

<template>
    <nav v-show="authStore.user" class="navbar navbar-expand navbar-light bg-light">
        <router-link to="/" class="navbar-brand">Investrawberry</router-link>
        <div class="navbar-nav ml-auto">
            <router-link to="/balance" class="nav-item nav-link text-dark">자산</router-link>
            <router-link to="/strategy" class="nav-item nav-link text-dark">전략</router-link>
            <router-link to="/mypage" class="nav-item nav-link text-dark">마이페이지</router-link>
            <button @click="authStore.logout()" class="btn btn-link nav-item nav-link text-dark">로그아웃</button>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    background-color: white;
}
</style>

