<template>
    <b-modal ref="confirmation-modal" @hide="onHide" hide-footer>
        <template #modal-title>
            {{ title }}
        </template>
        <div class="d-block text-center">
            <div>{{ message }}</div>
            <b-button @Click="okClicked" variant="primary" class="mt-2" pill>Ok</b-button>
        </div>
    </b-modal>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        },
        message: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            itemId: null
        }
    },
    methods: {
        show(itemId) {
            this.itemId = itemId
            this.$refs['confirmation-modal'].show()
        },
        okClicked() {
            this.$emit('confirmed', this.itemId)
            this.$refs['confirmation-modal'].hide()
        },
        onHide() {
            this.itemId = null
        }
    }
}
</script>