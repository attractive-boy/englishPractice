<template>
    <div ref="scoreLineChart" class="chart"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'ScoreLineChart',
    props: ['data'],
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = echarts.init(this.$refs.scoreLineChart);
        const option = {
          title: {
            text: '得分情况统计',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            bottom: '10',
            data: ['词汇难度', '句法复杂度', '可读性公式', '文本结构', '读者背景知识']
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
              type: 'line',
              data: this.data.map(item => item.scores.lexical),
              smooth: true,
              lineStyle: {
                color: '#FF6384'
              }
            },
            {
              name: '句法复杂度',
              type: 'line',
              data: this.data.map(item => item.scores.syntactic),
              smooth: true,
              lineStyle: {
                color: '#36A2EB'
              }
            },
            {
              name: '可读性公式',
              type: 'line',
              data: this.data.map(item => item.scores.readability),
              smooth: true,
              lineStyle: {
                color: '#FFCE56'
              }
            },
            {
              name: '文本结构',
              type: 'line',
              data: this.data.map(item => item.scores.structure),
              smooth: true,
              lineStyle: {
                color: '#4BC0C0'
              }
            },
            {
              name: '读者背景知识',
              type: 'line',
              data: this.data.map(item => item.scores.knowledge),
              smooth: true,
              lineStyle: {
                color: '#9966FF'
              }
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
  