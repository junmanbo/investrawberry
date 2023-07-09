<template>
    <div>
        <h3>API Keys</h3>
        <div v-if="apiKeyStore.apiKeys.length === 0">
            등록된 키가 없습니다. 아래의 버튼을 눌러 키를 등록하세요.
        </div>
        <div v-else>
            <ul>
                <li v-for="(key, index) in apiKeyStore.apiKeys" :key="index">
                    <strong>거래소: </strong>{{ key.exchange.exchange_nm }}
                    <br/>
                    <strong>Access Key: </strong>{{ key.access_key }}
                    <button @click="deleteKey(key.id)">삭제</button>
                </li>
            </ul>
        </div>
        <button class="btn btn-primary" @click="showModal = true">API Key 추가</button>

        <!-- API Key Registration Modal -->
        <div v-if="showModal" class="modal">
            <div class="modal-content">
                <span class="close-button" @click="showModal = false">&times;</span>

                <h2>Add New API Key</h2>

                <form @submit.prevent="submitForm">
                    <label for="exchange_nm">거래소:</label>
                    <select id="exchange_nm" v-model="newKey.exchange_nm" required>
                        <option disabled value="">거래소 선택</option>
                        <option>UPBIT</option>
                        <option>KIS</option>
                        <option>KIS_INTL</option>
                    </select>

                    <label for="access_key">Access Key:</label>
                    <input id="access_key" v-model="newKey.access_key" required>

                    <label for="secret_key">Secret Key:</label>
                    <input id="secret_key" v-model="newKey.secret_key" required>

                    <label for="account">계좌 (선택):</label>
                    <input id="account" v-model="newKey.account">

                    <button type="submit">등록</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useApiKeyStore } from '@/stores';

const apiKeyStore = useApiKeyStore();

onMounted(() => {
    apiKeyStore.getApiKeys();
});

const deleteKey = (id) => {
    apiKeyStore.deleteKey(id);
};

const showModal = ref(false);
const newKey = ref({
    exchange_nm: '',
    access_key: '',
    secret_key: '',
    account: ''
});

const submitForm = () => {
    apiKeyStore.postKey(newKey.value.exchange_nm, newKey.value.access_key, newKey.value.secret_key, newKey.value.account);
    showModal.value = false;
};
</script>

<style scoped>
.modal {
    display: block;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.4);
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
}

.close-button {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}

.close-button:hover,
.close-button:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}

form label {
    display: block;
    margin-top: 10px;
}

</style>

