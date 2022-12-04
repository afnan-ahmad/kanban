<template>
  <kanban-navigation/>
  <router-view/>
  <create-update-dialog id="createUpdateDialog"/>
</template>

<script>
import KanbanNavigation from "@/components/Navigation"
import CreateUpdateDialog from "@/components/layout/dialogs/CreateUpdateDialog"

export default {
  components: {
    KanbanNavigation,
    CreateUpdateDialog
  },
  created() {
    this.$store.commit('GET_AUTH_TOKEN')
    this.$store.commit('GET_PROFILE')
  },
  mounted() {
    const modalElement = document.getElementById('createUpdateDialog')
    const modal = new window.bootstrap.Modal(modalElement)

    modalElement.addEventListener('hidden.bs.modal', () => {
      this.$store.state.createUpdateDialog.shown = false
    })

    this.$store.watch((state) => state.createUpdateDialog.shown, (shown) => {
      if (shown) {
        modal.show()
      } else {
        modal.hide()
      }
    })
  }
}
</script>