<template>
  <div class="modal fade">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold">
            {{ dialog.title }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"/>
        </div>
        <div class="modal-body">
          <div v-if="dialog.message" class="mb-3">
            {{ dialog.message }}
          </div>
          <form id="createUpdateForm" action="#">
            <div v-for="(field, key) in dialog.fields" :key="key" class="mb-3">
              <label class="form-label" :for="key">{{ field.label }} {{ field.required ? '*' : '' }}</label>

              <div v-if="field.type === 'boolean'" class="form-check form-switch d-inline-block align-middle ms-2">
                <input type="checkbox" class="form-check-input" :id="field.name" :name="field.name"
                       :required="field.required" v-model="field.value"/>
              </div>

              <select v-else-if="field.type === 'select'" class="form-select" :id="field.name" :name="field.name"
                      :required="field.required" v-model="field.value">
                <option v-for="(option, key) in field.options" :key="key" :value="option.value">
                  {{ option.label }}
                </option>
              </select>

              <input v-else-if="field.type === 'date'" type="date"
                     :class="'form-control ' + (field.error ? 'is-invalid' : '')"
                     :id="field.name" :name="field.name" :min="field.min" :max="field.max" :required="field.required"
                     v-model="field.value"/>

              <textarea v-else-if="field.type === 'textarea'"
                        :class="'form-control ' + (field.error ? 'is-invalid' : '')"
                        :id="field.name" :name="field.name" :maxlength="field.maxlength" :required="field.required"
                        v-model="field.value"/>

              <input v-else type="text"
                     :class="'form-control ' + (field.error ? 'is-invalid' : '')"
                     :id="field.name" :name="field.name" :maxlength="field.maxlength" :required="field.required"
                     v-model="field.value"/>

              <div v-if="field.error" class="invalid-feedback">
                {{ field.error }}
              </div>
            </div>
            <div class="text-end">
              <button @click="handleAction" type="submit" class="btn btn-primary" :disabled="inProgress">
                <span v-if="inProgress" class="spinner-border spinner-border-sm"></span>
                {{ dialog.action_text }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreateUpdateDialog',
  computed: {
    dialog() {
      return this.$store.state.createUpdateDialog
    }
  },
  data() {
    return {
      inProgress: false
    }
  },
  methods: {
    async handleAction(e) {
      e.preventDefault()

      const form = document.getElementById('createUpdateForm')

      if (!form.checkValidity()) {
        form.reportValidity()
        return
      }

      this.inProgress = true

      await this.$store.state.createUpdateDialog.action()

      this.inProgress = false
    }
  }
}
</script>