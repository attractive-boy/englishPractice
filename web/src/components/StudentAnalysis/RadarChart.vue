<template>
    <div ref="radarChart" class="chart"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'RadarChart',
    props: ['data'],
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = echarts.init(this.$refs.radarChart);
        const option = {
          title: {
            text: '一周得分总分情况',
            left: 'center'
          },
          tooltip: {},
          radar: {
            indicator: this.data.map(item => ({
              name: item.name,
              max: 10
            }))
          },
          series: [{
            name: '得分情况',
            type: 'radar',
            data: [{
              value: this.data.map(item => item.value),
              name: '得分'
            }]
          }]
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
  