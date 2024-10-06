<template>
    <ModalBase :showModal="showModal" modalTitle="New item">
      <template v-slot:body>
        <div class="mb-3">
          <label for="nameInput" class="form-label">Name</label>
          <input v-model="newItem.name" type="text" class="form-control" id="nameInput">
        </div>

        <div class="mb-3">
          <label for="dateInput" class="form-label">Date</label>
          <input v-model="newItem.date" type="text" class="form-control" id="dateInput" aria-describedby="dateHelp">
          <div id="datelHelp" class="form-text">Enter the expiry date of the product.</div>
        </div>
      </template>

      <template v-slot:footer>
        <button @click="addNewItem()" type="submit" class="btn btn-primary">Add</button>
      </template>
    </ModalBase>
</template>

<script>
import ModalBase from './base_components/Modal.vue'

export default {
  components: {ModalBase},
  props: {
    showModal: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      newItem: {
        name: '',
        date: ''
      }
    }
  },
  methods: {
    addNewItem() {
      fetch(`${import.meta.env.VITE_API_URL}items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.$cookies.get('access-token')}`
        },
        body: JSON.stringify(this.newItem)
      }).then((response) => response.json()).then((data) => {
        console.log('data..', data)
      })
    }
  }
}
</script>