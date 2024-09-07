<template>
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
</template>

<script>
export default {

}
</script>

<style scoped>

</style>