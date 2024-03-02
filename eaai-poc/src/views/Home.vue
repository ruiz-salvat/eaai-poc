<script setup>
import ConfirmationModal from '../components/ConfirmationModal.vue'
</script>

<template>
  <b-container>
    <b-modal ref="add-item-modal" title="Add a new item to the calendar" hide-footer>
      <div class="d-block">
        <b-form @submit="onSubmit">
          <b-form-group
            label="Name:"
            label-for="input-1">
            <b-form-input
              id="input-1"
              v-model="newItem.name"
              type="text"
              placeholder="Milk"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label="Expiry date:"
            label-for="input-2"
            class="mt-2">
            <b-form-datepicker 
                id="input-2"
                v-model="newItem.date"
                required />
          </b-form-group>
          
          <div class="text-center">
            <b-button type="submit" variant="primary" class="mt-2" pill>Add</b-button>
          </div>
        </b-form>
      </div>
    </b-modal>

    <ConfirmationModal 
      ref="delete-modal" 
      @confirmed="onDeleteConfirmed"
      title="Delete item" 
      message="Are you sure you want to delete this item?"/>

    <b-row class="mt-2 mb-2">
      <b-button @click="openItemModal()" variant="primary" pill>Add new item</b-button>
    </b-row>

    <b-row class="mt-2 mb-2">
      <b-calendar 
        v-model="value" 
        @context="onContext" 
        block 
        :date-info-fn="dateClass" 
        locale="en-US">
      </b-calendar>
    </b-row>
    
    <b-row class="mt-2 mb-2">
      <b-table 
        :items="items"
        :fields="fields"
        thead-class="d-none"
        hover
        @row-clicked="tableRowClicked">
        <template #cell(date)="data">
          <span :style="tableDateStyle(data.item.date)">{{ formatDate(data.item.date) }}</span>
        </template>
        <template #cell(actions)="data">
          <b-icon 
            @click="deleteItem(data.item.id)"
            icon="trash-fill" 
            variant="danger" />
        </template>
      </b-table>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      items: [],
      fields: [
        {key: 'name'},
        {key: 'date'},
        {key: 'actions'}
      ],
      value: null,
      newItem: {
        name: null,
        date: null
      }
    }
  },
  created() {
    this.getItems()
  },
  methods: {
    getItems() {
      fetch('http://127.0.0.1:5000/items')
      .then((response) => response.json())
      .then((response) => {
        this.items = response.items
      })
    },
    dateClass(ymd, date) {
      if (this.items.map(x => x.date).includes(ymd)) {
        let d = Date.parse(ymd)
        if (d < new Date())
          return 'item-expiry-danger'
        else if (d < new Date(Date.now() + 24 * 60 * 60 * 1000))
          return 'item-expiry-warning'
        else
          return 'item-expiry-ok'
      }
      return ''
    },
    tableDateStyle(dateStr) {
      let date = Date.parse(dateStr)
      if (date < new Date())
        return 'color: red'
      return ''
    },
    openItemModal() {
      this.$refs['add-item-modal'].show()
    },
    onSubmit(event) {
      event.preventDefault()
      
      fetch('http://127.0.0.1:5000/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.newItem)
      }).then(() => {
        this.$refs['add-item-modal'].hide()
        this.getItems()
        this.newItem = {name: null, date: null}
      })
    },
    tableRowClicked(row) {
      console.log('row clicked', row)
    },
    deleteItem(id) {
      this.$refs['delete-modal'].show(id)      
    },
    onDeleteConfirmed(id) {
      fetch(`http://127.0.0.1:5000/item/${id}`, {
        method: 'DELETE'
      }).then(() => {
        this.getItems()
      })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const day = date.getDate()
      const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
      ]
      const month = monthNames[date.getMonth()]
      const year = date.getFullYear()
      return `${day} ${month} ${year}`
    }
  }
}
</script>

<style>
.item-expiry-danger {
  background-color: #ff5959;
}

.item-expiry-warning {
  background-color: #fff459;
}

.item-expiry-ok {
  background-color: #59ff67;
}
</style>
