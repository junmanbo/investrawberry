<template>
  <div class="form-group">
    <div class="dropdown">
      <button class="btn btn-secondary dropdown-toggle" type="button" id="orderMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        {{ selectedMenu }}
      </button>
      <div class="dropdown-menu" aria-labelledby="orderMenuButton">
        <a class="dropdown-item" href="#" @click="selectMenu('SIMPLE')">단순주문</a>
        <a class="dropdown-item" href="#" @click="selectMenu('PORTFOLIO')">포트폴리오</a>
        <a class="dropdown-item" href="#" @click="selectMenu('TWAP')">시간분할매매</a>
        <a class="dropdown-item" href="#" @click="selectMenu('DCA')">분할적립투자</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { defineEmits } from 'vue';

const router = useRouter();
const props = defineProps({
  selectedMenu: String,
});
const emit = defineEmits(['update:selected-menu']);

const selectMenu = (menu) => {
  emit('update:selected-menu', menu);
};

watch(() => props.selectedMenu, (newVal) => {
  switch (newVal) {
    case 'PORTFOLIO':
      router.push('/order/portfolio');
      break;
    case 'TWAP':
      //router.push('/order/twap');
      break;
    case 'DCA':
      //router.push('/order/dca');
      break;
    default:
      router.push('/order');
      break;
  }
});
</script>

