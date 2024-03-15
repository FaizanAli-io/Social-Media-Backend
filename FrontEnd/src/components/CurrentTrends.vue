<template>
    <!-- Trends section -->
    <div class="p-4 bg-white border border-gray-200 rounded-lg">

        <h3 class="mb-6 text-xl">Current Trends</h3>

        <!-- Four trending hashtags -->
        <div class="space-y-4">

            <!-- Hashtag 1 -->
            <div v-for="trend in trends" v-bind:key="trend.id" class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <p class="text-xs">
                        <strong>#{{ trend.content }}</strong><br>
                        <span class="text-gray-500">{{ trend.occurrence }} mentions</span>
                    </p>
                </div>

                <RouterLink :to="{ name: 'trend', params: { id: trend.content } }"
                    class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">
                    Explore
                </RouterLink>
            </div>

        </div>

    </div>
</template>

<script>

import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {

    data() { return { trends: [] } },

    mounted() { this.getTrends() },

    methods: {
        getTrends() {
            axios
                .get('api/posts/trends/')
                .then(response => {
                    console.log("Trends:", response.data);
                    this.trends = response.data;
                })
                .catch(error => {
                    console.log("Error:", error);
                });
        }
    },

    components: { RouterLink }
}

</script>