<template>
    <div v-if="loading" class="loading-container">
      <img src="../assets/gifs/eat.gif" class="loading-image" />
      <i class="mt-2">Thank you for your patience! I am currently analyzing the image you provided. Please hold on while I process the information.</i>
    </div>
</template>

<script>
export default {
    props: {
        loading: {
            type: Boolean,
            default: () => false
        }
    }
}
</script>

<style scoped>
.loading-image {
  max-width: 400px;
  max-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>