<template>
  <li class="list-group-item card p-0 my-2 shadow-sm">
    <div class="card-body">
      <div class="d-flex">
        <span class="card-title flex-grow-1 fw-bolder">{{ card.title }}</span>
        <kanban-card-menu :card="card" @toggle-card-status="toggleStatus"
                          @edit-card="editCard" @delete-card="deleteCard"
                          @move-card="moveCard"/>
      </div>
      <p v-if="card.content" class="card-text m-0 mb-3">{{ card.content }}</p>
      <span v-if="card.completed" class="badge text-bg-success">Completed</span>
      <span v-else-if="cardOverdue" class="badge text-bg-warning">
        Overdue: {{ naturalDate }}
      </span>
      <span v-else class="badge text-bg-light">Due: {{ naturalDate }}</span>
    </div>
  </li>
</template>

<script>
import KanbanCardMenu from "@/components/layout/menus/CardMenu"
import moment from "moment"

export default {
  name: 'KanbanCard',
  props: {
    card: {}
  },
  computed: {
    cardOverdue() {
      const deadline = moment(this.$props.card.deadline.toString()).endOf('day')

      return moment().startOf('day').isAfter(deadline)
    },
    naturalDate() {
      const deadline = moment(this.$props.card.deadline.toString()).endOf('day')

      const daysLeft = deadline.diff(moment().startOf('day'), 'days')

      if (daysLeft >= 7) {
        return deadline.year() === moment().year() ? deadline.format('MMM DD') : deadline.format('MM DD YYYY')
      } else if (daysLeft < 0) {
        return deadline.fromNow(true)
      }

      return deadline.calendar(null, {
        lastDay: '[Yesterday]',
        sameDay: '[Today]',
        nextDay: '[Tomorrow]',
        lastWeek: '[last] dddd',
        nextWeek: 'dddd',
        sameElse: 'L'
      })
    }
  },
  components: {
    KanbanCardMenu
  },
  methods: {
    toggleStatus() {
      this.$store.dispatch('UPDATE_CARD', {
        list_id: this.$props.card.list_id,
        id: this.$props.card.id,
        completed: !this.$props.card.completed
      })
    },
    editCard() {
      const dialog = {
        title: 'Edit card',
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
            value: this.$props.card.title,
            required: true
          },
          content: {
            type: 'textarea',
            label: 'Content',
            maxlength: 250,
            value: this.$props.card.content
          },
          deadline: {
            type: 'date',
            label: 'Deadline',
            value: moment(this.$props.card.deadline).format('YYYY-MM-DD'),
            required: true
          },
          completed: {
            type: 'boolean',
            label: 'Mark as complete',
            value: this.$props.card.completed
          }
        },
        action_text: 'Save'
      }

      for (let list of this.$store.state.list.data) {
        dialog.fields.list.options.push({
          value: list.id,
          label: list.name
        })
      }

      dialog.fields.list.value = this.$props.card.list_id

      dialog.action = async () => {
        const result = await this.$store.dispatch('UPDATE_CARD', {
          id: this.$props.card.id,
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
    moveCard() {
      const dialog = {
        title: 'Move card',
        fields: {
          list: {
            type: 'select',
            label: 'List',
            options: [],
            required: true,
          }
        },
        action_text: 'Move'
      }

      for (let list of this.$store.state.list.data) {
        if (list.id !== this.$props.card.list_id) {
          dialog.fields.list.options.push({
            value: list.id,
            label: list.name
          })
        }
      }

      dialog.action = async () => {
        const result = await this.$store.dispatch('MOVE_CARD', {
          card_id: this.$props.card.id,
          from: this.$props.card.list_id,
          to: dialog.fields.list.value
        })

        if (!result.success) {
          dialog.fields[result.reason.error_field].error = result.reason.error_message
        } else {
          this.$store.dispatch('HIDE_DIALOG')
        }
      }

      this.$store.dispatch('SHOW_DIALOG', dialog)
    },
    deleteCard() {
      this.$store.dispatch('DELETE_CARD', {
        list_id: this.$props.card.list_id,
        id: this.$props.card.id
      })
    }
  }
}
</script>
