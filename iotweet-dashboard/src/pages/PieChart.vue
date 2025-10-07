<template>
    <div class="chart-container">
      <Pie :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { Pie } from 'vue-chartjs';
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  export default {
    components: { Pie },
    props: {
      data: {
        type: Array,
        required: true
      }
    },
    computed: {
      chartData() {
        return {
          labels: this.data.map(item => item.aggregate_name),
          datasets: [
            {
              label: 'Total Material Consumption',
              data: this.data.map(item => item.total_aggregate),
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
            }
          ]
        };
      },
      chartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false
        };
      }
    }
  };
  </script>
  
  <style scoped>
  .chart-container {
    width: 100%;
    height: 400px;
  }
  </style>
  