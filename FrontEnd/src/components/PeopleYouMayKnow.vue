<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">

        <h3 class="mb-6 text-xl">People you may know</h3>

        <div class="space-y-4">

            <div v-for="person in suggestions" v-bind:key="person.id" class="flex items-center justify-between">

                <div class="flex items-center space-x-2">
                    <img :src="person.avatar_url" class="w-[40px] rounded-full">

                    <p class="text-xs"><strong>{{ person.name }}</strong></p>
                </div>

                <RouterLink :to="{ name: 'profile', params: { id: person.id } }"
                    class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</RouterLink>

            </div>

        </div>

    </div>
</template>

<script>

import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {

    data() { return { suggestions: [] } },

    mounted() { this.getSuggestions() },

    methods: {
        getSuggestions() {
            axios
                .get('api/friends/suggest/')
                .then(response => {
                    console.log("Suggested: ", response.data);
                    this.suggestions = response.data;
                })
                .catch(error => {
                    console.log("Error:", error);
                });
        }
    },

    components: { RouterLink }
}

</script>