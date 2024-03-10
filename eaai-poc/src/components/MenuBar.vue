<template>
    <div class="menu-bar">
        <b-sidebar id="sidebar-1" title="Your profile" shadow>
            <div class="px-3 py-2">
                <div class="centered-content">
                    <img src="../assets/avatars/profile.jpeg" class="avatar-image-lg"/>
                    <i>username</i>
                </div>
                <p class="mt-2">
                Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis
                in, egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
                </p>
            </div>
            <div class="centered-content-bt mb-4">
                <img src="../assets/ui/logo.png" style="max-height: 4rem; max-width: 4rem;"/>
            </div>
        </b-sidebar>

      <div class="menu-element">
        <img v-b-toggle.sidebar-1 src="../assets/avatars/profile.jpeg" class="avatar-image-sm"/>
      </div>
      <div class="menu-element">
        <router-link to="/">
            <div class="icon-container" :class="selectedClass('home')">
                <div>
                    <b-icon icon="house-fill"></b-icon>
                </div>
                <div>Home</div>
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
      <div class="menu-element">
        <router-link to="/plan">
            <div class="icon-container" :class="selectedClass('plan')">
                <div>
                    <b-icon icon="calendar3"></b-icon>
                </div>
                <div>Plan</div>
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
  background-color: #0d6efd;
  color: #f0ffff;
  width: 100%;
  display: flex;
  flex-direction: row;
}

.menu-element {
    padding-right: 1rem;
    padding-left: 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
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
    background-color: #f0ffff;
    color: #0d6efd;
    border-radius: 8px;
}

.avatar-image-sm {
    border-radius: 50%;
    max-height: 2.5rem;
    max-width: 2.5rem;
}

.avatar-image-lg {
    border-radius: 50%;
    max-height: 12.5rem;
    max-width: 12.5rem;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.4);
}

.centered-content {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.centered-content-bt {
    position: absolute;
    bottom: 0;
    width: 100%;
    display: flex;
    justify-content: center;
}

.avatar-image:hover {
    cursor: pointer;
}
</style>