<template>
  <section class="applications-manager">
    <div class="toolbar">
      <div class="filter-group">
        <button
          v-for="item in filters"
          :key="item.value"
          type="button"
          :class="['filter-btn', { active: activeFilter === item.value }]"
          @click="activeFilter = item.value"
        >
          {{ item.label }}
        </button>
      </div>

      <button type="button" class="refresh-btn" @click="loadApplications" :disabled="loading">
        {{ loading ? '刷新中...' : '刷新列表' }}
      </button>
    </div>

    <div v-if="errorMessage" class="panel-message error">{{ errorMessage }}</div>
    <div v-else-if="successMessage" class="panel-message success">{{ successMessage }}</div>

    <div v-if="loading" class="empty-state">
      <p>正在加载报名记录...</p>
    </div>

    <div v-else-if="!applications.length" class="empty-state">
      <p>当前筛选条件下还没有报名记录。</p>
    </div>

    <div v-else class="application-list">
      <article v-for="application in applications" :key="application.id" class="application-card">
        <div class="card-header">
          <div>
            <h3>{{ application.name }}</h3>
            <p>
              {{ application.group_name }} · {{ formatTime(application.created_at) }}
            </p>
          </div>
          <span :class="['status-badge', `status-${drafts[application.id]?.status || application.status}`]">
            {{ statusLabel(drafts[application.id]?.status || application.status) }}
          </span>
        </div>

        <div class="meta-grid">
          <div><span>学号</span><strong>{{ application.student_id }}</strong></div>
          <div><span>专业</span><strong>{{ application.grade_major }}</strong></div>
          <div><span>手机号</span><strong>{{ application.phone }}</strong></div>
          <div><span>邮箱</span><strong>{{ application.email }}</strong></div>
          <div><span>飞书通知</span><strong>{{ application.feishu_sent ? '已发送' : '发送失败' }}</strong></div>
          <div><span>处理时间</span><strong>{{ formatTime(application.processed_at) || '未处理' }}</strong></div>
        </div>

        <div class="links-row">
          <a v-if="application.github_url" :href="application.github_url" target="_blank" rel="noreferrer">
            GitHub
          </a>
          <a v-if="application.portfolio_url" :href="application.portfolio_url" target="_blank" rel="noreferrer">
            作品集
          </a>
          <span v-if="!application.github_url && !application.portfolio_url" class="muted-text">
            未填写外部链接
          </span>
        </div>

        <div class="content-block">
          <span>相关经历</span>
          <p>{{ application.experience || '未填写' }}</p>
        </div>

        <div class="content-block">
          <span>报名说明</span>
          <p>{{ application.motivation }}</p>
        </div>

        <div v-if="application.feishu_error" class="content-block warning-block">
          <span>飞书错误</span>
          <p>{{ application.feishu_error }}</p>
        </div>

        <div class="editor-grid">
          <label class="form-group">
            <span>处理状态</span>
            <select v-model="drafts[application.id].status">
              <option value="pending">待处理</option>
              <option value="reviewing">处理中</option>
              <option value="processed">已处理</option>
              <option value="archived">已归档</option>
            </select>
          </label>

          <label class="form-group form-group-wide">
            <span>后台备注</span>
            <textarea
              v-model.trim="drafts[application.id].admin_note"
              rows="3"
              placeholder="记录跟进情况、面试安排或处理结果"
            ></textarea>
          </label>
        </div>

        <div class="card-actions">
          <button
            type="button"
            class="save-btn"
            :disabled="savingId === application.id || !hasChanges(application)"
            @click="saveApplication(application)"
          >
            {{ savingId === application.id ? '保存中...' : '保存处理状态' }}
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { api } from '../../services/api.js'

const applications = ref([])
const drafts = ref({})
const loading = ref(false)
const savingId = ref(null)
const activeFilter = ref('all')
const errorMessage = ref('')
const successMessage = ref('')

const filters = [
  { value: 'all', label: '全部' },
  { value: 'pending', label: '待处理' },
  { value: 'reviewing', label: '处理中' },
  { value: 'processed', label: '已处理' },
  { value: 'archived', label: '已归档' }
]

function statusLabel(status) {
  return {
    pending: '待处理',
    reviewing: '处理中',
    processed: '已处理',
    archived: '已归档'
  }[status] || '待处理'
}

function formatTime(value) {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('zh-CN', { hour12: false })
}

function setDrafts(items) {
  drafts.value = Object.fromEntries(
    items.map((item) => [
      item.id,
      {
        status: item.status || 'pending',
        admin_note: item.admin_note || ''
      }
    ])
  )
}

function hasChanges(application) {
  const draft = drafts.value[application.id]
  if (!draft) return false
  return (
    draft.status !== (application.status || 'pending') ||
    (draft.admin_note || '') !== (application.admin_note || '')
  )
}

async function loadApplications() {
  loading.value = true
  errorMessage.value = ''

  try {
    const data = await api.getApplications(activeFilter.value)
    applications.value = data
    setDrafts(data)
  } catch (error) {
    errorMessage.value = error.message || '报名记录加载失败'
  } finally {
    loading.value = false
  }
}

async function saveApplication(application) {
  savingId.value = application.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const result = await api.updateApplication(application.id, drafts.value[application.id])
    const nextItem = result.application
    const index = applications.value.findIndex((item) => item.id === application.id)

    if (activeFilter.value !== 'all' && nextItem.status !== activeFilter.value) {
      applications.value = applications.value.filter((item) => item.id !== application.id)
    } else if (index >= 0) {
      applications.value[index] = nextItem
    }
    drafts.value[application.id] = {
      status: nextItem.status || 'pending',
      admin_note: nextItem.admin_note || ''
    }
    successMessage.value = '报名记录已更新'
  } catch (error) {
    errorMessage.value = error.message || '保存失败'
  } finally {
    savingId.value = null
  }
}

watch(activeFilter, () => {
  loadApplications()
})

onMounted(() => {
  loadApplications()
})
</script>

<style scoped>
.applications-manager {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-btn,
.refresh-btn,
.save-btn {
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn,
.refresh-btn {
  padding: 10px 14px;
  font-size: 13px;
}

.filter-btn.active {
  background: rgba(121, 168, 255, 0.18);
  border-color: rgba(121, 168, 255, 0.4);
  color: var(--primary);
}

.refresh-btn:hover,
.filter-btn:hover,
.save-btn:hover:not(:disabled) {
  border-color: rgba(121, 168, 255, 0.4);
}

.panel-message {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
}

.panel-message.success {
  background: rgba(70, 190, 120, 0.15);
  border: 1px solid rgba(70, 190, 120, 0.3);
  color: #8df2b2;
}

.panel-message.error {
  background: rgba(255, 100, 100, 0.15);
  border: 1px solid rgba(255, 100, 100, 0.3);
  color: #ff8d8d;
}

.empty-state {
  min-height: 240px;
  display: grid;
  place-items: center;
  border: 1px dashed var(--panel-border);
  border-radius: 16px;
  color: var(--muted);
}

.application-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.application-card {
  padding: 22px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.card-header h3 {
  margin: 0 0 6px;
  font-size: 20px;
}

.card-header p {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
}

.status-badge {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status-pending {
  background: rgba(255, 180, 50, 0.15);
  color: #ffcf70;
}

.status-reviewing {
  background: rgba(121, 168, 255, 0.15);
  color: var(--primary);
}

.status-processed {
  background: rgba(70, 190, 120, 0.15);
  color: #8df2b2;
}

.status-archived {
  background: rgba(170, 170, 170, 0.15);
  color: #d5d7de;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 16px;
}

.meta-grid div,
.content-block {
  min-width: 0;
}

.meta-grid span,
.content-block span,
.form-group span {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--muted);
}

.meta-grid strong,
.content-block p {
  display: block;
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
}

.links-row {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.links-row a {
  color: var(--primary);
  text-decoration: none;
}

.muted-text {
  color: var(--muted);
  font-size: 14px;
}

.warning-block {
  padding: 14px 16px;
  border-radius: 12px;
  background: rgba(255, 180, 50, 0.08);
  border: 1px solid rgba(255, 180, 50, 0.18);
}

.editor-grid {
  display: grid;
  grid-template-columns: minmax(0, 220px) minmax(0, 1fr);
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group-wide {
  min-width: 0;
}

.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.28);
  color: var(--text);
  font-size: 14px;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
}

.save-btn {
  padding: 12px 18px;
  background: linear-gradient(135deg, var(--primary), var(--primary-strong));
  border: none;
  color: #03111f;
  font-weight: 600;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 760px) {
  .meta-grid,
  .editor-grid {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
  }

  .card-actions {
    justify-content: stretch;
  }

  .save-btn {
    width: 100%;
  }
}
</style>
