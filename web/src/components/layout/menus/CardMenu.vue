<template>
  <div class="dropdown">
    <button class="btn btn-link p-0 shadow-none" data-bs-toggle="dropdown">
      <i class="material-icons align-middle">more_horiz</i>
    </button>
    <ul class="dropdown-menu dropdown-menu-end position-fixed border-0 shadow">
      <li>
        <button class="dropdown-item" @click="$emit('toggleCardStatus')">
          <span v-if="!card.completed">
            <i class="material-icons align-middle pe-2">done</i>
            Mark as Done
          </span>
          <span v-else>
            <i class="material-icons align-middle pe-2">history</i>
            Mark as Due
          </span>
        </button>
      </li>
      <li>
        <button class="dropdown-item" @click="$emit('editCard')">
          <i class="material-icons align-middle pe-2">drive_file_rename_outline</i>
          Edit
        </button>
      </li>
      <li v-if="$store.getters.listCount > 1">
        <button class="dropdown-item" @click="$emit('moveCard')">
          <i class="material-icons align-middle pe-2">swap_horiz</i>
          Move
        </button>
      </li>
      <li>
        <button class="dropdown-item" @click="$emit('deleteCard')">
          <i class="material-icons align-middle pe-2">delete_outline</i>
          Delete
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'KanbanCardMenu',
  props: {
    card: Object
  }
}
</script>