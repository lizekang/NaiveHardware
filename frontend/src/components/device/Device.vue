<template lang="html">
  <div class="device">
    <div class="img-wrapper" :class="[classMap[device.type], { selected }]"></div>
    <div class="text" v-if="device.type !== 'add'">
      {{ device.name }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'device',
  props: {
    device: Object,
    selected: Boolean
  },
  data () {
    return {
      id: this.device.id,
      functions: this.device.functions
    }
  },
  created () {
    this.classMap = {
      // 效应器
      'buzzer-gpio': 'bee',
      'ky-016': 'kaiguan',
      'ruff-v1-infrared-sender': 'hongwaifa',
      'lcd1602-pcf8574a-hd44780': 'program',
      'relay-1c': 'relay',
      // 传感器
      'button-gpio': 'button',
      'sound-01': 'mic',
      'dht11': 'shidu',
      'gy-30': 'hongwaishou',
      'time': 'clock',

      'add': 'add'
    }
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
@import '../../common/stylus/mixin'

.device
  .img-wrapper
    width: 80px
    height: 80px
    border-radius: 50%
    background-size: 80px 80px
    background-repeat: no-repeat
    &.selected
      box-shadow: 0 0 20px 2px #a1a1a1
    &.add
      bg-image('add')
      box-shadow: 0 0 20px 0 #a1a1a1
    &.bee
      bg-image('bee')
    &.button
      bg-image('button')
    &.hongwaifa
      bg-image('hongwaifa')
    &.hongwaishou
      bg-image('hongwaishou')
    &.kaiguan
      bg-image('kaiguan')
    &.mic
      bg-image('mic')
    &.netin
      bg-image('netin')
    &.netout
      bg-image('netout')
    &.program
      bg-image('program')
    &.shidu
      bg-image('shidu')
    &.wendu
      bg-image('wendu')
    &.clock
      bg-image('clock')
    &.relay
      bg-image('relay')
  .text
    margin-top: 2px
    font-size: 10px
    color: #657d87
    text-align: center
</style>
