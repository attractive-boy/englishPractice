<template>
    <div ref="lineChart" class="chart"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'LineChart',
    props: ['data'],
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = echarts.init(this.$refs.lineChart);
        const option = {
          title: {
            text: '每日参与时长',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
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
              name: '时长 (分钟)',
              type: 'line',
              data: this.data.map(item => item.value),
              smooth: true,
              lineStyle: {
                color: '#42b983'
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
  