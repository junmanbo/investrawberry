<template>
  <div class="text-right mt-3">
    <h5>{{ user.user_name }}님</h5>
    <button class="btn btn-secondary" @click="logout">로그아웃</button>
  </div>
  <div class="container">
    <div class="card m-3">
      <div class="row">
        <div class="col-md-4">
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
        <div class="col-md-4">
          <h4 class="card-header">공지사항</h4>
          <div class="card-body">
            <ul class="list-group">
              <li class="list-group-item">공지사항 1</li>
              <li class="list-group-item">공지사항 2</li>
              <li class="list-group-item">공지사항 3</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media (max-width: 767px) {
  .col-md-4 {
    margin-bottom: 20px;
  }
}
</style>

<script setup>
import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
const user = authStore.user;
const logout = async () => {
  try {
    await authStore.logout();
  } catch (error) {
    console.log(error);
  }
};
</script>

