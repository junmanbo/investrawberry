<template>
  <div class="modal fade" :id="modalId" tabindex="-1" role="dialog" aria-labelledby="modalTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalTitle">{{ title }}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="closeModal">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          {{ body }}
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="closeModal">닫기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    body: String,
    modalId: String, // 고유한 모달 ID
  },
  methods: {
    closeModal() {
      // 부모 컴포넌트로부터 전달된 이벤트를 통해 모달 닫기
      this.$emit('close-modal');
    },
  },
};
</script>

<style scoped>
/* 모바일 뷰를 위한 스타일 */
@media (max-width: 575.98px) {
  .modal-dialog {
    max-width: 90%;
  }
}
</style>

