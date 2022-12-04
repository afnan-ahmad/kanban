<template>
  <kanban-actionbar/>
  <kanban-board/>
</template>

<script>
import KanbanActionbar from "@/components/Actionbar"
import KanbanBoard from "@/components/Board.vue"

export default {
  name: 'BoardView',
  components: {
    KanbanActionbar,
    KanbanBoard
  }
}
</script>
