<template>
  <div :class="$style['ops-chat-container']">
    <div
      v-if="!headlessModeId"
      :class="[
        $style['ops-rooms-wrapper'],
        { [$style['ops-rooms-wrapper__show-rooms']]: !showRoomsList },
        { [$style['show-block']]: getMobileVisible },
      ]"
    >
      <!-- Room search box -->
      <div :class="$style['ops-rooms-wrapper__search-box']">
        <OInput v-model="searchQuery" placeholder="Search...">
          <template #prefix>
            <img
              :class="$style['ops-rooms-wrapper__search-icon']"
              :src="getImageUrl('assets/icons/search.svg')"
              alt="search-icon"
            />
          </template>
        </OInput>
        <button v-if="0" :class="$style['ops-rooms-wrapper__add-room']">
          <img
            width="30"
            :src="getImageUrl('assets/icons/create-room.svg')"
            alt="add"
          />
        </button>
      </div>

      <!-- List of filtered rooms -->
      <RoomsList
        v-if="websocketService.rooms.value.length"
        :rooms="filteredRooms"
        :selected-room="selectedRoom"
        :first-participant="getFirstUnParticipant"
      />
    </div>

    <!--    Current room-->
    <div :class="$style['ops-chat-room']">
      <Room
        v-if="selectedRoom?.id || headlessModeId"
        :class="{ [$style['show-block']]: !getMobileVisible }"
        :show-rooms-list="showRoomsList"
        :room-id="selectedRoom?.id || headlessModeId"
        @toggle-rooms-list="toggleRoomsList"
      />
      <RoomNoMessages v-else text="Please select room" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import OInput from "@/components/ui/OInput.vue";
import RoomsList from "@/components/rooms/RoomsList.vue";
import Room from "@/components/room/Room.vue";
import { IRoom } from "@/types/rooms.types";
import { getImageUrl } from "@/helpers/import-image";
import { useMainStore } from "@/store/useMainStore";
import chatService from "@/services/chat/chat";
import websocketService from "@/services/chat/websocket-chat";
import RoomNoMessages from "@/components/room/content/RoomNoMessages.vue";

const mainStore = useMainStore();

const searchQuery = ref("");
const showRoomsList = ref(true);
const getMobileVisible = computed(() => mainStore.isMobileVisible);
const selectedRoom = computed(() => websocketService.selectedRoom.value);
const headlessModeId = computed(() => websocketService.headlessModeId.value);
const filteredRooms = computed(() => {
  const query = searchQuery.value.toLowerCase();
  if (!query) {
    return totalRooms.value;
  }
  return totalRooms.value?.filter((chat: IRoom) => {
    return chat.name.toLowerCase().includes(query);
  });
});

const toggleRoomsList = () => (showRoomsList.value = !showRoomsList.value);

const loadRooms = async () => {
  websocketService.rooms.value = await chatService.fetchConversations();
};

const totalRooms = computed(() => {
  return [
    ...websocketService.rooms.value
      .filter((el) => el.is_person_participant)
      .sort((a) => (a.unread_messages > 0 ? -1 : 1))
      .sort(
        (a, b) =>
          new Date(b.last_message?.timestamp).getTime() -
          new Date(a.last_message?.timestamp).getTime()
      ),
    ...websocketService.rooms.value
      .filter((el) => !el.is_person_participant)
      .sort((a) => (a.unread_messages > 0 ? -1 : 1))
      .sort(
        (a, b) =>
          new Date(b.last_message?.timestamp).getTime() -
          new Date(a.last_message?.timestamp).getTime()
      ),
  ];
});

const getFirstUnParticipant = computed(() =>
  totalRooms.value.find((el) => !el.is_person_participant)
);

onMounted(() => {
  if (!headlessModeId.value) {
    loadRooms();
  }
});
</script>

<style lang="scss" module>
.ops-chat-container {
  @apply flex h-[calc(100vh-6rem)];

  .ops-rooms-wrapper {
    @apply bg-white flex flex-col transition-all duration-1000 overflow-hidden relative grow-0 shrink-0 md:basis-3/12 min-w-[16.25rem] w-full md:max-w-[31.25rem] p-4 h-full md:border-grey-100 md:border-r-[1px];

    &__search-box {
      @apply flex items-center w-full;
    }

    &__search-icon {
      @apply mr-1;
      filter: invert(45%) sepia(8%) saturate(778%) hue-rotate(182deg)
        brightness(94%) contrast(80%);
    }

    &__add-room {
      @apply ml-3 rounded-full;

      img {
        @apply transition-all duration-500;

        &:hover {
          @apply scale-110 opacity-70;
        }
      }
    }

    &__show-rooms {
      @apply w-0 min-w-0 basis-0 px-0 #{!important};
    }
  }

  .ops-chat-room {
    @apply h-full w-full relative bg-grey-50;
  }
}

.show-block {
  @apply hidden md:flex #{!important};
}
</style>
