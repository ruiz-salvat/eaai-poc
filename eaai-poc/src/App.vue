<script setup>
import MenuBar from './components/MenuBar.vue'
import { ref, provide } from 'vue'

let api_key = ref(null)

function updateKey() {
  fetch('http://172.19.0.2:5000/api_key')
  .then((response) => response.text())
  .then((response) => {
    api_key.value = response
  })
}

provide('api_key', {
  api_key,
  updateKey
})
</script>

<template>
  <div>
    <MenuBar />
    
    <div>
      <router-view></router-view>
    </div>
  </div>  
</template>
