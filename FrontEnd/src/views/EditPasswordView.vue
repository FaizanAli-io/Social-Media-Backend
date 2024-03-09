<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <h1 class="mb-6 text-2xl"> Edit Password </h1>

                <p class="mb-6 text-grey-500">
                    Here you can change your password.
                </p>

                <RouterLink to="/profile/edit" class="underline">Back to Edit Profile</RouterLink>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-grey-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="SubmitForm">
                    <div>
                        <label>Old Password</label><br>
                        <input type="password" v-model="form.old_password" placeholder="Your old password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">

                        <label>New Password</label><br>
                        <input type="password" v-model="form.new_password1" placeholder="Your new password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">

                        <label>Repeat Password</label><br>
                        <input type="password" v-model="form.new_password2" placeholder="Repeat password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
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
                old_password: '',
                new_password1: '',
                new_password2: '',
            },
            errors: [],
        }
    },

    methods: {
        SubmitForm() {
            this.errors = []

            if (this.form.new_password1 !== this.form.new_password2) {
                this.errors.push('Your passwords do not match')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('old_password', this.form.old_password)
                formData.append('new_password1', this.form.new_password1)
                formData.append('new_password2', this.form.new_password2)

                axios
                    .post('/api/editpassword/', formData, {
                        'headers': {
                            'Content-Type': 'multipart/form-data',
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'Information updated', 'bg-emerald-500')

                            this.$router.push(`/profile/${this.userStore.user.id}`)

                        } else {
                            this.toastStore.showToast(5000, 'Something went wrong', 'bg-red-300')

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