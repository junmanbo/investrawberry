<script setup>
import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
</script>

<template>
    <nav v-show="authStore.user" class="navbar navbar-expand navbar-dark bg-dark">
        <div class="navbar-nav">
            <router-link to="/" class="nav-item nav-link">홈</router-link>
            <router-link to="/users" class="nav-item nav-link">유저</router-link>
            <button @click="authStore.logout()" class="btn btn-link nav-item nav-link">로그아웃</button>
        </div>
    </nav>
</template>
