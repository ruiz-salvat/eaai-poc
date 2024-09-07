<script setup>
import LoadingGif from '../components/LoadingGif.vue'

import { inject } from 'vue'
const { api_key, updateKey } = inject('api_key')
</script>

<template>
    <b-modal ref="scan-modal" title="Scan item" hide-footer>
      <div class="d-block">
        <b-row v-if="!loading">
          <b-col>
            <div class="image-area">
              <img v-if="file" :src="imageBase64" class="item-image" />
              <b-icon v-if="!file" icon="image" font-scale="7.5"></b-icon>
            </div>
          </b-col>
          <b-col>
            <h6>Use your camera or upload from device</h6>
            <b-form-file v-model="file" :state="Boolean(file)" @Input="onFileDrop"
              placeholder="" 
              drop-placeholder="">
            </b-form-file>
            <b-button v-if="file" @click="scanFile(api_key)" variant="primary" class="mt-2" pill>Scan</b-button>
          </b-col>
        </b-row>

        <LoadingGif :loading="loading"></LoadingGif>
      </div>
    </b-modal>
</template>

<script>
export default {

}
</script>

<style scoped>

</style>