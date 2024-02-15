import { defineStore } from "pinia";
import axios from 'axios';

export const useUserStore = defineStore({
    id: 'user',

    state: () => ({
        user: {
            id: null,
            name: null,
            email: null,
            avatar: null,
            access: null,
            refresh: null,
            isAuthenticated: false,
        }
    }),

    actions: {
        initStore() {
            if (localStorage.getItem('user.access')) {
                this.user.id = localStorage.getItem('user.id')
                this.user.name = localStorage.getItem('user.name')
                this.user.email = localStorage.getItem('user.email')
                this.user.avatar = localStorage.getItem('user.avatar')
                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.isAuthenticated = true

                this.refreshToken()

                console.log("Initialized User: ", this.user)
            }
        },

        setToken(data) {
            console.log("Set Token: ", data)

            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)
        },

        removeToken() {
            console.log("Remove Token.")

            this.user.id = null
            this.user.name = null
            this.user.email = null
            this.user.avatar = null
            this.user.access = null
            this.user.refresh = null
            this.user.isAuthenticated = false
            
            localStorage.setItem('user.id', '')
            localStorage.setItem('user.name', '')
            localStorage.setItem('user.email', '')
            localStorage.setItem('user.avatar', '')
            localStorage.setItem('user.access', '')
            localStorage.setItem('user.refresh', '')
        },

        setUserInfo(data) {
            console.log("Set User Info: ", data)

            this.user.id = data.id
            this.user.name = data.name
            this.user.email = data.email
            this.user.avatar = data.avatar

            localStorage.setItem('user.id', data.id)
            localStorage.setItem('user.name', data.name)
            localStorage.setItem('user.email', data.email)
            localStorage.setItem('user.avatar', data.avatar)
        },

        refreshToken() {
            axios.post('/api/refresh/', {
                refresh: this.user.refresh
            })
                .then(response => {
                    this.user.access = response.data.access
                    localStorage.setItem('user.access', response.data.access)
                    axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                })

                .catch(error => {
                    console.log(error)
                    this.removeToken()
                })
        },
    }
})