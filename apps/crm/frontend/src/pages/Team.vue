<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Team" />
      </template>
      <template #right-header>
        <Button
          :label="__('Invite Member')"
          @click="showInviteModal = true"
        >
          <template #prefix>
            <FeatherIcon name="user-plus" class="size-4" />
          </template>
        </Button>
      </template>
    </LayoutHeader>

    <div class="flex-1 overflow-auto p-6 glass-scrollbar">
      <div v-if="teamMembers.loading" class="flex items-center justify-center h-64">
        <LoadingIndicator />
      </div>
      <div v-else-if="teamMembers.data && teamMembers.data.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <GlassCard
          v-for="member in teamMembers.data"
          :key="member.name"
          hoverable
          class="glass-card"
        >
          <div class="flex flex-col items-center text-center">
            <UserAvatar
              :user="member.name"
              size="lg"
              class="mb-4"
            />
            <h3 class="text-lg font-semibold glass-text mb-2">
              {{ member.full_name || member.name }}
            </h3>
            <p class="text-sm text-ink-gray-5 mb-4">{{ member.email }}</p>
            <div class="flex gap-2">
              <Badge :label="member.role" />
            </div>
          </div>
        </GlassCard>
      </div>
      <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
        <FeatherIcon name="users" class="size-12 text-ink-gray-5 mb-4" />
        <p class="text-ink-gray-5 mb-4">{{ __('No team members yet') }}</p>
        <Button
          :label="__('Invite Your First Member')"
          @click="showInviteModal = true"
        />
      </div>
    </div>

    <GlassModal
      v-model="showInviteModal"
      title="Invite Team Member"
      size="md"
    >
      <InviteUserForm
        @save="handleInviteSave"
        @cancel="showInviteModal = false"
      />
    </GlassModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import GlassCard from '@/components/UI/GlassCard.vue'
import GlassModal from '@/components/UI/GlassModal.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import InviteUserForm from '@/components/Settings/InviteUserPage.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { Button, FeatherIcon, Badge } from 'frappe-ui'

const showInviteModal = ref(false)

const teamMembers = createResource({
  url: 'crm.api.user.get_team_members',
  auto: true,
  transform: (data) => data || []
})

const handleInviteSave = () => {
  showInviteModal.value = false
  teamMembers.reload()
}
</script>
