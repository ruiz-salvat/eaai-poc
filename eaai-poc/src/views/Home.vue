<script setup>
import ConfirmationModal from '../components/ConfirmationModal.vue'
import LoadingGif from '../components/LoadingGif.vue'

import { inject } from 'vue'
const { api_key, updateKey } = inject('api_key')
</script>

<template>
  <div>
    {{ updateKey() }}
    
    <ConfirmationModal 
      ref="delete-modal" 
      @confirmed="onDeleteConfirmed"
      title="Delete item" 
      message="Are you sure you want to delete this item?"/>

    <v-btn @click="scanItem()" style="margin-right: 0.5rem">
      <b-icon icon="camera"/> Scan
    </v-btn>
    <v-btn @click="openItemModal()">Add new item</v-btn>

    <v-data-table-server :headers="headers" :items="items"></v-data-table-server>
     {{ this.items }}

    <!-- <b-row class="mt-2">
      <b-table 
        :items="items"
        :fields="fields"
        thead-class="d-none"
        hover
        @row-clicked="tableRowClicked">
        <template #cell(date)="data">
          <span :class="tableDateStyle(data.item.date)">{{ formatDate(data.item.date) }}</span>
        </template>
        <template #cell(actions)="data">
          <b-icon 
            @click="deleteItem(data.item.id)"
            icon="trash-fill" 
            variant="danger" />
        </template>
      </b-table>
    </b-row> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [
    {
      name: 'African Elephant',
      species: 'Loxodonta africana',
      diet: 'Herbivore',
      habitat: 'Savanna, Forests',
    },
    // ... more items
  ],
      fields: [
        {key: 'name'},
        {key: 'date'},
        {key: 'actions'}
      ],

      headers: [
        { title: 'Name', key: 'name', align: 'end' },
        { title: 'Date', key: 'date', align: 'end' },
        // { title: 'Iron (%)', key: 'iron', align: 'end' },
      ],

      newItem: {
        name: null,
        date: null
      },
      file: null,
      imageBase64: '',
      aiResponse: '',
      loading: false
    }
  },
  created() {
    this.getItems()
  },
  methods: {
    getItems() {
      fetch(`${import.meta.env.VITE_API_URL}items`)
      .then((response) => response.json())
      .then((response) => {
        console.log('items', response)
        // this.items = JSON.parse(JSON.stringify(response))
      })
    },
  //   tableDateStyle(ymd) {
  //     if (this.items.map(x => x.date).includes(ymd)) {
  //       let d = Date.parse(ymd)
  //       if (d < new Date())
  //         return 'item-expiry-danger'
  //       else if (d < new Date(Date.now() + 24 * 60 * 60 * 1000))
  //         return 'item-expiry-warning'
  //       else
  //         return 'item-expiry-ok'
  //     }
  //     return ''
  //   },
  //   openItemModal() {
  //     this.newItem = {
  //       name: null,
  //       date: null
  //     }
  //     this.$refs['add-item-modal'].show()
  //   },
  //   scanItem() {
  //     this.newItem = {
  //       name: null,
  //       date: null
  //     }
  //     this.$refs['scan-modal'].show()
  //   },
  //   onSubmit(event) {
  //     event.preventDefault()
      
  //     fetch(`${import.meta.env.VITE_API_URL}items`, {
  //       method: 'POST',
  //       headers: {
  //           'Content-Type': 'application/json'
  //       },
  //       body: JSON.stringify(this.newItem)
  //     }).then(() => {
  //       this.$refs['add-item-modal'].hide()
  //       this.getItems()
  //       this.newItem = {name: null, date: null}
  //     })
  //   },
  //   tableRowClicked(row) {
  //     console.log('row clicked', row)
  //   },
  //   deleteItem(id) {
  //     this.$refs['delete-modal'].show(id)      
  //   },
  //   onDeleteConfirmed(id) {
  //     fetch(`${import.meta.env.VITE_API_URL}item/${id}`, {
  //       method: 'DELETE'
  //     }).then(() => {
  //       this.getItems()
  //     })
  //   },
  //   onFileDrop(file) {
  //     this.getBase64(file).then(base64 => {
  //       this.imageBase64 = base64
  //     })
  //   },
  //   getBase64(file) {
  //     return new Promise((resolve, reject) => {
  //       const reader = new FileReader()
  //       reader.readAsDataURL(file)
  //       reader.onload = () => resolve(reader.result)
  //       reader.onerror = error => reject(error)
  //     })
  //   },
  //   scanFile(api_key) {
  //     this.loading = true

  //     this.getBase64(this.file).then(base64 => {

  //       const jsonData = {
  //         "model": "gpt-4-vision-preview",
  //         "messages": [
  //           {
  //             "role": "user",
  //             "content": [
  //               {
  //                 "type": "text",
  //                 "text": "What is the expiration date? use 1 word, include day month and year in format yyyy-mm-dd"
  //               },
  //               {
  //                 "type": "text",
  //                 "text": "What is grocery in the image? use five words maximum"
  //               },
  //               {
  //                 "type": "image_url",
  //                 "image_url": {
  //                   "url": base64
  //                 }
  //               }
  //             ]
  //           }
  //         ],
  //         "max_tokens": 300
  //       }

  //       fetch('https://api.openai.com/v1/chat/completions', {
  //         method: 'POST',
  //         headers: {
  //           'Content-Type': 'application/json',
  //           'Authorization': `Bearer ${api_key}`
  //         },
  //         body: JSON.stringify(jsonData)
  //       }).then((response) => response.json())
  //       .then((response) => {
  //         this.aiResponse = response.choices[0].message.content
  //         this.newItem = this.createNewItem(this.aiResponse)
  //         this.$refs['scan-modal'].hide()
  //         setTimeout(() => {this.$refs['add-item-modal'].show()}, 500)
  //         this.loading = false
  //       })

  //     }).catch(() => alert('No file selected!'))
  //   },
  //   createNewItem(itemStr) {
  //     let parts = itemStr.split('\n')
  //     let firstPart = parts[0]
  //     let restOfString = parts.slice(1).join(' ')
  //     return {name: restOfString, date: firstPart}
  //   },
  //   addItem() {
  //     fetch(`${import.meta.env.VITE_API_URL}items`, {
  //       method: 'POST',
  //       headers: {
  //           'Content-Type': 'application/json'
  //       },
  //       body: JSON.stringify(this.newItem)
  //     }).then(() => {
  //       this.$refs['add-item-modal'].hide()
  //     })
  //   },
  //   formatDate(dateStr) {
  //     if (!dateStr)
  //       return '-'
  //     const date = new Date(dateStr)
  //     const day = date.getDate()
  //     const monthNames = [
  //       "January", "February", "March", "April", "May", "June",
  //       "July", "August", "September", "October", "November", "December"
  //     ]
  //     const month = monthNames[date.getMonth()]
  //     const year = date.getFullYear()
  //     return `${day} ${month} ${year}`
  //   }
  }
}
</script>

<style scoped>
.item-image {
  max-width: 300px;
  max-height: 300px;
}

.image-area {
  border: solid 1px #797979;
  height: 300px;
  width: 225px;
  max-width: 300px;
  max-height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.item-expiry-danger {
  color: #6e0909;
  font-weight: bold;
}

.item-expiry-warning {
  color: #5a530b;
  font-weight: bold;
}

.item-expiry-ok {
  color: #0e5529;
  font-weight: bold;
}
</style>
