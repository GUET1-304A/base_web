<template>
  <div class="editor-section">
    <div class="editor-group">
      <h3 class="group-title">区块信息</h3>
      
      <div class="form-field">
        <label class="field-label">区块标题</label>
        <input 
          type="text" 
          class="field-input"
          :value="modelValue.title"
          @input="update('title', $event.target.value)"
          placeholder="如: 人员介绍"
        >
      </div>
      
      <div class="form-field">
        <label class="field-label">区块描述</label>
        <textarea 
          class="field-textarea"
          :value="modelValue.description"
          @input="update('description', $event.target.value)"
          placeholder="区块的简短描述"
          rows="2"
        ></textarea>
      </div>
    </div>
    
    <div class="editor-group">
      <div class="group-header">
        <h3 class="group-title">成员小组</h3>
        <button class="add-btn" @click="addGroup">+ 添加小组</button>
      </div>
      
      <div class="groups-list">
        <div 
          v-for="(group, index) in modelValue.groups" 
          :key="index"
          class="group-item"
        >
          <div class="group-item-header">
            <div class="group-tag-preview" v-if="group.tag">{{ group.tag }}</div>
            <span class="group-name-preview">{{ group.name || '未命名小组' }}</span>
            <button class="remove-btn" @click="removeGroup(index)" title="删除">×</button>
          </div>
          
          <div class="group-fields">
            <div class="form-row">
              <div class="form-field">
                <label class="field-label">小组标签</label>
                <input 
                  type="text"
                  class="field-input"
                  :value="group.tag"
                  @input="updateGroup(index, 'tag', $event.target.value)"
                  placeholder="如: 产品策划"
                >
              </div>
              
              <div class="form-field">
                <label class="field-label">小组名称</label>
                <input 
                  type="text"
                  class="field-input"
                  :value="group.name"
                  @input="updateGroup(index, 'name', $event.target.value)"
                  placeholder="如: 流光组"
                >
              </div>
            </div>
            
            <div class="form-field">
              <label class="field-label">小组描述</label>
              <textarea 
                class="field-textarea"
                :value="group.description"
                @input="updateGroup(index, 'description', $event.target.value)"
                placeholder="描述小组的职责和工作内容"
                rows="2"
              ></textarea>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="!modelValue.groups?.length" class="empty-state">
        <p>暂无小组，点击上方按钮添加</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

function update(key, value) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

function updateGroup(index, key, value) {
  const groups = [...(props.modelValue.groups || [])]
  groups[index] = { ...groups[index], [key]: value }
  emit('update:modelValue', { ...props.modelValue, groups })
}

function addGroup() {
  const groups = [...(props.modelValue.groups || []), { tag: '', name: '', description: '' }]
  emit('update:modelValue', { ...props.modelValue, groups })
}

function removeGroup(index) {
  const groups = (props.modelValue.groups || []).filter((_, i) => i !== index)
  emit('update:modelValue', { ...props.modelValue, groups })
}
</script>

<style scoped>
.editor-section {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.editor-group {
  background: rgba(12, 24, 42, 0.5);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  padding: 24px;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.group-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: var(--text);
}

.group-header .group-title {
  margin: 0;
}

.form-field {
  margin-bottom: 16px;
}

.form-field:last-child {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  margin-bottom: 8px;
}

.field-input,
.field-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text);
  font-size: 14px;
  transition: border-color 0.2s, background 0.2s;
}

.field-input:focus,
.field-textarea:focus {
  outline: none;
  border-color: var(--primary);
  background: rgba(121, 168, 255, 0.05);
}

.field-textarea {
  resize: vertical;
  min-height: 60px;
  line-height: 1.6;
}

.add-btn {
  padding: 8px 16px;
  border: 1px solid var(--primary);
  border-radius: 8px;
  background: transparent;
  color: var(--primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background: rgba(121, 168, 255, 0.1);
}

.groups-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.group-item {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(121, 168, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
}

.group-item-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(121, 168, 255, 0.05);
  border-bottom: 1px solid rgba(121, 168, 255, 0.1);
}

.group-tag-preview {
  padding: 4px 10px;
  background: rgba(121, 168, 255, 0.15);
  color: var(--primary-strong);
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.group-name-preview {
  flex: 1;
  font-weight: 600;
  color: var(--text);
}

.group-fields {
  padding: 16px;
}

.remove-btn {
  width: 28px;
  height: 28px;
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 6px;
  background: transparent;
  color: #ff6b6b;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 100, 100, 0.1);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--muted);
}
</style>
