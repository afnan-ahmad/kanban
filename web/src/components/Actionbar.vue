<template>
  <div class="d-flex flex-row align-items-center mx-3 mt-1">
    <div class="btn-group btn-group-sm me-3">
      <button @click="createList" class="btn btn-primary pe-3">
        <i class="material-icons align-middle">add</i>
        <span class="align-middle fw-bolder">Create list</span>
      </button>
    </div>
    <div class="btn-group btn-group-sm ms-auto">
      <router-link to="/" class="btn btn-outline-primary">Board</router-link>
      <router-link to="/summary" class="btn btn-outline-primary">Summary</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KanbanActionbar',
  methods: {
    createList() {
      const dialog = {
        title: 'Create list',
        fields: {
          name: {
            type: 'text',
            label: 'Name',
            required: true,
            maxlength: 25,
            value: ''
          }
        },
        action_text: 'Create'
      }

      dialog.action = async () => {
        const result = await this.$store.dispatch('CREATE_LIST', dialog.fields.name.value)

        if (!result.success) {
          dialog.fields[result.reason.error_field].error = result.reason.error_message
        } else {
          this.$store.dispatch('HIDE_DIALOG')
        }
      }

      this.$store.dispatch('SHOW_DIALOG', dialog)
    }
  }
}
</script>