<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <h1 class="mb-6 text-2xl"> Edit Profile </h1>

                <p class="mb-6 text-grey-500">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                    dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                    ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                    fugiat nulla pariatur.
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
                        <label>Avatar</label><br>
                        <input type="file" ref="file">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save Changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()
        return { toastStore, userStore }
    },

    data() {
        return {
            form: {
                name: this.userStore.user.name,
                email: this.userStore.user.email,
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

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)
                formData.append('avatar', this.$refs.file.files[0])

                axios
                    .post('/api/editprofile/', formData, {
                        'headers': {
                            'Content-Type': 'multipart/form-data',
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'Information updated', 'bg-emerald-500')

                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                            })

                            this.$router.back()

                        } else {
                            this.toastStore.showToast(5000, response.data.message, 'bg-red-300')
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