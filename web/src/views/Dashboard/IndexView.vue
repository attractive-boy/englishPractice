<template>
  <div>
    <student-analysis />
  </div>
</template>

<script>
import StudentAnalysis from '@/components/StudentAnalysis/StudentAnalysis.vue';

export default {
  name: 'Dashboard',
  components: {
    StudentAnalysis
  }
};
</script>
