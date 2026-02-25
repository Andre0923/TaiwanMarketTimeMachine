<script setup lang="ts">
import { ref } from 'vue'
import ChartWidget from './components/ChartWidget.vue'
import ChartGrid from './components/ChartGrid.vue'

// View Mode
const viewMode = ref<'single' | 'grid'>('single')

// Single Chart State
const stockCode = ref('2330')
const startDate = ref('2024-01-01')
const endDate = ref('2024-01-31')

// Grid State
const newStockCode = ref('')
const gridCharts = ref([
  { stockCode: '2330', startDate: '2024-01-01', endDate: '2024-01-31' },
  { stockCode: '2317', startDate: '2024-01-01', endDate: '2024-01-31' },
  { stockCode: '2454', startDate: '2024-01-01', endDate: '2024-01-31' }
])

function addToGrid(): void {
  const code = newStockCode.value.trim()
  if (!code) return
  if (gridCharts.value.some(chart => chart.stockCode === code)) {
    alert(股票  已在監控列表中)
    return
  }
  gridCharts.value.push({
    stockCode: code,
    startDate: '2024-01-01',
    endDate: '2024-01-31'
  })
  newStockCode.value = ''
}

function removeFromGrid(code: string): void {
  gridCharts.value = gridCharts.value.filter(chart => chart.stockCode !== code)
}
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1> 台灣股市時光機</h1>
      <p class="subtitle">Taiwan Market Time Machine - M02 Chart Demo</p>
      <div class="view-toggle">
        <button :class="['toggle-btn', { active: viewMode === 'single' }]" @click="viewMode = 'single'">單一圖表</button>
        <button :class="['toggle-btn', { active: viewMode === 'grid' }]" @click="viewMode = 'grid'">多圖監控</button>
      </div>
    </header>
    
    <main class="app-main">
      <div v-if="viewMode === 'single'" class="demo-controls">
        <div class="control-group">
          <label for="stock-code">股票代碼</label>
          <input id="stock-code" v-model="stockCode" type="text" placeholder="2330" />
        </div>
        <div class="control-group">
          <label for="start-date">起始日期</label>
          <input id="start-date" v-model="startDate" type="date" />
        </div>
        <div class="control-group">
          <label for="end-date">結束日期</label>
          <input id="end-date" v-model="endDate" type="date" />
        </div>
      </div>

      <div v-if="viewMode === 'grid'" class="grid-control-panel">
        <div class="control-group-grid">
          <label>監控股票列表：</label>
          <div class="stock-tags">
            <span v-for="chart in gridCharts" :key="chart.stockCode" class="stock-tag">
              {{ chart.stockCode }}
              <button class="remove-tag" @click="removeFromGrid(chart.stockCode)"></button>
            </span>
          </div>
        </div>
        <div class="control-group-grid">
          <input v-model="newStockCode" type="text" class="stock-input" placeholder="輸入股票代號" @keyup.enter="addToGrid" />
          <button class="add-btn" @click="addToGrid">新增股票</button>
        </div>
      </div>
      
      <div class="chart-demo">
        <ChartWidget v-if="viewMode === 'single'" :key="\\-\-\\" :stock-code="stockCode" :start-date="startDate" :end-date="endDate" />
        <ChartGrid v-if="viewMode === 'grid'" :charts="gridCharts" :default-columns="3" />
      </div>
    </main>
  </div>
</template>

<style>
:root { --color-background: #f8f9fa; --color-background-soft: #ffffff; --color-background-mute: #f1f3f5; --color-border: #dee2e6; --color-text: #212529; --color-text-secondary: #6c757d; --color-primary: #667eea; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; -webkit-font-smoothing: antialiased; }
#app { width: 100%; min-height: 100vh; }
</style>

<style scoped>
.app-container { width: 100%; min-height: 100vh; background-color: var(--color-background); }
.app-header { position: relative; padding: 2rem 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.app-header h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
.app-header .subtitle { font-size: 0.875rem; opacity: 0.9; }
.view-toggle { position: absolute; top: 2rem; right: 3rem; display: flex; gap: 0.5rem; background-color: rgba(255,255,255,0.2); padding: 0.25rem; border-radius: 8px; }
.toggle-btn { padding: 0.5rem 1.5rem; border: none; background-color: transparent; color: white; font-weight: 500; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
.toggle-btn:hover { background-color: rgba(255,255,255,0.15); }
.toggle-btn.active { background-color: white; color: #667eea; font-weight: 600; }
.demo-controls { display: flex; gap: 1.5rem; padding: 1.5rem 3rem; background-color: var(--color-background-soft); border-bottom: 1px solid var(--color-border); }
.control-group { display: flex; flex-direction: column; gap: 0.5rem; min-width: 200px; }
.control-group label { font-weight: 600; font-size: 0.875rem; color: var(--color-text); }
.control-group input { padding: 0.625rem 0.875rem; border: 1px solid var(--color-border); border-radius: 6px; font-size: 0.875rem; background-color: white; transition: all 0.2s; }
.control-group input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
.grid-control-panel { padding: 1.5rem 3rem; background-color: var(--color-background-soft); border-bottom: 1px solid var(--color-border); }
.control-group-grid { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.control-group-grid:last-child { margin-bottom: 0; }
.control-group-grid label { font-weight: 600; font-size: 0.875rem; color: var(--color-text); white-space: nowrap; }
.stock-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; flex: 1; }
.stock-tag { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background-color: #667eea; color: white; border-radius: 20px; font-size: 0.875rem; font-weight: 500; box-shadow: 0 2px 4px rgba(102,126,234,0.2); }
.remove-tag { width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; background-color: rgba(255,255,255,0.3); border: none; border-radius: 50%; color: white; font-size: 0.75rem; cursor: pointer; transition: background-color 0.2s; }
.remove-tag:hover { background-color: rgba(255,255,255,0.5); }
.stock-input { flex: 1; padding: 0.625rem 0.875rem; border: 1px solid var(--color-border); border-radius: 6px; font-size: 0.875rem; background-color: white; transition: all 0.2s; }
.stock-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
.add-btn { padding: 0.625rem 1.5rem; background-color: #667eea; color: white; border: none; border-radius: 6px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.add-btn:hover { background-color: #5568d3; box-shadow: 0 4px 8px rgba(102,126,234,0.3); }
.chart-demo { padding: 0; }
@media (max-width: 768px) {
  .app-header { padding: 1.5rem; }
  .view-toggle { position: static; margin-top: 1rem; }
  .demo-controls { flex-direction: column; padding: 1.5rem; }
  .grid-control-panel { padding: 1.5rem; }
  .control-group-grid { flex-direction: column; align-items: stretch; }
  .stock-tags { width: 100%; }
}
</style>
