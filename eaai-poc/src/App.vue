<script setup>
import MenuBar from './components/MenuBar.vue'
</script>

<template>
  <div>
    <MenuBar />
    
    <div>
      <router-view></router-view>
    </div>
  </div>  
</template>
