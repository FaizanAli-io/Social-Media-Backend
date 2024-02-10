<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- Center of the Feed -->
        <div class="main-center col-span-3 space-y-4">

            <!-- Make a post section -->
            <div class="bg-white border border-gray-200 rounded-lg">
                <form method="post" v-on:submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>
                    </div>
                </form>
            </div>

            <!-- Text Post section -->
            <div v-for="post in posts" v-bind:key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
                <FeedItem v-bind:post="post" />
            </div>

        </div>

        <!-- Right side of the Feed -->
        <div class="main-right col-span-1 space-y-4">

            <PeopleYouMayKnow />

            <CurrentTrends />

        </div>

    </div>
</template>

<script>

import axios from 'axios'

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'
import CurrentTrends from '@/components/CurrentTrends.vue'
import FeedItem from '@/components/FeedItem.vue'

export default {
    name: 'FeedView',

    components: {
        PeopleYouMayKnow,
        CurrentTrends,
        FeedItem,
    },

    data() {
        return {
            posts: [],
            body: '',
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('api/posts/')
                .then(response => {
                    this.posts = response.data
                    console.log('Data: ', response.data)
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        submitForm() {
            console.log('Submit Form', this.body)

            axios
                .post('api/posts/create/', { 'body': this.body })
                .then(response => {
                    console.log('Data: ', response.data)
                    this.posts.unshift(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}

</script>