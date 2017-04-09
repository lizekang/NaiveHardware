export const type = [
  {
    type: 'buzzer-gpio',
    name: '蜂鸣器',
    functions: [
      { function_name: 'turnOn', tip: '打开', argsTip: '无', args: '' }
    ]
  }, {
    type: 'ky-016',
    name: 'LED灯',
    functions: [
      { function_name: 'turnOn', tip: '发光', argsTip: '无', args: '' }
      // { function_name: 'setRGB', tip: '设定颜色值', argsTip: '255,255,255' }
    ]
  },
  { type: 'ruff-v1-infrared-sender', name: '红外发射器', functions: [] },
  { type: 'lcd1602-pcf8574a-hd44780', name: '显示器', functions: [] },
  {
    type: 'relay-1c',
    name: '继电器',
    functions: [
      { function_name: 'turnOn', tip: '接通', argsTip: '无', args: '' }
    ]
  }
]

export default 'effector'
