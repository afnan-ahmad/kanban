<template>
  <div class="d-flex align-items-center justify-content-center h-100">
    <div class="col-11 col-md-3 bg-body rounded shadow-sm p-4 mb-5">
      <h3 class="fw-bold mb-3">Login</h3>
      <ul v-if="errors">
        <li v-for="error in errors" :key="error">{{ error[0] }}</li>
      </ul>
      <form class="mt-3" id="login_user_form" action="#">
        <div class="mb-3">
          <label class="form-label" for="email">Email</label>
          <input v-model="email" class="form-control" type="email" id="email" name="email"
                 :disabled="loggingIn" required/>
        </div>
        <div class="mb-3">
          <label class="form-label" for="password">Password</label>
          <input v-model="password" class="form-control" type="password" id="password" name="password"
                 :disabled="loggingIn" required/>
        </div>
        <div class="text-end">
          <button type="submit" @click="login" class="btn btn-primary" :disabled="loggingIn">
            <span v-if="loggingIn" class="spinner-border spinner-border-sm"></span>
            Login
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      email: 'afnan@example.com',
      password: 'Test@123',
      errors: [],
      loggingIn: false
    }
  },
  methods: {
    async login(e) {
      e.preventDefault()

      this.loggingIn = true

      const form = document.getElementById('login_user_form')
      if (!form.checkValidity()) {
        form.reportValidity()
        return
      }

      const result = await this.$store.dispatch('LOGIN', {
        email: this.email,
        password: this.password
      })

      if (result.success) {
        // noinspection JSUnresolvedFunction
        this.$router.replace('/')

        this.$store.dispatch('FETCH_PROFILE')

      } else {
        this.errors = result.reason
      }

      this.loggingIn = false
    }
  }
}
</script>
