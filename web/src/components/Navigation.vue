<template>
  <nav class="navbar navbar-expand navbar-light">
    <div class="container-fluid px-3">
      <a href="/" class="navbar-brand align-middle fw-bolder">Kanban</a>
      <ul v-if="$store.getters.isLoggedIn" class="navbar-nav">
        <li class="nav-item dropdown">
          <button class="btn btn-link nav-link shadow-none dropdown-toggle" data-bs-toggle="dropdown">
            {{ $store.state.user.profile.displayName }}
          </button>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow">
            <li>
              <button @click="exportLists" class="dropdown-item">Export</button>
            </li>
            <li>
              <button @click="logout" class="dropdown-item">Logout</button>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'KanbanNavigation',
  methods: {
    exportLists() {
      const dialog = {
        title: 'Export lists',
        message: 'This will export all list related data into a CSV file. You will get an email with the file attached once it is ready.',
        action_text: 'Export'
      }

      dialog.action = async () => {
        await this.$store.dispatch('REQUEST_JOB', {job_name: 'export_lists'})
        this.$store.dispatch('HIDE_DIALOG')
      }

      this.$store.dispatch('SHOW_DIALOG', dialog)
    },
    async logout() {
      await this.$store.dispatch('LOGOUT')

      // noinspection JSUnresolvedFunction
      this.$router.replace('/login')
    }
  }
}
</script>