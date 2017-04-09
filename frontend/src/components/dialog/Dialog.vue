<template lang="html">
  <transition name="fade">
    <div class="choose">
      <div class="choose-wrapper" v-if="cardType === 0">
        <v-choose-card :type="type"></v-choose-card>
      </div>
      <div class="prop-wrapper" v-if="cardType === 1">
        <v-prop-card :selectedDevice="selectedDevice" :selectedIndex="selectedIndex" @setPropFunc="setPropFunc" :plans="plans" :transducers="transducers" :effectors="effectors"></v-prop-card>
      </div>
      <div class="delete-wrapper" v-if="cardType === 2">
        <v-delete-card :plan="plan" :deleteType="deleteType" :deleteName="deleteName" :deleteFunc="deleteFunc"></v-delete-card>
      </div>
      <div class="deploy-wrapper" v-if="cardType === 3">
        <v-deploy-card :plan="plan" :type="type"></v-deploy-card>
      </div>
      <div class="mask" @click="closeDialog"></div>
    </div>
  </transition>
</template>

<script>
import ChooseCard from 'components/choosecard/ChooseCard'
import PropCard from 'components/propcard/PropCard'
import DeleteCard from 'components/deletecard/DeleteCard'
import DeployCard from 'components/deploycard/DeployCard'

import TRANSDUCER from 'common/js/TransducerType'
import EFFECTOR from 'common/js/EffectorType'

const CHOOSE_CARD = 0
const PROP_CARD = 1
const DELETE_CARD = 2
const DEPLOY_CARD = 3

export default {
  name: 'dialog',
  props: {
    type: String,
    deleteName: String,
    deleteFunc: Function,
    selectedDevice: Object,
    selectedIndex: Number,
    setPropFunc: Function,
    plans: Array,
    transducers: Array,
    effectors: Array,
    plan: Object,
    deleteType: String
  },
  methods: {
    closeDialog () {
      this.$emit('closeDialog')
    }
  },
  computed: {
    cardType () {
      if (this.type === TRANSDUCER || this.type === EFFECTOR) {
        return CHOOSE_CARD
      } else if (this.type === 'prop') {
        return PROP_CARD
      } else if (this.type === 'delete') {
        return DELETE_CARD
      } else if (this.type === 'deploy' || this.type === 'undeploy') {
        return DEPLOY_CARD
      }
    }
  },
  components: {
    'v-choose-card': ChooseCard,
    'v-prop-card': PropCard,
    'v-delete-card': DeleteCard,
    'v-deploy-card': DeployCard
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.choose
  position: fixed
  top: 0
  left: 0
  width: 100%
  min-width: 900px
  height: 100%
  z-index: 100
  &.fade-enter-active, &.fade-leave-active
    transition: all 0.3s ease-in
  &.fade-enter, &.fade-leave-to
    opacity: 0
  .mask
    position: absolute
    top: 0
    left: 0
    width: 100%
    height: 100%
    background-color: #f4f4f4
    opacity: 0.6
    z-index: -1
  .choose-wrapper, .prop-wrapper
    width: 30%
    min-width: 480px
    margin: 128px auto 0
  .deploy-wrapper
    width: 480px
    height: 480px
    margin: 128px auto 0
  .delete-wrapper
    width: 25%
    min-width: 380px
    margin: 242px auto 0
</style>
