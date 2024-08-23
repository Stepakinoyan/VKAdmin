<template>
    <Card style="overflow: hidden" class="border border-gosuslugi-border">
        <template #title>{{ title }}</template>
        <template #content>
            <ul class="space-y-4">
                <li v-for="item in items"><a href="#" class="text-blue-700 hover:text-blue-600 text-base">{{ item }}</a></li>
            </ul>
        </template>
    </Card>
</template>


<script>
export default {
    props: {
        title: String,
        items: Array
    }
}
</script>   