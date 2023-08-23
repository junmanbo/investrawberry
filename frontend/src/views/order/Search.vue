<!--Search.vue-->
<template>
  <div class="form-group">
    <div class="input-group">
      <input
        type="text"
        class="form-control"
        v-model="search"
        placeholder="종목 검색..."
      />
      <div class="input-group-append">
        <button class="btn btn-outline-secondary" type="button" @click="search = ''">
          x
        </button>
      </div>
    </div>
    <ul
      class="list-group"
      v-if="searchResult.length > 0 && search.length > 0"
    >
      <li
        class="list-group-item"
        v-for="ticker in searchResult"
        :key="ticker.id"
        @click="selectTicker(ticker)"
      >
        {{ ticker.ticker_knm }} - {{ ticker.symbol }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineEmits } from 'vue';
import { debounce } from 'lodash';
import { useTickerStore } from '@/stores/ticker.store';

const tickerStore = useTickerStore();
const search = ref('');
const searchResult = computed(() => tickerStore.searchResult);

const searchTicker = debounce(() => {
  tickerStore.searchTicker(search.value);
}, 500);

watch(search, () => {
  if (!search.value) {
    tickerStore.clearSearchResult();
  } else {
    searchTicker();
  }
});

const emit = defineEmits(['ticker-selected']);
const selectTicker = (ticker) => {
  emit('ticker-selected', ticker);
};
</script>

