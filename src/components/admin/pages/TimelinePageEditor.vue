<template>
  <div class="timeline-editor">
    <!-- Hero 区域 -->
    <div class="form-section">
      <h3>Hero 区域</h3>
      <div class="form-group">
        <label>小标签</label>
        <input v-model="content.hero.eyebrow" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>主标题</label>
        <input v-model="content.hero.title" type="text" @input="emitUpdate" />
      </div>
      <div class="form-group">
        <label>副标题</label>
        <input v-model="content.hero.subtitle" type="text" @input="emitUpdate" />
      </div>
    </div>

    <!-- 即将到来 -->
    <div class="form-section">
      <h3>即将到来的活动</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.upcomingTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="events-list">
        <div v-for="(event, index) in content.upcoming" :key="index" class="event-card">
          <div class="card-header">
            <span>{{ event.title || `活动 ${index + 1}` }}</span>
            <button class="remove-btn small" @click="removeUpcoming(index)">×</button>
          </div>
          <input v-model="event.title" placeholder="活动名称" @input="emitUpdate" />
          <div class="form-row">
            <input v-model="event.date" type="date" @input="emitUpdate" />
            <input v-model="event.type" placeholder="类型 (如: 讲座)" @input="emitUpdate" />
          </div>
          <textarea v-model="event.description" placeholder="活动描述" rows="2" @input="emitUpdate"></textarea>
        </div>
      </div>
      <button class="add-btn" @click="addUpcoming">+ 添加活动</button>
    </div>

    <!-- 里程碑 -->
    <div class="form-section">
      <h3>里程碑</h3>
      <div class="form-group">
        <label>区块标题</label>
        <input v-model="content.sections.milestonesTitle" type="text" @input="emitUpdate" />
      </div>
      <div class="milestones-list">
        <div v-for="(milestone, index) in content.milestones" :key="index" class="milestone-item">
          <div class="item-header">
            <input v-model="milestone.year" placeholder="年份" class="year-input" @input="emitUpdate" />
            <button class="remove-btn small" @click="removeMilestone(index)">×</button>
          </div>
          <input v-model="milestone.title" placeholder="标题" @input="emitUpdate" />
          <textarea v-model="milestone.description" placeholder="描述" rows="2" @input="emitUpdate"></textarea>
        </div>
      </div>
      <button class="add-btn" @click="addMilestone">+ 添加里程碑</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const defaultContent = {
  hero: { eyebrow: '', title: '', subtitle: '' },
  upcoming: [],
  milestones: [],
  sections: { upcomingTitle: '', milestonesTitle: '' }
}

const content = reactive({ ...defaultContent })

onMounted(() => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...props.modelValue })))
})

watch(() => props.modelValue, (newVal) => {
  Object.assign(content, JSON.parse(JSON.stringify({ ...defaultContent, ...newVal })))
}, { deep: true })

function emitUpdate() {
  emit('update:modelValue', JSON.parse(JSON.stringify(content)))
}

function addUpcoming() {
  content.upcoming.push({ title: '', date: '', type: '', description: '' })
  emitUpdate()
}

function removeUpcoming(index) {
  content.upcoming.splice(index, 1)
  emitUpdate()
}

function addMilestone() {
  content.milestones.push({ year: '', title: '', description: '' })
  emitUpdate()
}

function removeMilestone(index) {
  content.milestones.splice(index, 1)
  emitUpdate()
}
</script>

<style scoped>
.timeline-editor {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  padding: 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--panel-border);
  border-radius: 14px;
}

.form-section h3 {
  margin: 0 0 20px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-section h3::before {
  content: '';
  width: 4px;
  height: 16px;
  background: var(--primary);
  border-radius: 2px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.events-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.event-card {
  padding: 20px;
  background: rgba(121, 168, 255, 0.05);
  border: 1px solid rgba(121, 168, 255, 0.2);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

.event-card input,
.event-card textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.event-card input:focus,
.event-card textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.milestones-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.milestone-item {
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--panel-border);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.year-input {
  width: 100px;
  padding: 8px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--primary);
  font-size: 18px;
  font-weight: 700;
}

.milestone-item input,
.milestone-item textarea {
  padding: 10px 12px;
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.3);
  color: var(--text);
  font-size: 13px;
}

.milestone-item input:focus,
.milestone-item textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.add-btn {
  padding: 10px 20px;
  border: 1px dashed var(--panel-border);
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.remove-btn.small {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 100, 100, 0.1);
  color: #ff6b6b;
  font-size: 14px;
  cursor: pointer;
  flex-shrink: 0;
}

.remove-btn.small:hover {
  background: rgba(255, 100, 100, 0.2);
}
</style>
