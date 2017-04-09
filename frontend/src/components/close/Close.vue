<template lang="html">
  <div class="close" @click="close"></div>
</template>

<script>
import EventHub from '@/EventHub'

export default {
  name: 'close',
  methods: {
    close () {
      EventHub.$emit('close-dialog')
      EventHub.$emit('close-dialog-plan')
    }
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.close
  width: 22px
  height: 22px
  background-size: 22px 22px
  background-repeat: no-repeat
  background-image: url('./close.png')
  &:hover
    cursor: pointer
</style>
