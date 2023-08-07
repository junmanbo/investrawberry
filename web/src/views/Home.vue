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
        <div class="jumbotron text-center">
            <h1 class="display-4">{{user.token_type}}님, 안녕하세요!</h1>
            <p class="lead">오늘도 좋은 하루 되세요</p>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <div class="card text-white bg-info mb-3">
                        <div class="card-header">총자산</div>
                        <div class="card-body">
                            <h5 class="card-title">₩ 10,627,992.28</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th colspan="4">관심종목</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><img src="https://mblogthumb-phinf.pstatic.net/MjAxOTA5MDVfMjgy/MDAxNTY3NjY3OTkzNjI3.WhD_wzHJcfzo141UK_81UXfSYbnlpaHbyNZwOEn1BEEg.0khjPkf1MrG78J1on0aWrStqK-zWHpIqYMnhvl4q8oQg.PNG.passtheway/1280px-Samsung_Logo.svg.png?type=w800" alt="sam"></td>
                    <td>삼성전자<br><small>005930</small></td>
                    <td>₩70,300</td>
                </tr>
                <tr>
                    <td><img src="https://cdn.senmoney.co.kr/news/photo/202106/10281_10262_4124.jpg" alt="sk"></td>
                    <td>SK하이닉스<br><small>005660</small></td>
                    <td>₩115,100</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style>
@import '@/assets/home.css';
</style>
