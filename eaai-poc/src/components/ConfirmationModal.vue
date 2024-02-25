<template>
    <b-modal ref="confirmation-modal" hide-footer>
        <template #modal-title>
            {{ title }}
        </template>
        <div class="d-block text-center">
            {{ message }}
        </div>
        <b-button pill>Cancel</b-button>
        <b-button variant="primary" pill>Ok</b-button>
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
    methods: {
        show() {
            this.$refs['confirmation-modal'].show()
        }
    }
}
</script>