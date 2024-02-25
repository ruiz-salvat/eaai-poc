<template>
  <b-container>
    <b-modal ref="bv-modal" hide-footer>
      <template #modal-title>
        Add a new item to the calendar
      </template>
      <div class="d-block text-center">
        <b-form @submit="onSubmit">
          <b-form-group
            label="Name:"
            label-for="input-1">
            <b-form-input
              id="input-1"
              v-model="newItem.name"
              type="text"
              placeholder="Enter email"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            label="Expiry date:"
            label-for="input-2">
            <b-form-input
              id="input-2"
              v-model="newItem.date"
              type="text"
              placeholder="02-02-2023"
              required
            ></b-form-input>
          </b-form-group>

          <b-button type="submit" variant="primary">Add</b-button>
        </b-form>
      </div>
    </b-modal>

    <b-row>
      <b-button @click="openItemModal()">Add new item</b-button>
    </b-row>

    <b-row>
      <b-calendar 
        v-model="value" 
        @context="onContext" 
        block 
        :date-info-fn="dateClass" 
        locale="en-US">
      </b-calendar>
    </b-row>
    
    <b-row>
      <b-table :items="items">
        <template #cell(date)="data">
          <span :style="tableDateStyle(data.item.date)">{{ data.item.date }}</span>
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
      return this.items.map(x => x.date).includes(ymd) ? 'item-expiry' : ''
    },
    tableDateStyle(dateStr) {
      let date = Date.parse(dateStr)
      if (date < new Date())
        return 'color: red'
      return ''
    },
    openItemModal() {
      this.$refs['bv-modal'].show()
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
        this.$refs['bv-modal'].hide()
        this.getItems()
        this.newItem = {name: null, date: null}
      })
    }
  }
}
</script>

<style>
.item-expiry {
  background-color: #ff5959;
}
</style>
