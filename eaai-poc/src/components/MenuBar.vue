<template>
    <div class="menu-bar">
      <div class="menu-element">Title...</div>
      <div class="menu-element">
        <router-link to="/">
            <div class="icon-container" :class="selectedClass('home')">
                <div>
                    <b-icon icon="calendar3"></b-icon>
                </div>
                <div>Home</div>
            </div>
        </router-link>
      </div>
      <div class="menu-element">
        <router-link to="/scan">
            <div class="icon-container" :class="selectedClass('scan')">
                <div>
                    <b-icon icon="camera"></b-icon>
                </div>
                <div>Scan</div>
            </div>
        </router-link>
      </div>
      <div class="menu-element">
        <router-link to="/cook">
            <div class="icon-container" :class="selectedClass('cook')">
                <div>
                    <b-icon icon="emoji-heart-eyes"></b-icon>
                </div>
                <div>Cook</div>
            </div>
        </router-link>
      </div>
    </div>
</template>

<script>
export default {
    methods: {
        selectedClass(pathName) {
            if (this.$route.name === pathName)
                return 'active-tab'
            return ''
        }
    }
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.menu-bar {
  background-color: #002fca;
  color: #f0ffff;
  width: 100%;
  display: flex;
  flex-direction: row;
}

.menu-element {
  padding-right: 1rem;
  padding-left: 1rem;
}

.icon-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-left: 3px;
    padding-right: 3px;
    margin-top: 3px;
    margin-bottom: 3px;
    color:#f0ffff;
}

.icon-container:hover {
    color:#797979;
}

.active-tab {
    /* border: solid white 1px; */
    background-color: #f0ffff;
    color: #002fca;
    border-radius: 8px;
}
</style>