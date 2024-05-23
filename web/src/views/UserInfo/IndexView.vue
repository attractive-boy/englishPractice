<template>
  <div class="container">
    <EditTeacherProfile v-if="role == 'teacher'"/>
    <EditStudentProfile v-if="role == 'student'"/>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessage } from 'element-plus';
import EditTeacherProfile from '@/components/EditTeacherProfile/EditTeacherProfile.vue'
import EditStudentProfile from '@/components/EditStudentProfile/EditStudentProfile.vue'

const { proxy } = getCurrentInstance() as any;
const role = localStorage.getItem('role')
</script>

<style scoped>

</style>
