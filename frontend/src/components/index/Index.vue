<template lang="html">
  <div class="index">
    <div class="banner-wrapper">
      <img src="./banner.png" />
    </div>
    <div class="feature-wrapper">
      <img src="./icon1.png" />
      <img class="compatible" src="./icon2.png" />
      <img src="./icon3.png" />
    </div>
    <div class="desc-wrapper">
      <img class="desc" src="./desc.png" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'index'
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.index
  background-color: #f4f4f4
  padding-bottom: 79px
  padding-top: 22px
  .banner-wrapper
    position: relative
    width: 100%
    height: 0
    padding-top: 26%
    & > img
      position: absolute
      top: 0
      left: 0
      width: 100%
      height: 100%
  .feature-wrapper
    height: 321px
    box-sizing: border-box
    padding-top: 47px
    text-align: center
    .compatible
      margin: 0 154px
  .desc-wrapper
    position: relative
    width: 100%
    height: 0
    padding-top: 32%
    .desc
      position: absolute
      width: 100%
      height: 100%
      top: 0
      left: 0
</style>
