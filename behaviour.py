from sources import *
import copy


class DrawMap:
    """绘制地图"""

    def __init__(self, ai_game):
        """初始化地图"""
        readmap(map, 1)
        self.mapnow = copy.deepcopy(map)
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.img = None
        self.rect = None
        self.inmap1 = None  # 判断下一个点是否在地图内
        self.inmap2 = None  # 判断再下一个点是否在地图内
        for i in range(0, 7):
            for j in range(0, 7):
                if self.mapnow[i][j] == 1:
                    self.workerx = i
                    self.workery = j

    def renewmap(self):
        # 绘制地图
        for i in range(0, 7):
            for j in range(0, 7):
                self.img = imgs[self.mapnow[i][j]]
                self.rect = self.img.get_rect()
                self.rect.x = i * 32
                self.rect.y = j * 32
                self.screen.blit(self.img, self.rect)

    def initmap(self):
        # 恢复地图状态
        self.mapnow = copy.deepcopy(map)
        for i in range(0, 7):
            for j in range(0, 7):
                if self.mapnow[i][j] == 1:
                    self.workerx = i
                    self.workery = j
        self.renewmap()

    def moveto(self, x1, y1, x2, y2):
        # 移动工人并改变地图数组内容
        if 0 <= x1 < 7 and 0 <= y1 < 7:
            self.inmap1 = True
        else:
            self.inmap1 = False

        if 0 <= x2 < 7 and 0 <= y2 < 7:
            self.inmap2 = True
        else:
            self.inmap2 = False

        # 对移动的下一个点和下下一个点进行判定
        # 下一点为路面
        if self.inmap1 and self.mapnow[x1][y1] == road:
            self.moveman()
            self.mapnow[x1][y1] = worker
            self.workerx = x1
            self.workery = y1
        # 下一点为箱子，下下一点为路或者目的地
        elif self.inmap1 and self.inmap2 and self.mapnow[x1][y1] == box and (self.mapnow[x2][y2] == road or self.mapnow[x2][y2] == destination):
            if self.mapnow[x2][y2] == road:
                self.moveman()
                self.mapnow[x1][y1] = worker
                self.mapnow[x2][y2] = box
                self.workerx = x1
                self.workery = y1
            elif self.mapnow[x2][y2] == destination:
                self.moveman()
                self.mapnow[x1][y1] = worker
                self.mapnow[x2][y2] = box_in_des
                self.workerx = x1
                self.workery = y1
        # 下一点为目的地箱子，下下一点为路
        elif self.inmap1 and self.inmap2 and self.mapnow[x1][y1] == box_in_des and self.mapnow[x2][y2] == road:
            self.moveman()
            self.mapnow[x1][y1] = man_in_des
            self.mapnow[x2][y2] = box
            self.workerx = x1
            self.workery = y1
        # 下一点为目的地箱子，下下一点为目的地
        elif self.inmap1 and self.inmap2 and self.mapnow[x1][y1] == box_in_des and self.mapnow[x2][y2] == destination:
            self.moveman()
            self.mapnow[x1][y1] = man_in_des
            self.mapnow[x2][y2] = box_in_des
            self.workerx = x1
            self.workery = y1
        # 下一点为目的地
        elif self.inmap1 and self.mapnow[x1][y1] == destination:
            self.moveman()
            self.mapnow[x1][y1] = man_in_des
            self.workerx = x1
            self.workery = y1

    def moveman(self):
        # 改变工人移动后原来位置的图形
        if self.mapnow[self.workerx][self.workery] == worker:
            self.mapnow[self.workerx][self.workery] = road
        elif self.mapnow[self.workerx][self.workery] == man_in_des:
            self.mapnow[self.workerx][self.workery] = destination
