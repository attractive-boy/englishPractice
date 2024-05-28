<template>
  <div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else>
      <student-analysis v-if="showCharts" :records="studentRecords" @close="hideCharts"/>
      <div class="student-management" v-else >
        <el-table :data="students" style="width: 100%">
          <el-table-column prop="student_id" label="学生ID"></el-table-column>
          <el-table-column prop="average_lexical_difficulty_score" label="词汇难度平均分"></el-table-column>
          <el-table-column prop="average_syntactic_complexity_score" label="句法复杂度平均分"></el-table-column>
          <el-table-column prop="average_readability_formula_score" label="可读性公式平均分"></el-table-column>
          <el-table-column prop="average_text_structure_score" label="文本结构平均分"></el-table-column>
          <el-table-column prop="average_reader_background_knowledge_score" label="读者背景知识平均分"></el-table-column>
          <el-table-column prop="average_score" label="总平均分"></el-table-column>
          <el-table-column prop="average_duration_minutes" label="平均学习时长 (分钟)"></el-table-column>
          <el-table-column prop="most_common_scenario" label="最常用学习场景"></el-table-column>
          <el-table-column label="操作">
            <template v-slot="scope">
              <el-button size="mini" @click="showDetails(scope.row)">查看详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue';
import StudentAnalysis from '@/components/StudentAnalysis/StudentAnalysis.vue';
import { ElMessage } from 'element-plus';

const { proxy } = getCurrentInstance();

const loading = ref(true);
const role = localStorage.getItem('role');
const showCharts = ref(role === 'student');
const students = ref([]);
const studentRecords = ref(null);

const fetchStudentRecords = async (studentId) => {
  try {
    const response = await proxy.$http.get(`/study_records/weekly?student_id=${studentId}`);
    studentRecords.value = response.data.records;
  } catch (error) {
    ElMessage.error('Failed to fetch student records');
  } finally {
    loading.value = false;
  }
};

const showDetails = (student) => {
  fetchStudentRecords(student.student_id);
  showCharts.value = true;
};

const hideCharts = () => {
  showCharts.value = false;
};

const fetchWeeklyAverageStudyRecords = async () => {
  try {
    const response = await proxy.$http.get('/study_records/weekly/average');
    students.value = response.data;
  } catch (error) {
    ElMessage.error('Failed to fetch weekly average study records');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (showCharts.value) {
    fetchStudentRecords();
  } else {
    fetchWeeklyAverageStudyRecords();
  }
});
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 20px;
}

.student-management {
  padding: 20px;
}
</style>
