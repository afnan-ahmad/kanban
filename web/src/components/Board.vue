<template>
  <div class="d-flex flex-row overflow-auto h-100 px-3 px-md-0 board">
    <kanban-list v-for="list in $store.state.list.data" :key="list.id" :id="list.id" :name="list.name"
                 :cards="list.cards"/>
  </div>
</template>

<script>
import KanbanList from "@/components/List"

export default {
  name: 'KanbanBoard',
  components: {
    KanbanList
  },
  created() {
    this.$store.dispatch('FETCH_LISTS')
  }
}
</script>