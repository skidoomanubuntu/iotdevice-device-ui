<template>
  <div id="app">
    <app-header />
    <div>
      <h1>Skidooman</h1>
      <div class="progress">
        <h1>Battery Level</h1>
        <ve-progress :progress="battery_level" />
      </div>
    </div>
    <div>
      <vue-final-modal
        v-model="showModal"
        classes="modal-container"
        content-class="modal-content"
      >
        <span class="modal__title">Internal System Error Detected</span>
        <div class="modal__content">
          <p>
            Batter Level can not be more 100%! Please wait while the software
            reverts to the last known good state
          </p>
        </div>
      </vue-final-modal>
    </div>
  </div>
</template>
i
<script>
import AppHeader from './components/AppHeader.vue';
import axios from 'axios';
import { VueEllipseProgress } from 'vue-ellipse-progress';

export default {
  name: 'App',
  components: {
    AppHeader,
    VueEllipseProgress,
  },
  data() {
    return {
      max_allowed_battery_level: 100,
      polling_battery_level: null,
      battery_level: 0,
      polling_refresh: null,
      showModal: false,
    };
  },
  created() {
    this.loadData();
    this.pollBattery();
    this.pollUpdate();
  },
  methods: {
    pollBattery() {
      this.polling_battery_level = setInterval(() => {
        this.loadData();
      }, 1000);
    },
    pollUpdate() {
      this.polling_refresh = setInterval(() => {
        this.refresh();
      }, 45000);
    },
    async loadData() {
      const res = await axios.get('http://localhost:4040/battery-level');
      this.battery_level = res.data.battery;
      if (this.battery_level > this.max_allowed_battery_level) {
        this.showModal = true;
        await this.revert();
        const res = await axios.get('http://localhost:4040/battery-level');
        this.battery_level = res.data.battery;
      }

      if (this.battery_level <= this.max_allowed_battery_level) {
        this.showModal = false;
      }
    },
    async refresh() {
      const res = await axios.post('http://localhost:4500/refresh');
      console.log(JSON.stringify(res));
    },
    async revert() {
      const res = await axios.post('http://localhost:4500/revert', {
        name: 'iotdevice-device-controller',
      });
      console.log(JSON.stringify(res));
    },
  },
  beforeDestroy() {
    clearInterval(this.polling_speed);
    clearInterval(this.polling_refresh);
  },
};
</script>

<style lang="scss">
h1 {
  font-family: 'RobotoNormal';
  font-weight: 100;
  font-size: 38px;
  text-align: center;
  letter-spacing: 3px;
  padding-top: 3px;
}

.progress {
  margin: auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}

body {
  background: white;
}
</style>

<style scoped>
:deep(.modal-container) {
  display: flex;
  justify-content: center;
  align-items: center;
}
:deep(.modal-content) {
  display: flex;
  flex-direction: column;
  margin: 0 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  background: #fff;
}
.modal__title {
  font-size: 1.5rem;
  font-weight: 700;
}
</style>
