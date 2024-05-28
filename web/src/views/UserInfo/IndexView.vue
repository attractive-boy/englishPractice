<template>
  <div class="container">
    <EditTeacherProfile />
  </div>
</template>

<script setup >
import { ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';
import EditTeacherProfile from '@/components/EditTeacherProfile/EditTeacherProfile.vue'

const { proxy } = getCurrentInstance() as any;


</script>

<style scoped>

</style>
