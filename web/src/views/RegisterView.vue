<template>
  <div class="d-flex align-items-center justify-content-center h-100">
    <div class="col-11 col-md-3 bg-body rounded shadow-sm p-4 mb-5">
      <h3 class="fw-bold">Register</h3>
      <p class="pb-1 text-muted">Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
      <form class="mt-3" id="register_user_form" action="#">
        <div class="mb-3">
          <label class="form-label" for="name">Name</label>
          <input class="form-control" type="text" id="name" name="name" required/>
        </div>
        <div class="mb-3">
          <label class="form-label" for="email">Email</label>
          <input class="form-control" type="email" id="email" name="email" required/>
        </div>
        <div class="mb-3">
          <label class="form-label" for="password">Password</label>
          <input class="form-control" type="password" id="password" name="password" required/>
        </div>
        <div class="mb-3">
          <label class="form-label" for="password_confirm">Confirm Password</label>
          <input class="form-control" type="password" id="password_confirm" name="password_confirm" required/>
        </div>
        <div class="text-end">
          <button type="submit" class="btn btn-primary">Register</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterView'
}
</script>
