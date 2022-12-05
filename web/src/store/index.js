import {createStore} from "vuex"

import user from "./user"
import list from "./list"
import card from "./card"

export default createStore({
    state: {
        createUpdateDialog: {
            title: '',
            message: '',
            fields: [],
            action_text: '',
            action: async () => false,
            shown: false
        }
    },
    getters: {},
    mutations: {},
    actions: {
        'SHOW_DIALOG': function (context, dialog) {
            context.state.createUpdateDialog.title = dialog.title
            context.state.createUpdateDialog.message = dialog.message
            context.state.createUpdateDialog.fields = dialog.fields
            context.state.createUpdateDialog.action_text = dialog.action_text
            context.state.createUpdateDialog.action = dialog.action
            context.state.createUpdateDialog.shown = true
        },
        'HIDE_DIALOG': function (context) {
            context.state.createUpdateDialog.shown = false
        },
        'REQUEST_JOB': async (context, job) => {
            try {
                const res = await fetch('http://localhost:5000/api/jobs', {
                    method: 'POST',
                    headers: {
                        'Authentication-Token': context.rootState.user.authToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(job)
                })

                const result = await res.json()

                if (res.ok) {
                    return {
                        success: true
                    }
                } else {
                    return {
                        success: false,
                        reason: result
                    }
                }
            } catch {
                return {
                    success: false
                }
            }
        },
    },
    modules: {
        user, list, card
    }
})
