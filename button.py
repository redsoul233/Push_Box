import pygame.font


class Button:
    """控制按钮的类"""

    def __init__(self, ai_game, msg, x, y):
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮尺寸和其它属性
        self.width, self.height = 50, 20
        self.button_color = (151, 113, 74)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 24)

        # 创建按钮rect对象，并居中，y轴坐标需要输入
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x
        self.rect.y = y

        # 渲染按钮
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制按钮
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)