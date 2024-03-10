<script setup>
import LoadingGif from '../components/LoadingGif.vue'
import ConfirmationModal from '../components/ConfirmationModal.vue'

import { inject } from 'vue'
const { api_key, updateKey } = inject('api_key')
</script>

<template>
  <b-container class="mt-2 mb-2">
    {{ updateKey() }}

    <b-modal ref="add-recipe-modal" title="Add a new recipe" hide-footer>
      <div class="d-block">
          <b-form-group
            label="Name:"
            label-for="input-1">
            <b-form-input
              id="input-1"
              v-model="newRecipe.name"
              type="text"
              placeholder="Spaghuetti bolognese"
              required
            ></b-form-input>
          </b-form-group>
          
          <div class="text-center">
            <b-button @click="saveRecipe()" variant="primary" class="mt-2" pill>Save</b-button>
          </div>
      </div>
    </b-modal>

    <ConfirmationModal 
      ref="delete-modal" 
      @confirmed="onDeleteConfirmed"
      title="Delete recipe" 
      message="Are you sure you want to delete this recipe?"/>

    <b-alert
      v-model="showDeleteRecipeAlert"
      class="position-fixed fixed-top m-0 rounded-0"
      style="z-index: 2000;"
      variant="success"
      dismissible>
      Recipe deleted successfully!
    </b-alert>

    <div v-if="!loading">
      <div v-if="display === 'picker'">
        <div class="option-container">
          <div class="option" 
            :class="'list' === selectedMode ? 'active-option' : ''" 
            @click="selectedMode = 'list'">
            <b-icon icon="inboxes"/>
          </div>
          <div class="option" 
            :class="'scan' === selectedMode ? 'active-option' : ''" 
            @click="selectedMode = 'scan'">
            <b-icon icon="camera"/>
          </div>
          <div class="option" 
            :class="'recipe-list' === selectedMode ? 'active-option' : ''" 
            @click="selectedMode = 'recipe-list'">
            <b-icon icon="list"/>
          </div>
          <div class="option" 
            v-if="aiResponse.length"
            @click="display = 'recipe'">
            <b-icon icon="chevron-compact-right"/>
          </div>
        </div>

        <div v-if="selectedMode == 'list'">
          <div class="list-container">
            <b-list-group v-for="item in items">
              <b-list-group-item @Click="itemClick(item)" :active="selectedItems.map((x) => x.id).includes(item.id)">
                {{ item.name }}
              </b-list-group-item>
            </b-list-group>
          </div>
          <b-button @click="generateRecipe(api_key)" variant="primary" class="mt-2" pill>Generate recipe</b-button>
        </div>

        <div v-if="selectedMode == 'scan'">
          <div class="image-area">
            <img v-if="file" :src="imageBase64" class="item-image" />
            <b-icon v-if="!file" icon="image" font-scale="7.5"></b-icon>
          </div>
          <b-form-file v-model="file" 
            :state="Boolean(file)" 
            @Input="onFileDrop"
            class="mt-2"
            placeholder="" 
            drop-placeholder="">
          </b-form-file>
          <b-button @click="generateRecipe(api_key)" variant="primary" class="mt-2" pill>Generate recipe</b-button>
        </div>

        <div v-if="selectedMode == 'recipe-list'">
          <div class="list-container">
            <b-list-group v-for="recipe in recipies">
              <b-list-group-item>
                <b-row>
                  <b-col @Click="recipeClick(recipe)" cols="10">{{ recipe.name }}</b-col>
                  <b-col class="text-center">
                    <b-icon 
                      @click="deleteRecipe(recipe.id)"
                      icon="trash-fill" 
                      variant="danger" />
                  </b-col>
                </b-row>
              </b-list-group-item>
            </b-list-group>
          </div>
        </div>
      </div>

      <div v-if="display === 'recipe'">
        <div class="option-container">
          <div class="option" 
            @click="display = 'picker'">
            <b-icon icon="chevron-compact-left"/>
          </div>
        </div>

        <b-overlay :show="loadingChat" rounded="sm">
          <b-card title="Your recipe" :aria-hidden="loadingChat ? 'true' : null">
            <div class="recipe-container">{{ aiResponse }}</div>
            <b-button @click="save()" variant="primary" class="mt-2" pill>
              <b-icon icon="archive-fill"/>
              Save
            </b-button>
          </b-card>
        </b-overlay>

        <b-form-textarea
          id="textarea"
          v-model="feedbackText"
          placeholder="Send feedback to improve the recipe"
          rows="3"
          max-rows="6"
          class="mt-2"
        ></b-form-textarea>

        <b-button @click="sendFeedback(api_key)" variant="primary" class="mt-2" pill>
          <b-icon icon="shift-fill"/>
          Send
        </b-button>
      </div>
    </div>
    
    <LoadingGif :loading="loading"></LoadingGif>
  </b-container>
</template>

<script>
export default {
  props: {
      api_key: {
          type: String,
          default: () => ''
      }
  },
  data() {
    return {
      items: [],
      selectedItems: [],
      recipies: [],
      aiResponse: '',
      loading: false,
      selectedMode: 'list',
      display: 'picker',
      file: null,
      imageBase64: null,
      loadingChat: false,
      feedbackText: '',
      newRecipe: {
        name: null,
        text: null
      },
      showDeleteRecipeAlert: false
    }
  },
  created() {
    this.getItems()
    this.getRecipes()
  },
  methods: {
    getItems() {
      fetch(`${import.meta.env.VITE_API_URL}items`)
      .then((response) => response.json())
      .then((response) => {
        this.items = response.items
      })
    },
    getRecipes() {
      fetch(`${import.meta.env.VITE_API_URL}recipies`)
      .then((response) => response.json())
      .then((response) => {
        this.recipies = response
      })
    },
    generateRecipe(api_key) {
      this.loading = true
      let jsonData

      if (this.selectedMode === 'list') {
        jsonData = {
          "model": "gpt-4",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": `Give a recipe using  ${this.selectedItems.map((x => x.name))}`
                }
              ]
            }
          ],
          "max_tokens": 300
        }

        this.getAiResponse(jsonData, api_key)
      } else if (this.selectedMode === 'scan') {
        this.getBase64(this.file).then(base64 => {
          this.imageBase64 = base64

          jsonData = {
            "model": "gpt-4-vision-preview",
            "messages": [
              {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": "Make a list of the groceries that appear in the image"
                  },
                  {
                    "type": "text",
                    "text": "Make a recipe using the groceries that appear in the image"
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

          this.getAiResponse(jsonData, api_key)
        })
      }
    },
    sendFeedback(api_key) {
      this.loadingChat = true

      const jsonData = {
          "model": "gpt-4",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": `Improve de recipe by ${this.feedbackText}`
                },
                {
                  "type": "text",
                  "text": this.aiResponse
                }
              ]
            }
          ],
          "max_tokens": 300
        }

        this.getAiResponse(jsonData, api_key)
    },
    getAiResponse(jsonData, api_key) {
      fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${api_key}`
        },
        body: JSON.stringify(jsonData)
      }).then((response) => response.json())
      .then((response) => {
        console.log('response...', response)

        this.aiResponse = response.choices[0].message.content
        this.display = 'recipe'
        this.loading = false
        this.loadingChat = false
      })

      // this.aiResponse = 'blah blah blah ...'
      // this.display = 'recipe'
      // this.loading = false
      // this.loadingChat = false
    },
    itemClick(item) {
      if (this.selectedItems.map((x) => x.id).includes(item.id))
        this.selectedItems = this.selectedItems.filter((x) => x.id !== item.id)
      else
        this.selectedItems.push(item)
    },
    recipeClick(recipe) {
      this.aiResponse = recipe.text
      this.display = 'recipe'
    },
    save() {
      this.newRecipe.text = this.aiResponse
      this.$refs['add-recipe-modal'].show()
    },
    saveRecipe() {
      fetch(`${import.meta.env.VITE_API_URL}recipies`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.newRecipe)
      }).then((response) => {
        console.log('res', response)
        this.newRecipe = {name: null, text: null}
        this.$refs['add-recipe-modal'].hide()
        this.getRecipes()
      }).catch(() => {this.newRecipe = {name: null, text: null}})
    },
    deleteRecipe(recipeId) {
      this.$refs['delete-modal'].show(recipeId)
    },
    onDeleteConfirmed(id) {
      fetch(`${import.meta.env.VITE_API_URL}recipe/${id}`, {
        method: 'DELETE'
      }).then(() => {
        this.showDeleteRecipeAlert = true
        setTimeout(() => {this.showDeleteRecipeAlert = false}, 4000)
        this.getRecipes()
      }).catch((err) => {console.log(err)})
    },
    onFileDrop(file) {
      this.getBase64(file).then(base64 => {
        this.imageBase64 = base64
      })
    },
    getBase64(file) { // TODO reuse
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = error => reject(error)
      })
    },
  }
}
</script>

<style scoped>
.option-container {
  display: flex;
  flex-direction: row;
  margin-bottom: 0.5rem;
}

.option {
  border: solid 1px #0d6efd;
  color: #0d6efd;
  margin-right: 0.5rem;
  border-radius: 0.5rem;
  padding: 0.25rem;
}

.active-option {
  background-color: #0d6efd;
  color: #ffffff;
}

option:hover {
  cursor: pointer;
}

.item-image {
  max-width: 200px;
  max-height: 200px;
}

.image-area {
  border: solid 1px #797979;
  height: 200px;
  max-width: 200px;
  max-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.list-container {
  max-height: 200px;
  overflow-y: auto;
}

.recipe-container {
  max-height: 350px;
  overflow-y: auto;
}
</style>