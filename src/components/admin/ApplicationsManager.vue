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

      <div class="toolbar-right">
        <span class="auto-refresh-hint">无未保存修改时每 8 秒与飞书同步</span>
        <button type="button" class="refresh-btn" @click="loadApplications" :disabled="loading">
          {{ loading ? '刷新中...' : '刷新列表' }}
        </button>
      </div>
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
            {{ statusLabel(application) }}
          </span>
        </div>

        <div class="meta-grid">
          <div><span>学号</span><strong>{{ application.student_id }}</strong></div>
          <div><span>专业</span><strong>{{ application.grade_major }}</strong></div>
          <div><span>手机号</span><strong>{{ application.phone }}</strong></div>
          <div><span>邮箱</span><strong>{{ application.email }}</strong></div>
          <div><span>飞书渠道</span><strong>{{ feishuModeLabel(application) }}</strong></div>
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

        <div v-if="application.last_email_type" class="content-block">
          <span>最近邮件</span>
          <p>
            {{ application.last_email_type }}
            ·
            {{ application.last_email_sent ? '已发送' : (application.last_email_error || '发送失败') }}
          </p>
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

          <label class="form-group form-group-wide">
            <span>考核群信息</span>
            <textarea
              v-model.trim="drafts[application.id].review_group_info"
              rows="3"
              placeholder="通过时会写入结果邮件和飞书状态通知"
            ></textarea>
          </label>

          <label class="form-group form-group-wide">
            <span>邮件附加链接</span>
            <textarea
              v-model.trim="drafts[application.id].result_email_links"
              rows="3"
              placeholder="每行一个链接，例如：https://example.com"
            ></textarea>
          </label>

          <label class="form-group form-group-wide">
            <span>邮件图片 URL</span>
            <textarea
              v-model.trim="drafts[application.id].result_email_image_url"
              rows="2"
              placeholder="例如：https://example.com/qrcode.png"
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
          <button
            type="button"
            class="danger-btn"
            :disabled="savingId === application.id"
            @click="deleteApplication(application)"
          >
            删除
          </button>
          <button
            v-if="canReviewWorkflow(application)"
            type="button"
            class="ghost-btn"
            :disabled="savingId === application.id"
            @click="applyAction(application, 'reviewing')"
          >
            标记处理中
          </button>
          <button
            v-if="canReviewWorkflow(application)"
            type="button"
            class="save-btn"
            :disabled="savingId === application.id"
            @click="applyAction(application, 'approve')"
          >
            通过并发邮件
          </button>
          <button
            v-if="canReviewWorkflow(application)"
            type="button"
            class="danger-btn"
            :disabled="savingId === application.id"
            @click="applyAction(application, 'reject')"
          >
            拒绝并发邮件
          </button>
          <button
            v-if="canArchive(application)"
            type="button"
            class="ghost-btn"
            :disabled="savingId === application.id"
            @click="applyAction(application, 'archive')"
          >
            归档录用
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { api } from '../../services/api.js'

const POLL_MS = 8000
let pollTimer = null

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

function statusLabel(application) {
  const draft = drafts.value[application.id]
  const s = draft?.status || application.status || 'pending'
  if (s === 'processed') {
    if (application.result_type === 'approved') return '已处理 · 已通过'
    if (application.result_type === 'rejected') return '已处理 · 已拒绝'
    return '已处理'
  }
  if (s === 'archived') return '已归档'
  if (s === 'reviewing') return '处理中'
  return '待处理'
}

function feishuModeLabel(application) {
  const m = application.feishu_delivery_mode
  if (m === 'app') return '应用机器人'
  if (m === 'webhook') return 'Webhook'
  return '—'
}

function canReviewWorkflow(application) {
  const s = application.status
  return s === 'pending' || s === 'reviewing'
}

function canArchive(application) {
  return application.status === 'processed' && application.result_type === 'approved'
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
        admin_note: item.admin_note || '',
        review_group_info: item.review_group_info || '',
        result_email_links: item.result_email_links || '',
        result_email_image_url: item.result_email_image_url || ''
      }
    ])
  )
}

function hasChanges(application) {
  const draft = drafts.value[application.id]
  if (!draft) return false
  return (
    draft.status !== (application.status || 'pending') ||
    (draft.admin_note || '') !== (application.admin_note || '') ||
    (draft.review_group_info || '') !== (application.review_group_info || '') ||
    (draft.result_email_links || '') !== (application.result_email_links || '') ||
    (draft.result_email_image_url || '') !== (application.result_email_image_url || '')
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
      admin_note: nextItem.admin_note || '',
      review_group_info: nextItem.review_group_info || '',
      result_email_links: nextItem.result_email_links || '',
      result_email_image_url: nextItem.result_email_image_url || ''
    }
    successMessage.value = '报名记录已更新'
  } catch (error) {
    errorMessage.value = error.message || '保存失败'
  } finally {
    savingId.value = null
  }
}

async function applyAction(application, action) {
  savingId.value = application.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const result = await api.updateApplication(application.id, {
      action,
      admin_note: drafts.value[application.id].admin_note,
      review_group_info: drafts.value[application.id].review_group_info,
      result_email_links: drafts.value[application.id].result_email_links,
      result_email_image_url: drafts.value[application.id].result_email_image_url
    })
    const nextItem = result.application
    const index = applications.value.findIndex((item) => item.id === application.id)

    if (activeFilter.value !== 'all' && nextItem.status !== activeFilter.value) {
      applications.value = applications.value.filter((item) => item.id !== application.id)
    } else if (index >= 0) {
      applications.value[index] = nextItem
    }

    drafts.value[application.id] = {
      status: nextItem.status || 'pending',
      admin_note: nextItem.admin_note || '',
      review_group_info: nextItem.review_group_info || '',
      result_email_links: nextItem.result_email_links || '',
      result_email_image_url: nextItem.result_email_image_url || ''
    }

    const warnings = [result.email_warning, result.feishu_warning].filter(Boolean)
    successMessage.value = warnings.length
      ? `处理完成，但存在提醒：${warnings.join('；')}`
      : '报名流程已更新'
  } catch (error) {
    errorMessage.value = error.message || '处理失败'
  } finally {
    savingId.value = null
  }
}

async function deleteApplication(application) {
  const hint = hasChanges(application) ? '（当前有未保存修改，删除后将丢失）' : ''
  const ok = typeof window !== 'undefined'
    ? window.confirm(`确认删除报名记录「${application.name}」${hint}？此操作不可恢复。`)
    : true
  if (!ok) return

  savingId.value = application.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await api.deleteApplication(application.id)
    applications.value = applications.value.filter((item) => item.id !== application.id)
    const nextDrafts = { ...drafts.value }
    delete nextDrafts[application.id]
    drafts.value = nextDrafts
    successMessage.value = '报名记录已删除'
  } catch (error) {
    errorMessage.value = error.message || '删除失败'
  } finally {
    savingId.value = null
  }
}

watch(activeFilter, () => {
  loadApplications()
})

async function silentRefresh() {
  if (typeof document !== 'undefined' && document.visibilityState !== 'visible') return
  if (savingId.value || loading.value) return
  if (applications.value.some((a) => hasChanges(a))) return
  try {
    const data = await api.getApplications(activeFilter.value)
    applications.value = data
    setDrafts(data)
  } catch {
    /* 静默失败，避免打断管理员操作 */
  }
}

onMounted(() => {
  loadApplications()
  pollTimer = setInterval(silentRefresh, POLL_MS)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
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

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.auto-refresh-hint {
  font-size: 12px;
  color: var(--muted);
  max-width: 220px;
  line-height: 1.4;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-btn,
.refresh-btn,
.save-btn,
.ghost-btn,
.danger-btn {
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
.save-btn:hover:not(:disabled),
.ghost-btn:hover:not(:disabled),
.danger-btn:hover:not(:disabled) {
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
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 12px;
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

.ghost-btn,
.danger-btn {
  padding: 12px 18px;
}

.ghost-btn {
  color: var(--text);
}

.danger-btn {
  background: rgba(255, 100, 100, 0.12);
  border-color: rgba(255, 100, 100, 0.22);
  color: #ffd3d3;
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

  .save-btn,
  .ghost-btn,
  .danger-btn {
    width: 100%;
  }
}
</style>
