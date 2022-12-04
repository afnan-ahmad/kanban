export default {
    state: {
        data: []
    },
    getters: {
        listCount(state) {
            return state.data.length
        }
    },
    mutations: {
        'SET_LISTS': (state, lists) => {
            state.data = lists
        },
        'PUSH_LIST': (state, list) => {
            state.data.push(list)
        },
        'UPDATE_LIST': (state, updatedList) => {
            const list = state.data.find(x => x.id === updatedList.id)
            list.name = updatedList.name
            if (updatedList.cards) {
                list.cards = updatedList.cards
            }
        },
        'MOVE_CARDS': (state, move) => {
            const fromList = state.data.find(x => x.id === move.from)
            const toList = state.data.find(x => x.id === move.to)

            toList.cards.push(...fromList.cards)
        },
        'MOVE_ONE_CARD': (state, move) => {
            const fromList = state.data.find(x => x.id === move.from)
            const toList = state.data.find(x => x.id === move.to)

            const index = fromList.cards.findIndex(x => x.id === move.card_id)
            const card = fromList.cards[index]

            card.list_id = move.to
            toList.cards.push(card)

            fromList.cards.splice(index, 1)
        },
        'REMOVE_LIST': (state, id) => {
            const index = state.data.findIndex(x => x.id === id)
            if (index > -1) {
                state.data.splice(index, 1)
            }
        },
        'PUSH_CARD': (state, card) => {
            const list = state.data.find(x => x.id === card.list_id)
            list.cards.push(card)
        },
        'UPDATE_CARD': (state, updatedCard) => {
            const list = state.data.find(x => x.id === updatedCard.list_id)
            const card = list.cards.find(x => x.id === updatedCard.id)
            for (let prop in updatedCard) {
                card[prop] = updatedCard[prop]
            }
        },
        'REMOVE_CARD': (state, card) => {
            const list = state.data.find(x => x.id === card.list_id)
            const index = list.cards.findIndex(x => x.id === card.id)
            if (index > -1) {
                list.cards.splice(index, 1)
            }
        }
    },
    actions: {
        'FETCH_LISTS': async (context) => {
            if (context.state.data.length > 0) {
                return
            }
            const res = await fetch('http://localhost:5000/api/list', {
                method: 'GET',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken
                }
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('SET_LISTS', result)
            }
        },
        'FETCH_CARDS': async (context, list) => {
            const res = await fetch('http://localhost:5000/api/list/' + list.id, {
                method: 'GET',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                }
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('UPDATE_LIST', result)

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
        'CREATE_LIST': async (context, name) => {
            const res = await fetch('http://localhost:5000/api/list', {
                method: 'POST',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name
                })
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('PUSH_LIST', result)

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
        'UPDATE_LIST': async (context, list) => {
            const res = await fetch('http://localhost:5000/api/list/' + list.id, {
                method: 'PUT',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: list.name
                })
            })

            const result = await res.json()

            if (res.ok) {
                context.commit('UPDATE_LIST', list)

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
        'DELETE_LIST': async (context, opts) => {
            let url = 'http://localhost:5000/api/list/' + opts.id
            if (opts.move_to) {
                url = url + '?move_to=' + opts.move_to
            }
            const res = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Authentication-Token': context.rootState.user.authToken,
                    'Content-Type': 'application/json'
                }
            })

            const result = await res.json()

            if (res.ok) {
                if (opts.move_to && opts.move_to > -1) {
                    context.commit('MOVE_CARDS', {
                        from: opts.id,
                        to: opts.move_to
                    })
                }
                context.commit('REMOVE_LIST', opts.id)

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