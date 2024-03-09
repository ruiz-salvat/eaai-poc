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
                    
                    <div class="text-center">
                        <b-button @click="getPlan()" variant="primary" class="mt-2" pill>Save</b-button>
                    </div>
                </div>
                
                <LoadingGif :loading="loadingPlan"></LoadingGif>
            </div>
        </b-modal>

        <b-button @click="generatePlan()" variant="primary" pill>Generate plan</b-button>

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
                    <div class="day-container">{{ dayText }}</div>
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
    methods: {
        generatePlan() {
            this.selectedOption = null
            this.$refs['make-plan-modal'].show()
        },
        getPlan() {
            this.loadingPlan = true

            let jsonData = {
                "model": "gpt-4",
                "messages": [
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": `Give a diet ${this.selectedPlan} plan. Provide it in a json object with the format [{"day": {"breakfast": "value", "lunch": "value", "dinner": "value"}}].`
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
                'Authorization': 'Bearer '
              },
              body: JSON.stringify(jsonData)
            }).then((response) => response.json())
            .then((response) => {
              this.currentPlan = JSON.parse(response.choices[0].message.content)
              this.$refs['make-plan-modal'].hide()
              this.loadingPlan = false
            })
        }
    },
    computed: {
        dayText() {
            if (this.value) {
                const [year, month, day] = this.value.split('-')
                const date = new Date(year, month - 1, day)
                const dayNumber = date.getDay()

                if (this.currentPlan) {
                    let i = 0
                    for (var key in this.currentPlan) {
                        if (i === dayNumber) {
                            var value = this.currentPlan[key]
                            return value
                        }
                        i++
                    }
                }

                switch (dayNumber) {
                    case 0:
                        return `
                            Breakfast (271 calories):
                            Avocado-Egg Toast
                            A.M. Snack (84 calories):
                            1 cup blueberries
                            Lunch (350 calories):
                            Loaded Black Bean Nacho Soup
                            P.M. Snack (62 calories):
                            1 medium orange
                            Dinner (457 calories):
                            Seared Salmon with Green Peppercorn Sauce
                            1 cup steamed green beans
                        `
                        break
                    case 1:
                        return `
                            Breakfast:
                            Greek yogurt with sliced strawberries and a sprinkle of granola
                            A.M. Snack:
                            Baby carrots with hummus
                            Lunch:
                            Quinoa salad with mixed vegetables and feta cheese
                            P.M. Snack:
                            Almonds
                            Dinner:
                            Baked chicken breast with roasted sweet potatoes and broccoli
                        `
                        break
                    case 2:
                        return `
                            Breakfast:
                            Oatmeal with sliced banana and a drizzle of honey
                            A.M. Snack:
                            Cottage cheese with pineapple chunks
                            Lunch:
                            Lentil soup with whole-grain bread
                            P.M. Snack:
                            Apple slices with peanut butter
                            Dinner:
                            Veggie stir-fry with tofu and brown rice
                        `
                        break
                    case 3:
                        return `
                            Breakfast:
                            Whole-grain toast with scrambled eggs and spinach
                            A.M. Snack:
                            Mixed berries (blueberries, raspberries, and blackberries)
                            Lunch:
                            Chickpea salad with cucumber, tomatoes, and lemon-tahini dressing
                            P.M. Snack:
                            Trail mix (nuts and dried fruit)
                            Dinner:
                            Grilled shrimp with quinoa and asparagus
                        `
                        break
                    case 4:
                        return `
                            Breakfast:
                            Smoothie (spinach, banana, almond milk, and protein powder)
                            A.M. Snack:
                            Edamame
                            Lunch:
                            Turkey and avocado wrap with whole-grain tortilla
                            P.M. Snack:
                            Cottage cheese with sliced peaches
                            Dinner:
                            Baked cod with roasted Brussels sprouts
                        `
                        break
                    case 5:
                        return `
                            Breakfast:
                            Vegetarian: Avocado toast with poached eggs.
                            Vegan: Avocado toast with mashed chickpeas and cherry tomatoes.
                            Lunch:
                            Vegetarian: Grilled vegetable panini with pesto.
                            Vegan: Hummus and roasted vegetable wrap.
                            Dinner:
                            Vegetarian: Spinach and feta stuffed bell peppers.
                            Vegan: Stuffed bell peppers with quinoa and black beans.
                        `
                        break
                    case 6:
                        return `
                            Breakfast:
                            Vegetarian: Greek yogurt with sliced strawberries and a sprinkle of granola.
                            Vegan: Coconut yogurt with mixed berries and a drizzle of maple syrup.
                            Lunch:
                            Vegetarian: Caprese salad with fresh mozzarella, tomatoes, and basil.
                            Vegan: Chickpea salad with cucumber, red onion, and lemon-tahini dressing.
                            Dinner:
                            Vegetarian: Lentil curry with brown rice.
                            Vegan: Vegetable stir-fry with tofu and quinoa.
                        `
                        break
                }
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
