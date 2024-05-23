<template>
    <div ref="pieChart" class="chart"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'PieChart',
    props: ['data'],
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = echarts.init(this.$refs.pieChart);
        const option = {
          title: {
            text: '学习场景占比',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            bottom: '10',
            left: 'center'
          },
          series: [
            {
              name: '场景占比',
              type: 'pie',
              radius: '50%',
              data: this.data.map(item => ({ name: item.name, value: item.value })),
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
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
  