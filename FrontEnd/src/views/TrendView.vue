<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- Center of the Feed -->
        <div class="main-center col-span-3 space-y-4">

            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <h2 class="text-xl font-bold">Trend: #{{ $route.params.id }}</h2>
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
        }
    },

    mounted() {
        this.getFeed()
    },

    watch: {
        '$route.params.id': {
            handler: function () {
                this.getFeed()
            },
            immediate: true,
            deep: true,
        }
    },

    methods: {
        getFeed() {
            axios
                .get(`api/posts/?trend=${this.$route.params.id}`)
                .then(response => {
                    console.log('Data: ', response.data)
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },
    }
}

</script>