<template>
    <div class="modal fade" id="baseModal" tabindex="-1" aria-labelledby="baseModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="baseModalLabel">{{ modalTitle }}</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <slot name="body"></slot>
          </div>
          <div class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import * as bootstrap from 'bootstrap'

export default {
    props: {
        showModal: {
            type: Boolean,
            default: false
        },
        modalTitle: {
            type: String,
            default: ''
        }
    },
    watch: {
        showModal(newValue) {
            if (newValue) {
                const myModalEl = document.getElementById('baseModal')
                myModalEl.addEventListener('hide.bs.modal', () => {this.$emit('close')})
                const myModal = new bootstrap.Modal('#baseModal', {})
                myModal.show()
            }
        }
    }
}
</script>