<template>
  <div class="bg-background-dark border border-border-color rounded-lg p-6 flex flex-col items-center">
    <p class="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">{{ title }}</p>
    <div ref="chartRef" class="h-[200px] w-full"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts/core'
import { GaugeChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([GaugeChart, CanvasRenderer])

const props = defineProps<{
  title: string
  value: number
  max?: number
  unit?: string // e.g. '%', 'GB'
  variant?: 'cpu' | 'ram' | 'temp' | 'disk'
  detailFormatter?: (val: number) => string
}>()

const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

const colorStops = {
  cpu: [[0.3, '#22c55e'], [0.7, '#25d1f4'], [1, '#ef4444']],
  ram: [[0.3, '#8b5cf6'], [0.7, '#a855f7'], [1, '#ef4444']],
  temp: [[0.5, '#22c55e'], [0.8, '#f59e0b'], [1, '#ef4444']],
  disk: [[0.7, '#22c55e'], [0.9, '#f59e0b'], [1, '#ef4444']]
}

const mainColor = {
  cpu: '#25d1f4',
  ram: '#a855f7',
  temp: '#f59e0b',
  disk: '#22c55e'
}

function initChart() {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

function updateChart() {
  if (!chart) return
  
  const variant = props.variant || 'cpu'
  const maxVal = props.max || 100
  const stops = colorStops[variant] || colorStops.cpu
  const ptrColor = mainColor[variant] || mainColor.cpu

  const option = {
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: maxVal,
      radius: '90%',
      center: ['50%', '70%'],
      axisLine: {
        lineStyle: {
          width: 15,
          color: stops
        }
      },
      pointer: {
        icon: 'path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.194028 2092.44859,617.312956 L2096.90698,728.755929 C2097.05155,732.369577 2094.2393,735.416212 2090.62566,735.56078 C2090.53845,735.564269 2090.45117,735.566014 2090.36389,735.566014 L2090.36389,735.566014 C2086.74736,735.566014 2083.81557,732.63423 2083.81557,729.017692 C2083.81557,728.930412 2083.81732,728.84314 2083.82081,728.755929 L2088.2792,617.312956 C2088.32396,616.194028 2089.24407,615.30999 2090.36389,615.30999 Z',
        length: '75%',
        width: 8,
        offsetCenter: [0, '5%'],
        itemStyle: { color: ptrColor }
      },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: {
        color: '#64748b',
        fontSize: 10,
        distance: -30,
        formatter: (val: number) => {
            if (maxVal <= 100) return val % 25 === 0 ? val + '' : ''
            return val % (maxVal/4) === 0 ? val + '' : ''
        }
      },
      detail: {
        valueAnimation: true,
        formatter: props.detailFormatter ? props.detailFormatter(props.value) : '{value}' + (props.unit || ''),
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
        offsetCenter: [0, '20%']
      },
      data: [{ value: props.value }]
    }]
  }
  chart.setOption(option)
}

watch(() => props.value, () => {
    updateChart()
})

onMounted(() => {
  nextTick(() => {
     initChart()
     window.addEventListener('resize', ResizeHandler)
  })
})

onUnmounted(() => {
    window.removeEventListener('resize', ResizeHandler)
    if (chart) chart.dispose()
})

function ResizeHandler() {
    chart?.resize()
}
</script>
