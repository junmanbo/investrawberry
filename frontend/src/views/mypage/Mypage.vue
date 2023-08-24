<script setup>
import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
const user = authStore.user;
</script>

<template>
    <div class="card m-3">
        <div class="row">
            <div class="col-sm-4">
                <h4 class="card-header">Menu</h4>
                <div class="card-body">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <router-link to="/mypage/apikey" class="nav-link">API Key 관리</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/edit" class="nav-link">회원정보 수정</router-link>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="col-sm-4">
                <h4 class="card-header">Profile</h4>
                <div class="card-body">
                    <img src="https://via.placeholder.com/150" alt="Profile Picture" class="img-thumbnail">
                    <h5>{{ user.username }}</h5>
                </div>
            </div>
            <div class="col-sm-4">
                <h4 class="card-header">공시사항</h4>
                <div class="card-body">
                    <ul>
                        <li>공지사항 1</li>
                        <li>공지사항 2</li>
                        <li>공지사항 3</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

