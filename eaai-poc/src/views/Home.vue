<script setup>
import ConfirmationModal from '../components/ConfirmationModal.vue'
import LoadingGif from '../components/LoadingGif.vue'

import { inject } from 'vue'
const { api_key, updateKey } = inject('api_key')
</script>

<template>
  <b-container class="mt-2 mb-2">
    {{ updateKey() }}

    <b-modal ref="add-item-modal" title="Add a new item to the calendar" hide-footer>
      <!-- TODO: make component -->
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

    <b-modal ref="scan-modal" title="Scan item" hide-footer>
      <!-- TODO: make component -->
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

    <ConfirmationModal 
      ref="delete-modal" 
      @confirmed="onDeleteConfirmed"
      title="Delete item" 
      message="Are you sure you want to delete this item?"/>

    <b-button @click="scanItem()" variant="outline-primary" style="margin-right: 0.5rem" pill>
      <b-icon icon="camera"/> Scan</b-button>
    <b-button @click="openItemModal()" variant="primary"  pill>Add new item</b-button>

    <b-row class="mt-2">
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
        this.items = response.items
      })
    },
    tableDateStyle(ymd) {
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
    openItemModal() {
      this.newItem = {
        name: null,
        date: null
      }
      this.$refs['add-item-modal'].show()
    },
    scanItem() {
      this.newItem = {
        name: null,
        date: null
      }
      this.$refs['scan-modal'].show()
    },
    onSubmit(event) {
      event.preventDefault()
      
      fetch(`${import.meta.env.VITE_API_URL}items`, {
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
      fetch(`${import.meta.env.VITE_API_URL}item/${id}`, {
        method: 'DELETE'
      }).then(() => {
        this.getItems()
      })
    },
    onFileDrop(file) {
      this.getBase64(file).then(base64 => {
        this.imageBase64 = base64
      })
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = error => reject(error)
      })
    },
    scanFile(api_key) {
      console.log('scanning...', api_key)
      this.loading = true

      this.getBase64(this.file).then(base64 => {

        const jsonData = {
          "model": "gpt-4-vision-preview",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "What is the expiration date? use 1 word, include day month and year in format yyyy-mm-dd"
                },
                {
                  "type": "text",
                  "text": "What is grocery in the image? use five words maximum"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": base64
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }

        fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${api_key}`
          },
          body: JSON.stringify(jsonData)
        }).then((response) => response.json())
        .then((response) => {
          this.aiResponse = response.choices[0].message.content
          this.newItem = this.createNewItem(this.aiResponse)
          this.$refs['scan-modal'].hide()
          setTimeout(() => {this.$refs['add-item-modal'].show()}, 500)
          this.loading = false
        })

      }).catch(() => alert('No file selected!'))
    },
    createNewItem(itemStr) {
      let parts = itemStr.split('\n')
      let firstPart = parts[0]
      let restOfString = parts.slice(1).join(' ')
      return {name: restOfString, date: firstPart}
    },
    addItem() {
      fetch(`${import.meta.env.VITE_API_URL}items`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.newItem)
      }).then(() => {
        this.$refs['add-item-modal'].hide()
      })
    },
    formatDate(dateStr) {
      if (!dateStr)
        return '-'
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
