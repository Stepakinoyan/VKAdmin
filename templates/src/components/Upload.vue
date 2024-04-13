<template>
    <div class="flex justify-center items-center">
        <Toast class="text-bla"/>
        <FileUpload mode="basic" name="file" url="http://localhost:7777/excel/upload" @upload="onUpload" :auto="true" chooseLabel="Загрузить"/>
    </div>
</template>

<script>
import { useToast } from 'primevue/usetoast';
export default {
    data(){
        return {
            toast: useToast()
        }
        
    },
    methods: {
        onUpload() {
            this.$toast.add({ severity: 'contrast', summary: 'Success', detail: 'Файл загружен!', life: 6000 });
        }
    }
};
</script>