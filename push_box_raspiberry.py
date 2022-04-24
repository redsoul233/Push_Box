import sys
import os
import PCF8591 as ADC
import pygame

import joystick
from behaviour import *
from game_states import *
from button import Button


class PushBox:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化并创建游戏资源"""
        pygame.init()

        self.screen = pygame.display.set_mode((224, 244))
        pygame.display.set_caption("推箱子")
        self.bg_color = (114, 202, 38)  # 设置背景色
        self.screen.fill(self.bg_color)
        self.back_ground_pic = pygame.image.load('bmp/bgp.bmp')
        self.done_pic = pygame.image.load('bmp/done.gif')
        self.dead_pic = pygame.image.load('bmp/dead.jpg')
        self.trap_pic = pygame.image.load('bmp/trap.jpg')

        pygame.mixer.music.load('music/bgm.mp3')  # 载入背景音乐文件
        pygame.mixer.music.set_volume(0.2)  # 设定背景音乐音量
        pygame.mixer.music.play(loops=-1)  # 播放背景音乐，-1为无限循环播放
        self.push_sound = pygame.mixer.Sound('music/push.wav')  # 载入推箱子声音文件
        self.restart_sound = pygame.mixer.Sound('music/restart.wav')  # 载入推箱子声音文件
        self.done_sound = pygame.mixer.Sound('music/done.wav')  # 载入通关声音文件
        self.dead_sound = pygame.mixer.Sound('music/dead.mp3')  # 载入失败声音文件
        self.finish_sound = pygame.mixer.Sound('music/finish.wav')  # 载入过关音效

        self.states = GameStates()
        # 创建按钮
        self.start_button = Button(self, "start!", 112, 112)
        self.next_button = Button(self, "next", 112, 64)
        self.retry_button = Button(self, "retry", 112, 101)
        self.about_button = Button(self, "about", 25, 224)
        self.help_button = Button(self, "help", 75, 224)
        self.again_button = Button(self, "again", 112, 112)

        self.map = DrawMap(self)

    def _check_event(self, event):
        """检测摇杆"""
        if event == 1 or event == 2 or event == 3 or event == 4:
            if event == 4:
                # 向右移动一格工人
                print(event, 'qian')
                self.map.moveto(self.map.workerx + 1, self.map.workery, self.map.workerx + 2, self.map.workery)
                print(event, 'hou')
            if event == 3:
                print(event, 'qian')
                # 向左移动一格工人
                self.map.moveto(self.map.workerx - 1, self.map.workery, self.map.workerx - 2, self.map.workery)
                print(event, 'hou')
            if event == 2:
                # 向下移动一格工人
                print(event, 'qian')
                self.map.moveto(self.map.workerx, self.map.workery + 1, self.map.workerx, self.map.workery + 2)
                print(event, 'hou')
            if event == 1:
                # 向上移动一格工人
                print(event, 'qian')
                self.map.moveto(self.map.workerx, self.map.workery - 1, self.map.workerx, self.map.workery - 2)
                print(event, 'hou')

        print(event)
        self.push_sound.play()

    def _check_events(self):
        """检测鼠标及键盘按键"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.states.game_active == "STARTED":
                if event.key == pygame.K_RIGHT:
                    # 向右移动一格工人
                    self.map.moveto(self.map.workerx + 1, self.map.workery, self.map.workerx + 2, self.map.workery)
                if event.key == pygame.K_LEFT:
                    # 向左移动一格工人
                    self.map.moveto(self.map.workerx - 1, self.map.workery, self.map.workerx - 2, self.map.workery)
                if event.key == pygame.K_DOWN:
                    # 向下移动一格工人
                    self.map.moveto(self.map.workerx, self.map.workery + 1, self.map.workerx, self.map.workery + 2)
                if event.key == pygame.K_UP:
                    # 向上移动一格工人
                    self.map.moveto(self.map.workerx, self.map.workery - 1, self.map.workerx, self.map.workery - 2)
                if event.key == pygame.K_SPACE:
                    if self.states.level == 3:
                        self.states.time_left = TIMELEFT
                        self.states.nowtick = pygame.time.get_ticks()
                        self.states.lasttick = pygame.time.get_ticks()
                    # 重置地图
                    self.map.initmap()
                    self.restart_sound.play()
                self.push_sound.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pot = pygame.mouse.get_pos()
                # 按到下一关
                if self.next_button.rect.collidepoint(mouse_pot) and self.states.game_active == "FINISH":
                    self.states.game_active = "STARTED"  # 切换程序状态
                    self.states.level += 1  # 关卡数加一
                    # 重新设置第三关计时器
                    if self.states.level == 3:
                        self.states.time_left = TIMELEFT
                        self.states.nowtick = pygame.time.get_ticks()
                        self.states.lasttick = pygame.time.get_ticks()
                    readmap(map, self.states.level)
                    self.map.initmap()
                # 按到再试一次
                if self.retry_button.rect.collidepoint(mouse_pot) and (
                        self.states.game_active == "FINISH" or self.states.game_active == "DEAD" or self.states.game_active == "TRAP"):
                    self.states.game_active = "STARTED"  # 切换程序状态
                    # 重新设置第三关计时器
                    if self.states.level == 3:
                        self.states.time_left = TIMELEFT
                        self.states.nowtick = pygame.time.get_ticks()
                        self.states.lasttick = pygame.time.get_ticks()
                    self.map.initmap()
                # 按到关于
                if self.about_button.rect.collidepoint(mouse_pot):
                    os.startfile(r"mousepad .//explanation//about.txt")
                # 按到帮助
                if self.help_button.rect.collidepoint(mouse_pot):
                    os.system(r"mousepad .//explanation//help.txt")
                # 按到开始
                if self.start_button.rect.collidepoint(mouse_pot) and self.states.game_active == "NOT_START":
                    self.states.game_active = "STARTED"
                # 按到从头再来
                if self.again_button.rect.collidepoint(mouse_pot) and self.states.game_active == "DONE":
                    self.states.game_active = "NOT_START"

    def _check_finish(self):
        """检测是否完成本关"""
        for i in range(0, 7):  # 0--6
            for j in range(0, 7):  # 0--6
                if self.map.mapnow[i][j] == destination or self.map.mapnow[i][j] == man_in_des:
                    return False
        return True

    def prep_time(self):
        """显示倒计时"""
        time_str = str(self.states.time_left)
        font = pygame.font.SysFont(None, 24)
        time_image = font.render("time left: " + time_str, True, (0, 0, 0), (151, 113, 74))
        time_rect = time_image.get_rect()
        time_rect.x, time_rect.y = 0, 0
        self.screen.blit(time_image, time_rect)

    def run_game(self):
        """start game"""
        last_state = 0
        js_msg = ['home', 'up', 'down', 'left', 'right', 'pressed']
        while True:
            if self.states.game_active == "NOT_START":
                self._check_events()
                self.screen.fill(self.bg_color)
                self.screen.blit(self.back_ground_pic, self.back_ground_pic.get_rect())
                self.start_button.draw_button()

            elif self.states.game_active == "STARTED":
                # 响应摇杆与按键
                state = joystick.detect_js()
                if state != last_state:
                    print(js_msg[state])
                    self._check_event(state)
                    last_state = state
                joystick.time.sleep(0.01)
                self._check_events()
                # 绘制屏幕
                self.screen.fill(self.bg_color)
                self.map.renewmap()
                if self.states.level == 3:
                    self.states.nowtick = pygame.time.get_ticks()
                    if (self.states.nowtick - self.states.lasttick) // 1000 == 1:
                        self.states.time_left -= 1
                        self.states.lasttick = self.states.nowtick
                    self.prep_time()  # 显示倒计时
                    if self.states.time_left == 0:
                        self.states.game_active = "DEAD"
                        self.states.time_left = TIMELEFT
                        self.dead_sound.play()
                # 检查是否完成，如果完成显示下一关
                if self._check_finish():
                    if self.states.level != 5:
                        self.states.game_active = "FINISH"
                        self.finish_sound.play()
                    else:
                        self.states.game_active = "DONE"
                        self.done_sound.play()

            elif self.states.game_active == "FINISH":
                # 检测按键是否按到
                self._check_events()
                self.screen.fill(self.bg_color)
                self.map.renewmap()
                self.retry_button.draw_button()
                self.next_button.draw_button()

            elif self.states.game_active == "DONE":
                self._check_events()
                self.screen.fill(self.bg_color)
                self.screen.blit(self.done_pic, self.done_pic.get_rect())
                self.again_button.draw_button()

            elif self.states.game_active == "DEAD":
                self._check_events()
                self.screen.fill(self.bg_color)
                self.screen.blit(self.dead_pic, self.dead_pic.get_rect())
                self.retry_button.draw_button()

            elif self.states.game_active == "TRAP":
                self._check_events()
                self.screen.fill(self.bg_color)
                self.screen.blit(self.trap_pic, self.trap_pic.get_rect())
                self.retry_button.draw_button()

            self.about_button.draw_button()
            self.help_button.draw_button()
            pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行
    ADC.setup(0x48)
    ai = PushBox()
    ai.run_game()
