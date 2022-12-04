<template>
  <div :id="id" class="d-flex flex-column col-12 col-md-3 m-3 px-2 pt-2 bg-alpha rounded list">
    <div class="d-flex align-items-center">
      <span class="flex-grow-1 px-2 fw-bolder">{{ name }}</span>
      <div class="btn-group">
        <button @click="createCard" class="btn btn-link shadow-none">
          <i class="material-icons align-middle">add_circle_outline</i>
        </button>
        <kanban-list-menu :id="id" @edit-list="editList" @delete-list="deleteList"/>
      </div>
    </div>
    <ul class="list-group px-2 pb-2">
      <kanban-card v-for="card in cards" :key="card.id" :card="card"/>
    </ul>
  </div>
</template>

<script>
import KanbanListMenu from "@/components/layout/menus/ListMenu"
import KanbanCard from "@/components/Card"

export default {
  name: 'KanbanList',
  props: {
    id: Number,
    name: String,
    cards: Array
  },
  components: {
    KanbanListMenu,
    KanbanCard
  },
  mounted() {
    this.$store.dispatch('FETCH_CARDS', {id: this.$props.id})
  },
  methods: {
    createCard() {
      const dialog = {
        title: 'Create card',
        fields: {
          list: {
            type: 'select',
            label: 'List',
            options: [],
            required: true,
          },
          title: {
            type: 'text',
            label: 'Title',
            maxlength: 25,
            required: true
          },
          content: {
            type: 'textarea',
            label: 'Content',
            maxlength: 250
          },
          deadline: {
            type: 'date',
            label: 'Deadline',
            required: true
          },
          completed: {
            type: 'boolean',
            label: 'Mark as complete'
          }
        },
        action_text: 'Create'
      }

      for (let list of this.$store.state.list.data) {
        dialog.fields.list.options.push({
          value: list.id,
          label: list.name
        })
      }

      dialog.fields.list.value = this.$props.id

      dialog.action = async () => {
        const result = await this.$store.dispatch('CREATE_CARD', {
          list_id: dialog.fields.list.value,
          title: dialog.fields.title.value,
          content: dialog.fields.content.value,
          deadline: dialog.fields.deadline.value,
          completed: dialog.fields.completed.value
        })

        if (!result.success) {
          dialog.fields[result.reason.error_field].error = result.reason.error_message
        } else {
          this.$store.dispatch('HIDE_DIALOG')
        }
      }

      this.$store.dispatch('SHOW_DIALOG', dialog)
    },
    editList() {
      const dialog = {
        title: 'Edit list',
        fields: {
          name: {
            type: 'text',
            label: 'Name',
            required: true,
            maxlength: 25,
            value: this.$props.name
          }
        },
        action_text: 'Save'
      }

      dialog.action = async () => {
        const result = await this.$store.dispatch('UPDATE_LIST', {id: this.$props.id, name: dialog.fields.name.value})

        if (!result.success) {
          dialog.fields[result.reason.error_field].error = result.reason.error_message
        } else {
          this.$store.dispatch('HIDE_DIALOG')
        }
      }

      this.$store.dispatch('SHOW_DIALOG', dialog)
    },
    deleteList() {
      if (this.$props.cards.length > 0) {
        const dialog = {
          title: 'Delete ' + this.$props.name,
          message: 'This list has cards. Please select another list if you want to keep them.',
          fields: {
            list: {
              type: 'select',
              label: 'Move To',
              required: true,
              options: [
                {
                  label: 'None, delete the cards',
                  value: -1
                }
              ],
              value: -1
            }
          },
          action_text: 'Confirm'
        }

        for (let list of this.$store.state.list.data) {
          if (list.id !== this.$props.id) {
            dialog.fields.list.options.push({
              value: list.id,
              label: list.name
            })
          }
        }

        dialog.action = async () => {
          const result = await this.$store.dispatch('DELETE_LIST', {
            id: this.$props.id,
            move_to: dialog.fields.list.value
          })

          if (!result.success) {
            dialog.fields[result.reason.error_field].error = result.reason.error_message
          } else {
            this.$store.dispatch('HIDE_DIALOG')
          }
        }

        this.$store.dispatch('SHOW_DIALOG', dialog)
      } else {
        this.$store.dispatch('DELETE_LIST', {
          id: this.$props.id
        })
      }
    }
  }
}
</script>