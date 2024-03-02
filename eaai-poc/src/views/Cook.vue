<template>
  <b-container>
    <b-row>
      <b-list-group v-for="item in items">
        <b-list-group-item @Click="itemClick(item)" :active="selectedItems.map((x) => x.id).includes(item.id)">
          {{ item.name }}
        </b-list-group-item>
      </b-list-group>
    </b-row>
    <b-button @click="generateRecipe()">Generate recipe</b-button>
    <hr>
    <b-spinner v-if="loading" variant="primary"></b-spinner>
    <div>{{ aiResponse }}</div>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      items: [],
      selectedItems: [],
      aiResponse: '',
      loading: false
    }
  },
  created() {
    fetch('http://127.0.0.1:5000/items')
    .then((response) => response.json())
    .then((response) => {
      this.items = response.items
      console.log('items', response)
    })
  },
  methods: {
    generateRecipe() {
      console.log('selectedItems', this.selectedItems)
      this.loading = true

      const jsonData = {
        "model": "gpt-4",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": `Give a recipe using  ${this.selectedItems}`
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
        console.log('response...', response)

        this.aiResponse = response.choices[0].message.content
        this.loading = false
      })
    },
    itemClick(item) {
      if (this.selectedItems.map((x) => x.id).includes(item.id))
        this.selectedItems = this.selectedItems.filter((x) => x.id !== item.id)
      else
        this.selectedItems.push(item)
    }
  }
}
</script>
