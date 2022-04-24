import PCF8591 as ADC
import time

js_msg = ['home','up','down','left','right','pressed']  # 状态

def detect_js():
    state=0
    if ADC.read(0) <= 30 and 30<ADC.read(1)<225:  state = 1	# up方向
    if ADC.read(0) >= 225 and 30<ADC.read(1)<225: state = 2	# down方向
    if ADC.read(1) <= 30 and 30<ADC.read(0)<225:  state = 4	# right方向
    if ADC.read(1) >= 205 and 30<ADC.read(0)<225: state = 3	# left方向
    if ADC.read(2) == 0:   state = 5	# Button按下
    if ADC.read(0)<140 and ADC.read(0)>110 and ADC.read(1) <140\
	   and ADC.read(1)>110 and ADC.read(2) <1: state = 0	#复位
    return state   # 返回状态

def loop():
    state=last_state=0
    while True:
        state = detect_js()   	 # 调用状态监测函数
        if state != last_state:  # 判断状态是否发生改变
            print(js_msg[state]) # 打印
            print(ADC.read(0))
            last_state = state   # 保存以防止同一状态多次打印
        time.sleep(0.01)		 # sleep函数可以带小数参数

def destroy(): # 异常处理函数
    pass

if __name__ == '__main__':
	ADC.setup(0x48)  # 设置PCF8591模块地址
	try:
		loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时
		destroy()   # 调用析构函数
