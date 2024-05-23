<template>
    <div class="student-analysis">
      <h2>个人学习情况</h2>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else>
        <div class="summary">
          <h3>每日参与时长 (分钟)</h3>
          <line-chart :data="dailySummaryData"></line-chart>
        </div>
        <div class="scenario-percentage">
          <h3>学习场景占比 (周)</h3>
          <pie-chart :data="scenarioPercentageData"></pie-chart>
        </div>
        <div class="score-analysis">
          <h3>一周得分总分情况</h3>
          <radar-chart :data="weeklyScoreData"></radar-chart>
        </div>
        <div class="score-trend">
          <h3>得分情况统计</h3>
          <score-line-chart :data="scoreTrendData"></score-line-chart>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import LineChart from './LineChart.vue';
  import PieChart from './PieChart.vue';
  import RadarChart from './RadarChart.vue';
  import ScoreLineChart from './ScoreLineChart.vue';
  
  export default {
    name: 'StudentAnalysis',
    components: {
      LineChart,
      PieChart,
      RadarChart,
      ScoreLineChart
    },
    data() {
      return {
        loading: true,
        dailySummaryData: [],
        scenarioPercentageData: [],
        weeklyScoreData: [],
        scoreTrendData: []
      };
    },
    async created() {
      try {
        const userId = this.$route.params.userId; // 假设 userId 是通过路由传递的
        const response = await axios.get(`/api/study_records/weekly?user_id=${userId}`);
        const { records, updated_records } = response.data;
        this.processData(records, updated_records);
      } catch (error) {
        console.error('Error fetching study records:', error);
      } finally {
        this.loading = false;
      }
    },
    methods: {
      processData(records, updatedRecords) {
        this.dailySummaryData = this.calculateDailySummary(records);
        this.scenarioPercentageData = this.calculateScenarioPercentage(records);
        this.weeklyScoreData = this.calculateWeeklyScore(updatedRecords);
        this.scoreTrendData = this.calculateScoreTrend(updatedRecords);
      },
      calculateDailySummary(records) {
        // 计算每日参与时长
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
      },
      calculateScenarioPercentage(records) {
        // 计算学习场景占比
        const scenarioCounts = {};
        records.forEach(record => {
          const scenario = record.scenario_name;
          if (!scenarioCounts[scenario]) {
            scenarioCounts[scenario] = 0;
          }
          scenarioCounts[scenario] += 1;
        });
        const total = records.length;
        return Object.keys(scenarioCounts).map(scenario => ({
          name: scenario,
          value: ((scenarioCounts[scenario] / total) * 100).toFixed(2)
        }));
      },
      calculateWeeklyScore(updatedRecords) {
        // 计算一周的得分总分情况
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
        const days = updatedRecords.length;
        return [
          { name: '词汇难度', value: (totalScores.lexical / days).toFixed(2) },
          { name: '句法复杂度', value: (totalScores.syntactic / days).toFixed(2) },
          { name: '可读性公式', value: (totalScores.readability / days).toFixed(2) },
          { name: '文本结构', value: (totalScores.structure / days).toFixed(2) },
          { name: '读者背景知识', value: (totalScores.knowledge / days).toFixed(2) }
        ];
      },
      calculateScoreTrend(updatedRecords) {
        // 计算得分情况统计
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
      }
    }
  };
  </script>
  
  <style scoped>
  .student-analysis {
    padding: 20px;
  }
  .loading {
    text-align: center;
  }
  .summary, .scenario-percentage, .score-analysis, .score-trend {
    margin-bottom: 20px;
  }
  </style>
  