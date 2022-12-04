const KEY_AUTH_TOKEN = 'kanban_auth_token'
const KEY_PROFILE = 'kanban_profile'

export default {
    state: {
        authToken: '',
        profile: {
            displayName: ''
        }
    },
    getters: {
        isLoggedIn: state => !!state.authToken
    },
    mutations: {
        'SET_AUTH_TOKEN': (state, token) => {
            state.authToken = token
            sessionStorage.setItem(KEY_AUTH_TOKEN, token)
        },
        'GET_AUTH_TOKEN': (state) => {
            const token = sessionStorage.getItem(KEY_AUTH_TOKEN)
            if (token) {
                state.authToken = token
            }
        },
        'SET_PROFILE': (state, profile) => {
            state.profile = profile
            sessionStorage.setItem(KEY_PROFILE, JSON.stringify(profile))
        },
        'GET_PROFILE': (state) => {
            const profile = sessionStorage.getItem(KEY_PROFILE)
            if (profile) {
                state.profile = JSON.parse(profile)
            }
        },
        'CLEAR_AUTH_TOKEN': (state) => {
            state.authToken = ''
            state.profile = {}
            sessionStorage.clear()
        }
    },
    actions: {
        'LOGIN': async (context, credentials) => {
            const res = await fetch('http://localhost:5000/login?include_auth_token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(credentials)
            })

            const data = await res.json()

            if (res.ok) {
                context.commit('SET_AUTH_TOKEN', data.response.user.authentication_token)

                return {
                    success: true
                }
            }

            return {
                success: false,
                reason: data.response.errors
            }
        },
        'FETCH_PROFILE': async (context) => {
            if (!context.getters.isLoggedIn) {
                return false
            }

            const res = await fetch('http://localhost:5000/api/user', {
                method: 'GET',
                headers: {
                    'Authentication-Token': context.state.authToken
                }
            })

            if (res.ok) {
                const profile = await res.json()
                context.commit('SET_PROFILE', profile)
                return true
            }

            return false
        },
        'LOGOUT': async (context) => {
            if (!context.getters.isLoggedIn) {
                return false
            }

            context.commit('CLEAR_AUTH_TOKEN')
            context.commit('SET_LISTS', [])
            return true
        }
    }
}