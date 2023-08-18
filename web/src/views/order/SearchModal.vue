<template>
  <div>
    <button @click="showModal = true" class="btn btn-primary">
      + 종목추가
    </button>
    <div class="modal" tabindex="-1" role="dialog" :class="{ 'd-block': showModal, 'd-none': !showModal }">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">종목추가</h5>
            <button type="button" class="close" @click.stop="showModal = false">
              <span>&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <Search @ticker-selected="tickerSelected" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click.stop="showModal = false">닫기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Search } from '@/views/order';

export default {
  components: {
    Search,
  },
  data() {
    return {
      showModal: false,
    };
  },
  methods: {
    tickerSelected(ticker) {
      this.$emit('ticker-selected', ticker);
      this.showModal = false;
    },
  },
};
</script>

