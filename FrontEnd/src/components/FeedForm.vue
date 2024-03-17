<template>
    <form method="post" v-on:submit.prevent="submitForm">
        <div class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                placeholder="What are you thinking about?"></textarea>

            <label>
                <input type="checkbox" v-model="isPrivate"> Private
            </label>

            <div id="preview" v-if="url"><img :src="url" class="w-[100px] rounded-xl mt-3"></div>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                <input type="file" ref="file" @change="onFileChange"> Attach image
            </label>

            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<script>

import axios from 'axios'

export default {
    name: 'FeedForm',

    emits: ['postCreated'],

    props: {
        user: Object,
        posts: Array
    },

    data() {
        return {
            body: '',
            url: null,
            isPrivate: false,
        }
    },

    methods: {
        onFileChange(e) {
            const file = e.target.files[0]
            this.url = URL.createObjectURL(file)
        },

        submitForm() {
            console.log('Submit Form:', this.body)

            let formData = new FormData()
            formData.append('body', this.body)
            formData.append('is_private', this.isPrivate)
            formData.append('image', this.$refs.file.files[0])

            axios
                .post('api/posts/create/', formData, {
                    'headers': {
                        'Content-Type': 'multipart/form-data',
                    }
                })
                .then(response => {
                    console.log('Data: ', response.data)

                    this.body = ''
                    this.url = null
                    this.isPrivate = false
                    this.$refs.file.value = null

                    this.$emit('postCreated', response.data)
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },
    }
}

</script>
