TIMELEFT = 30


class GameStates:
    """跟踪游戏信息"""

    def __init__(self):
        """初始化信息"""
        self.level = 1  # 关卡数
        self.game_active = 'NOT_START'
        self.time_left = TIMELEFT
        self.lasttick = 0
        self.nowtick = 0
