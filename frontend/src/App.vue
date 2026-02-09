<script setup lang="ts">
import { ref } from 'vue'
import ChartWidget from './components/ChartWidget.vue'

// 預設查詢參數
const stockCode = ref('2330')
const startDate = ref('2024-01-01')
const endDate = ref('2024-01-31')
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1>📈 台灣股市時光機</h1>
      <p class="subtitle">Taiwan Market Time Machine - M02 Chart Demo</p>
    </header>
    
    <main class="app-main">
      <div class="demo-controls">
        <div class="control-group">
          <label for="stock-code">股票代碼</label>
          <input 
            id="stock-code" 
            v-model="stockCode" 
            type="text" 
            placeholder="2330"
          />
        </div>
        <div class="control-group">
          <label for="start-date">起始日期</label>
          <input 
            id="start-date" 
            v-model="startDate" 
            type="date"
          />
        </div>
        <div class="control-group">
          <label for="end-date">結束日期</label>
          <input 
            id="end-date" 
            v-model="endDate" 
            type="date"
          />
        </div>
      </div>
      
      <div class="chart-demo">
        <ChartWidget 
          :key="`${stockCode}-${startDate}-${endDate}`"
          :stock-code="stockCode"
          :start-date="startDate"
          :end-date="endDate"
        />
      </div>
    </main>
  </div>
</template>

<style>
:root {
  --color-primary: #0d6efd;
  --color-primary-hover: #0b5ed7;
  --color-background: #ffffff;
  --color-background-soft: #f8f9fa;
  --color-background-mute: #e9ecef;
  --color-text: #212529;
  --color-text-secondary: #6c757d;
  --color-border: #dee2e6;
  --color-error: #dc3545;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: var(--color-background-soft);
  color: var(--color-text);
}

#app {
  width: 100%;
  min-height: 100vh;
}
</style>

<style scoped>
.app-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: white;
  padding: 2rem;
  text-align: center;
  border-bottom: 1px solid var(--color-border);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.app-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.app-main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

.demo-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.control-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.control-group input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.control-group input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
}

.chart-demo {
  min-height: 500px;
}
</style>
