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
        }
    },
    modules: {
        user, list, card
    }
})
