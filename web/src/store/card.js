export default {
    state: {},
    getters: {},
    mutations: {},
    actions: {
        'CREATE_CARD': async (context, card) => {
            const res = await fetch('http://localhost:5000/api/card', {
                method: 'POST',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(card)
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('PUSH_CARD', result)

                return {
                    success: true
                }
            } else {
                return {
                    success: false,
                    reason: result
                }
            }
        },
        'UPDATE_CARD': async (context, card) => {
            const res = await fetch('http://localhost:5000/api/card/' + card.id, {
                method: 'PUT',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(card)
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('UPDATE_CARD', card)

                return {
                    success: true
                }
            } else {
                return {
                    success: false,
                    reason: result
                }
            }
        },
        'MOVE_CARD': async (context, move) => {
            const res = await fetch('http://localhost:5000/api/card/' + move.card_id, {
                method: 'PUT',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    list_id: move.to
                })
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('MOVE_ONE_CARD', move)

                return {
                    success: true
                }
            } else {
                return {
                    success: false,
                    reason: result
                }
            }
        },
        'DELETE_CARD': async (context, card) => {
            const res = await fetch('http://localhost:5000/api/card/' + card.id, {
                method: 'DELETE',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                }
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('REMOVE_CARD', card)

                return {
                    success: true
                }
            } else {
                return {
                    success: false,
                    reason: result
                }
            }
        }
    }
}