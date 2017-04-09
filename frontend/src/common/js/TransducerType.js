export const type = [
  {
    type: 'button-gpio',
    name: '按钮',
    functions: [
      { function_name: 'on', tip: '按下', argsTip: '无', args: 'push' }
    ]
  },
  {
    type: 'sound-01',
    name: '声音传感器',
    functions: [
      { function_name: 'on', tip: '检测声音', argsTip: '无', args: 'sound' }
    ]
  },
  { type: 'dht11',
    name: '温湿度传感器',
    functions: [
      { function_name: 'getTemperature', tip: '温度', argsTip: '>30' },
      { function_name: 'getRelativeHumidity', tip: '湿度', argsTip: '>30' }
    ]
  },
  {
    type: 'gy-30',
    name: '光照传感器',
    functions: [
      { function_name: 'getIlluminance', tip: '光照值', argsTip: '>30' }
    ]
  },
  {
    type: 'time',
    name: '时间传感器',
    functions: [
      { function_name: 'time', tip: '设置时间', argsTip: '12:00-13:00' }
    ]
  }
]

export default 'transducer'
