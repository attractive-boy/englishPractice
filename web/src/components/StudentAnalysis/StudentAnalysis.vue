<template>
  <div class="student-analysis">
    <h2>个人学习情况</h2>
    <el-button @click="$emit('close')" type="primary" style="margin-bottom: 20px;position: absolute;
    right: 40px;
    top: 125px;" v-if="role != 'student'">关闭</el-button>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else class="grid-container">
      <div class="grid-item">

        <line-chart :data="dailySummaryData"></line-chart>
      </div>
      <div class="grid-item">

        <pie-chart :data="scenarioPercentageData"></pie-chart>
      </div>
      <div class="grid-item">

        <radar-chart :data="weeklyScoreData"></radar-chart>
      </div>
      <div class="grid-item">

        <bar-chart :data="scoreTrendData"></bar-chart>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch } from 'vue';
import LineChart from './LineChart.vue';
import PieChart from './PieChart.vue';
import RadarChart from './RadarChart.vue';
import BarChart from './BarChart.vue';

const props = defineProps({
  records: Array
});
const role = localStorage.getItem('role');
const loading = ref(true);
const dailySummaryData = ref([]);
const scenarioPercentageData = ref([]);
const weeklyScoreData = ref([]);
const scoreTrendData = ref([]);

const processData = (records) => {
  dailySummaryData.value = calculateDailySummary(records);
  scenarioPercentageData.value = calculateScenarioPercentage(records);
  weeklyScoreData.value = calculateWeeklyScore(records);
  scoreTrendData.value = calculateScoreTrend(records);
};

const calculateDailySummary = (records) => {
  const summary = {};
  records.forEach(record => {
    const date = record.study_date;
    if (!summary[date]) {
      summary[date] = 0;
    }
    summary[date] += record.duration_minutes;
  });
  return Object.keys(summary).map(date => ({
    date,
    value: summary[date]
  }));
};

const calculateScenarioPercentage = (records) => {
  const scenarioCounts = {};
  records.forEach(record => {
    const scenario = record.scenario_name;
    if (!scenario) {
      // Skip records with empty scenario names
      return;
    }
    if (!scenarioCounts[scenario]) {
      scenarioCounts[scenario] = 0;
    }
    scenarioCounts[scenario] += 1;
  });
  const total = records.filter(record => record.scenario_name).length;
  return Object.keys(scenarioCounts).map(scenario => ({
    name: scenario,
    value: ((scenarioCounts[scenario] / total) * 100).toFixed(2)
  }));
};

const calculateWeeklyScore = (updatedRecords) => {
  const totalScores = {
    lexical: 0,
    syntactic: 0,
    readability: 0,
    structure: 0,
    knowledge: 0
  };
  updatedRecords.forEach(record => {
    totalScores.lexical += record.lexical_difficulty_score;
    totalScores.syntactic += record.syntactic_complexity_score;
    totalScores.readability += record.readability_formula_score;
    totalScores.structure += record.text_structure_score;
    totalScores.knowledge += record.reader_background_knowledge_score;
  });
  return [
    { name: '词汇难度', value: (totalScores.lexical).toFixed(2) },
    { name: '句法复杂度', value: (totalScores.syntactic).toFixed(2) },
    { name: '可读性公式', value: (totalScores.readability).toFixed(2) },
    { name: '文本结构', value: (totalScores.structure).toFixed(2) },
    { name: '读者背景知识', value: (totalScores.knowledge).toFixed(2) }
  ];
};

const calculateScoreTrend = (updatedRecords) => {
  return updatedRecords.map(record => ({
    date: record.study_date,
    scores: {
      lexical: record.lexical_difficulty_score,
      syntactic: record.syntactic_complexity_score,
      readability: record.readability_formula_score,
      structure: record.text_structure_score,
      knowledge: record.reader_background_knowledge_score
    }
  }));
};

watch(() => props.records, (newRecords) => {
  if (newRecords && newRecords.length > 0) {
    processData(newRecords);
    loading.value = false;
  }
}, { immediate: true });
</script>

<style scoped>
.student-analysis {
  padding: 20px;
}

.loading {
  text-align: center;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.grid-item {
  background: #fff;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.summary,
.scenario-percentage,
.score-analysis,
.score-trend {
  margin-bottom: 20px;
}
</style>

