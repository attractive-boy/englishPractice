<template>
    <div ref="barChart" class="chart"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'BarChart',
    props: ['data'],
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = echarts.init(this.$refs.barChart);
        const option = {
          title: {
            text: '学习得分情况',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['词汇难度', '句法复杂度', '可读性公式', '文本结构', '读者背景知识'],
            bottom: '10'
          },
          xAxis: {
            type: 'category',
            data: this.data.map(item => item.date)
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '词汇难度',
              type: 'bar',
              data: this.data.map(item => item.scores.lexical)
            },
            {
              name: '句法复杂度',
              type: 'bar',
              data: this.data.map(item => item.scores.syntactic)
            },
            {
              name: '可读性公式',
              type: 'bar',
              data: this.data.map(item => item.scores.readability)
            },
            {
              name: '文本结构',
              type: 'bar',
              data: this.data.map(item => item.scores.structure)
            },
            {
              name: '读者背景知识',
              type: 'bar',
              data: this.data.map(item => item.scores.knowledge)
            }
          ]
        };
        chart.setOption(option);
      }
    }
  };
  </script>
  
  <style scoped>
  .chart {
    width: 100%;
    height: 400px;
  }
  </style>
  