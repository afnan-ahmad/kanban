<template>
  <div class="dropdown">
    <button class="btn btn-link shadow-none" data-bs-toggle="dropdown">
      <i class="material-icons align-middle">more_vert</i>
    </button>
    <ul class="dropdown-menu dropdown-menu-end position-fixed border-0 shadow">
      <li>
        <button class="dropdown-item" @click="$emit('editList')">
          <i class="material-icons align-middle pe-2">drive_file_rename_outline</i>
          Edit
        </button>
      </li>
      <li>
        <button class="dropdown-item" @click="$emit('deleteList')">
          <i class="material-icons align-middle pe-2">delete_outline</i>
          Delete
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'KanbanListMenu',
  props: {
    id: Number
  }
}
</script>