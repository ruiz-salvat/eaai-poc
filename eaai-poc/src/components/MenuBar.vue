<template>
    <div class="menu-bar">
        <!-- <b-sidebar id="sidebar-1" title="Your profile" shadow>
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
        </b-sidebar> -->

      <div class="menu-element">
        <img v-b-toggle.sidebar-1 src="../assets/avatars/profile.jpeg" class="avatar-image-sm"/>
      </div>
      <div class="menu-element">
        <router-link to="/home">
            <div class="icon-container" :class="selectedClass('home')">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house" viewBox="0 0 16 16">
                        <path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293zM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5z"/>
                    </svg>
                </div>
                <div>Home</div>
            </div>
        </router-link>
      </div>
      <div class="menu-element">
        <router-link to="/cook">
            <div class="icon-container" :class="selectedClass('cook')">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-emoji-heart-eyes" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path d="M11.315 10.014a.5.5 0 0 1 .548.736A4.5 4.5 0 0 1 7.965 13a4.5 4.5 0 0 1-3.898-2.25.5.5 0 0 1 .548-.736h.005l.017.005.067.015.252.055c.215.046.515.108.857.169.693.124 1.522.242 2.152.242s1.46-.118 2.152-.242a27 27 0 0 0 1.109-.224l.067-.015.017-.004.005-.002zM4.756 4.566c.763-1.424 4.02-.12.952 3.434-4.496-1.596-2.35-4.298-.952-3.434m6.488 0c1.398-.864 3.544 1.838-.952 3.434-3.067-3.554.19-4.858.952-3.434"/>
                    </svg>
                </div>
                <div>Cook</div>
            </div>
        </router-link>
      </div>
      <div class="menu-element">
        <router-link to="/plan">
            <div class="icon-container" :class="selectedClass('plan')">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar3-week" viewBox="0 0 16 16">
                        <path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2M1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857z"/>
                        <path d="M12 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2m-5 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2m2-3a1 1 0 1 0 0-2 1 1 0 0 0 0 2m-5 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2"/>
                    </svg>
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