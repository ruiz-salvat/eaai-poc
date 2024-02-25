<template>
  <b-container>
    <b-modal ref="bv-modal" hide-footer>
      <template #modal-title>
        Do you want to add this item to the calendar?
      </template>
      <div class="d-block text-center">
        <b-row>
          <b-col>Name:</b-col>
          <b-col>{{ this.newItem.name }}</b-col>
        </b-row>
        <b-row>
          <b-col>Date:</b-col>
          <b-col>{{ this.newItem.date }}</b-col>
        </b-row>
      </div>
      <b-button class="mt-3" block @Click="addItem()">Add</b-button>
    </b-modal>

    <div class="file-upload-area">
      <h4>Use your camera</h4>
      <!-- <input id="input-camera" type="file" accept="image/*;capture=camera" /> -->
      <b-form-file v-model="file" :state="Boolean(file)" @Input="onFileDrop"
        accept="image/*;capture=camera"
        placeholder="Choose a file or drop it here..." 
        drop-placeholder="Drop file here...">
      </b-form-file>
      <br>
      <h4>Or upload from device</h4>
      <b-form-file v-model="file" :state="Boolean(file)" @Input="onFileDrop"
        placeholder="Choose a file or drop it here..." 
        drop-placeholder="Drop file here...">
      </b-form-file>
    </div>

    <img :src="imageBase64" class="item-image" />

    <b-button v-if="file" @click="scanFile()">Scan</b-button>

    <b-spinner v-if="loading" variant="primary"></b-spinner>

    <div>{{ aiResponse }}</div>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      file: null,
      imageBase64: '',
      aiResponse: '',
      loading: false,
      newItem: null
    }
  },
  methods: {
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
    scanFile() {
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
            'Authorization': 'Bearer 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'
          },
          body: JSON.stringify(jsonData)
        }).then((response) => response.json())
        .then((response) => {
          this.aiResponse = response.choices[0].message.content
          this.newItem = this.createNewItem(this.aiResponse)
          this.$refs['bv-modal'].show()
          console.log('new item', this.newItem)
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
      fetch('http://127.0.0.1:5000/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.newItem)
      }).then(() => {
        this.$router.push('/')
      })
    }
  }
}
</script>

<style scoped>
.item-image {
  max-width: 400px;
  max-height: 400px;
}

.file-upload-area {
  border: solid 1px red;
  padding: 0.5rem;
}
</style>