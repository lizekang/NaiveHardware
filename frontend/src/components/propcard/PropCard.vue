<template lang="html">
  <div class="card">
    <h1 class="title">参数设置</h1>
    <div class="name">
      <h2 class="id">ID</h2>
      <input class="id_input" type="text" :placeholder="id ? id : selectedDevice.name" v-model="id" />
    </div>
    <div class="props">
      <ul>
        <li v-for="prop in functions" class="prop">
          <div class="left_wrapper">
            <h2 class="key">功能</h2>
            <input class="value" type="text" :placeholder="prop.tip" readonly="true" />
          </div>
          <div class="right_wrapper">
            <h2 class="key">参数</h2>
            <input class="value" type="text" :placeholder="prop.argsTip" v-model="prop.args" :readonly="prop.readOnly" />
          </div>
        </li>
      </ul>
    </div>
    <div class="button" @click="setProps">
      确认
    </div>
    <div class="close-wrapper">
      <v-close></v-close>
    </div>
  </div>
</template>

<script>
import Close from 'components/close/Close'

export default {
  name: 'propcard',
  props: {
    selectedDevice: Object,
    selectedIndex: Number,
    plans: {
      type: Array,
      default () {
        return []
      }
    },
    transducers: Array,
    effectors: Array
  },
  data () {
    return {
      id: this.selectedDevice.id ? this.selectedDevice.id : '',
      functions: []
    }
  },
  methods: {
    setProps () {
      if (!this._deviceIdRepeat(this.id)) {
        this.$emit('setPropFunc', this.id, this.functions)
      } else {
        alert('id重复')
      }
    },
    _deviceIdRepeat (id) {
      let result = false

      this.plans.forEach(plan => {
        let transducers = plan.transducers
        let effectors = plan.effectors

        transducers.forEach(device => {
          if (id === device.id) {
            result = true
          }
        })

        effectors.forEach((device, index) => {
          if (id === device.id) {
            result = true
          }
        })
      })

      this.transducers.forEach((device, index) => {
        if (id === device.id && index !== this.selectedIndex) {
          result = true
        }
      })

      this.effectors.forEach((device, index) => {
        if (id === device.id && index !== this.selectedIndex) {
          result = true
        }
      })

      return result
    }
  },
  created () {
    this.selectedDevice.functions.forEach(item => {
      let prop = {
        function_name: item.function_name,
        tip: item.tip,
        argsTip: item.argsTip,
        args: item.args ? item.args : '',
        readOnly: item.function_name === 'on' || item.function_name === 'turnOn'
      }

      this.functions.push(prop)
    })
  },
  components: {
    'v-close': Close
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.card
  padding: 54px 55px 54px
  border-radius: 2px
  background-color: #fff
  position: relative
  .title
    font-size: 36px
    color: #60c5ba
    text-align: center
  .name
    margin-top: 30px
    .id
      font-size: 18px
      color: #60c5ba
      margin-bottom: 9px
    .id_input
      padding: 19px 0 19px 19px
      box-sizing: border-box
      width: 100%
      border-radius: 2px
      font-size: 14px
      color: #8b8687
      background-color: #e3dede
      outline: none
  .props
    .prop
      margin-top: 17px
      font-size: 0
      .left_wrapper, .right_wrapper
        display: inline-block
        width: 50%
        box-sizing: border-box
        .key
          font-size: 18px
          color: #60c5ba
          margin-bottom: 7px
        .value
          padding: 19px 0 19px 19px
          box-sizing: border-box
          width: 100%
          border-radius: 2px
          font-size: 14px
          color: #8b8687
          background-color: #e3dede
          outline: none
      .left_wrapper
        padding-right: 5%
      .right_wrapper
        padding-left: 5%
  .button
    margin-top: 42px
    width: 100%
    height: 50px
    line-height: 50px
    font-size: 14px
    color: #fff
    background-color: #47b8e0
    border-radius: 2px
    text-align: center
    &:hover
      cursor: pointer
  .close-wrapper
    position: absolute
    top: 12px
    right: 14px
</style>
