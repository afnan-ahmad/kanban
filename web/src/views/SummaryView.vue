<template>
  <kanban-actionbar/>
  <div class="d-flex flex-row flex-wrap">
    <div v-for="s in summary" :key="s.name" class="col-12 col-md-3 p-3">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <div class="d-flex mb-2">
            <span class="card-title flex-grow-1 fw-bolder">{{ s.name }}</span>
            <span class="text-end text-muted">{{ s.total }} tasks</span>
          </div>
          <div class="progress mb-2">
            <div class="progress-bar bg-success" :style="'width:' + s['completed_percent'] + '%;'"></div>
            <div class="progress-bar bg-warning" :style="'width:' + s['overdue_percent'] + '%;'"></div>
          </div>
          <p class="mb-1"><b>{{ s.completed }}</b> completed</p>
          <p class="mb-1"><b>{{ s.overdue }}</b> overdue</p>
          <p class="mt-3 text-center text-muted">Completed over the last week</p>
          <img class="img-fluid" :src="'data:image/png;base64,' + s['fig_data']"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import KanbanActionbar from "@/components/Actionbar"

export default {
  name: 'SummaryView',
  components: {
    KanbanActionbar
  },
  data() {
    return {
      summary: []
    }
  },
  async mounted() {
    const res = await fetch('http://localhost:5000/api/summary', {
      method: 'GET',
      headers: {
        'Authentication-Token': this.$store.state.user.authToken
      }
    })

    const data = await res.json()

    this.summary = data
  }
}
</script>
