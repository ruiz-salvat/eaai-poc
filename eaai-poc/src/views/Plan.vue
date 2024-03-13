<script setup>
import LoadingGif from '../components/LoadingGif.vue'

import { inject } from 'vue'
const { api_key, updateKey } = inject('api_key')
</script>

<template>
    <b-container class="mt-2 mb-2">
        {{ updateKey() }}

        <b-modal ref="make-plan-modal" title="Make a diet plan" hide-footer>
            <div class="d-block">
                <div v-if="!loadingPlan">
                    <b-form-group
                        label="Type:"
                        label-for="input-1">
                        <b-form-select
                            id="input-1"
                            v-model="selectedPlan"
                            :options="planOptions"
                        ></b-form-select>
                    </b-form-group>

                    <b-form-textarea
                        id="textarea"
                        v-model="infoText"
                        placeholder="Write additional info..."
                        rows="3"
                        max-rows="6"
                        class="mt-2"
                    ></b-form-textarea>
                    
                    <div class="text-center">
                        <b-button @click="getPlan(api_key)" variant="primary" class="mt-2" pill>Save</b-button>
                    </div>
                </div>
                
                <LoadingGif :loading="loadingPlan"></LoadingGif>
            </div>
        </b-modal>

        <b-button @click="generatePlan(api_key)" variant="primary" pill>Generate plan</b-button>

        <b-row class="mt-2">
            <b-calendar 
                v-model="value" 
                @context="onContext" 
                block 
                locale="en-US">
            </b-calendar>
        </b-row>

        <b-row class="mt-2">
            <b-overlay :show="loading" rounded="sm">
                <b-card :title="formatedDate" :aria-hidden="loading ? 'true' : null">
                    <div class="day-container" v-html="dayText"></div>
                </b-card>
            </b-overlay>
        </b-row>
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
            loading: false,
            loadingPlan: false,
            value: null,
            selectedPlan: null,
            infoText: '',
            planOptions: [
                { value: null, text: 'Please select an option' },
                { value: 'mediterranean', text: 'Mediterranean' },
                { value: 'low_carb', text: 'Low-Carb' },
                { value: 'flexitarian', text: 'Flexitarian' },
                { value: 'vegan', text: 'Vegan' },
                { value: 'intermittent_fasting', text: 'Intermittent Fasting'},
                { value: 'zone', text: 'Stabilize Sugar Levels'}
            ],
            currentPlan: null
        }
    },
    created() {
        let jsonPlan = "[\n  {\n    \"day1\": {\n      \"breakfast\": \"Scrambled eggs with tomatoes and avocado\",\n      \"lunch\": \"Grilled chicken salad with olive oil dressing\",\n      \"dinner\": \"Steak with grilled vegetables\"\n    }\n  },\n  {\n    \"day2\": {\n      \"breakfast\": \"Greek yogurt with a handful of almonds\",\n      \"lunch\": \"Shrimp stir-fry with broccoli and snow peas\",\n      \"dinner\": \"Baked salmon with lemon and asparagus\"\n    }\n  },\n  {\n    \"day3\": {\n      \"breakfast\": \"Protein smoothie with spinach, almond milk, protein powder\",\n      \"lunch\": \"Chicken Caesar salad without croutons\",\n      \"dinner\": \"Pork tenderloin with green beans\"\n    }\n  },\n  {\n    \"day4\": {\n      \"breakfast\": \"Omelette with spinach, mushrooms, and feta cheese\",\n      \"lunch\": \"Beef salad with cucumber, peppers, and romaine lettuce\",\n      \"dinner\": \"Baked cod with zucchini noodles\"\n    }\n  },\n  {\n    \"day5\": {\n      \"breakfast\": \"Avocado and turkey bacon wrap\",\n      \"lunch\": \"Chicken and vegetable stir-fry\",\n      \"dinner\": \"Stuffed bell peppers with ground turkey and cheese\"\n    }\n  },\n  {\n    \"day6\": {\n      \"breakfast\": \"Protein pancake with peanut butter spread\",\n      \"lunch\": \"Cobb Salad with hard-boiled eggs, chicken, and avocado\",\n      \"dinner\": \"Grilled shrimp skewers with a side salad\"\n    }\n  },\n  {\n    \"day7\": {\n      \"breakfast\": \"Chia seed pudding made with coconut milk\",\n      \"lunch\": \"Tuna salad wrapped in lettuce\",\n      \"dinner\": \"Grilled chicken with side of grilled squash and zucchini\"\n    }\n  }\n]"
        this.currentPlan = JSON.parse(jsonPlan)
    },
    methods: {
        generatePlan() {
            this.selectedOption = null
            this.$refs['make-plan-modal'].show()
        },
        getPlan(api_key) {
            this.loadingPlan = true

            let jsonData = {
                "model": "gpt-4",
                "messages": [
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": `Give a diet ${this.selectedPlan} plan ${this.infoText}. Provide it in a json object with the format [{"day": {"breakfast": "value", "lunch": "value", "dinner": "value"}}].`
                        }
                    ]
                    }
                ],
                // "max_tokens": 300
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
              this.currentPlan = JSON.parse(response.choices[0].message.content)
              this.$refs['make-plan-modal'].hide()
              this.loadingPlan = false
              this.selectedPlan = null
              this.infoText = ''
            })
        }
    },
    computed: {
        dayText() {
            if (this.value) {
                const [year, month, day] = this.value.split('-')
                const date = new Date(year, month - 1, day)
                const dayNumber = date.getDay()

                let text = ''
                if (this.currentPlan) {
                    let i = 0
                    for (var key in this.currentPlan) {
                        if (i === dayNumber) {
                            for (var key2 in this.currentPlan[key]) {

                                text = `${text}<i>${key2}</i><hr>`
                                for (var key3 in this.currentPlan[key][key2]) {
                                    text = `${text}<h4>${key3}</h4><p>${JSON.stringify(this.currentPlan[key][key2][key3])}<p>`
                                }
                            }
                        }
                        i++
                    }
                }
                return text
            }
            return 'Select date from calendar'
        },
        formatedDate() {
            if (!this.value)
                return null
            const date = new Date(this.value)
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
.day-container {
  max-height: 350px;
  overflow-y: auto;
}
</style>
