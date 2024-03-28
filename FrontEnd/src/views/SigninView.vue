<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <h1 class="mb-6 text-2xl">
                    Sign In
                </h1>

                <p class="mb-6 text-grey-500">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                    et
                    dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                    aliquip
                    ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum
                    dolore eu
                    fugiat nulla pariatur.
                </p>

                <p class="font-bold">
                    Don't have an account? <RouterLink :to="{ name: 'signup' }" class="underline">Click Here
                    </RouterLink>
                    to sign up!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="SubmitForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password" placeholder="Your password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign In</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'

import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: [],
        }
    },

    methods: {
        async SubmitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your E-mail is missing')
            }

            if (this.form.password === '') {
                this.errors.push('Your password is missing')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/signin/', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data)
                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                    })
                    .catch(error => {
                        console.log(error)
                        this.errors.push("The email or password is incorrect, or the user is not activated.")
                    })

                axios
                    .get('/api/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)
                        this.$router.push('/feed')
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        }
    }
}

</script>