<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <h1 class="mb-6 text-2xl">
                    Sign Up
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
                    Already have an account? <RouterLink :to="{ name: 'signin' }" class="underline">Click Here
                    </RouterLink>to sign in!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="SubmitForm">
                    <div>
                        <label>Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Your full name"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password1" placeholder="Your password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <div>
                        <label>Repeat Password</label><br>
                        <input type="password" v-model="form.password2" placeholder="Your password again"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign Up</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'

import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const toastStore = useToastStore()
        return { toastStore }
    },

    data() {
        return {
            form: {
                name: '',
                email: '',
                password1: '',
                password2: '',
            },
            errors: [],
        }
    },

    methods: {
        SubmitForm() {
            this.errors = []

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            if (this.form.email === '') {
                this.errors.push('Your E-mail is missing')
            }

            if (this.form.password1 === '') {
                this.errors.push('Your password is missing')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('Your passwords do not match')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The user is registered, please activate your account via the link sent to your email address.', 'bg-emerald-500')

                            this.form.name = ''
                            this.form.email = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            this.toastStore.showToast(5000, 'Something went wrong, please try again.', 'bg-red-300')

                            let data = JSON.parse(response.data.message)

                            for (const error in data) {
                                this.errors.push(data[error][0].message)
                            }
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        }
    }
}

</script>