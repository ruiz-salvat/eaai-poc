<template>
    <div v-if="loading" class="loading-container">
      <img :src="`/src/assets/gifs/${gifName}`" class="loading-image" />
      <i class="mt-2">Thank you for your patience! I am currently analyzing the image you provided. Please hold on while I process the information.</i>
      <b-spinner variant="primary" class="mt-2" />
    </div>
</template>

<script>
export default {
    props: {
        loading: {
            type: Boolean,
            default: () => false
        }
    },
    computed: {
      gifName() {
        let ranInt = Math.floor(Math.random() * 3)
        switch (ranInt) {
          case 0:
            return 'rat.gif'
          case 1:
            return 'eat.gif'
          case 2:
            return 'groceries.gif'
          case 3: // not used
            return 'kid.gif'
          case 4: // not used
            return 'fridge.gif'
          case 5: // not used
            return 'cat.gif'
        }
      }
    }
}
</script>

<style scoped>
.loading-image {
  max-width: 256px;
  max-height: 512px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>