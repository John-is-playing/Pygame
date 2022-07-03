from pygame.locals import *
from modules.endInterface import *
from modules.game2048 import *
from modules.utils import *
from blocks import block_s, block_i, block_j, block_l, block_o, block_t, block_z
from pygame.locals import QUIT, KEYDOWN
from collections import namedtuple
from sys import exit
score = 0
def games():
    def flappybird():
        import pygame
        import sys
        import random

        class Bird(object):
            """定义一个鸟类"""

            def __init__(self):
                """定义初始化方法"""
                self.birdRect = pygame.Rect(65, 50, 50, 50)  # 鸟的矩形
                # 定义鸟的3种状态列表
                self.birdStatus = [pygame.image.load("assets/1.png"),
                                   pygame.image.load("assets/2.png"),
                                   pygame.image.load("assets/dead.png")]
                self.status = 0  # 默认飞行状态
                self.birdX = 120  # 鸟所在X轴坐标,即是向右飞行的速度
                self.birdY = 350  # 鸟所在Y轴坐标,即上下飞行高度
                self.jump = False  # 默认情况小鸟自动降落
                self.jumpSpeed = 10  # 跳跃高度
                self.gravity = 5  # 重力
                self.dead = False  # 默认小鸟生命状态为活着

            def birdUpdate(self):
                if self.jump:
                    # 小鸟跳跃
                    self.jumpSpeed -= 1  # 速度递减，上升越来越慢
                    self.birdY -= self.jumpSpeed  # 鸟Y轴坐标减小，小鸟上升
                else:
                    # 小鸟坠落
                    self.gravity += 0.2  # 重力递增，下降越来越快
                    self.birdY += self.gravity  # 鸟Y轴坐标增加，小鸟下降
                self.birdRect[1] = self.birdY  # 更改Y轴位置

        class Pipeline(object):
            """定义一个管道类"""

            def __init__(self):
                """定义初始化方法"""
                self.wallx = 400;  # 管道所在X轴坐标
                self.pineUp = pygame.image.load("assets/top.png")
                self.pineDown = pygame.image.load("assets/bottom.png")

            def updatePipeline(self):
                """"管道移动方法"""
                self.wallx -= 5  # 管道X轴坐标递减，即管道向左移动
                # 当管道运行到一定位置，即小鸟飞越管道，分数加1，并且重置管道
                if self.wallx < -80:
                    global score
                    score += 1
                    self.wallx = 400

        def createMap():
            """定义创建地图的方法"""
            screen.fill((255, 255, 255))  # 填充颜色
            screen.blit(background, (0, 0))  # 填入到背景

            # 显示管道
            screen.blit(Pipeline.pineUp, (Pipeline.wallx, -300));  # 上管道坐标位置
            screen.blit(Pipeline.pineDown, (Pipeline.wallx, 500));  # 下管道坐标位置
            Pipeline.updatePipeline()  # 管道移动

            # 显示小鸟
            if Bird.dead:  # 撞管道状态
                Bird.status = 2
            elif Bird.jump:  # 起飞状态
                Bird.status = 1
            screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))  # 设置小鸟的坐标
            Bird.birdUpdate()  # 鸟移动

            # 显示分数
            screen.blit(font.render(str(score), -1, (255, 255, 255)), (200, 50))  # 设置颜色及坐标位置
            pygame.display.update()  # 更新显示

        def checkDead():
            # 上方管子的矩形位置
            upRect = pygame.Rect(Pipeline.wallx, -300,
                                 Pipeline.pineUp.get_width() - 10,
                                 Pipeline.pineUp.get_height())

            # 下方管子的矩形位置
            downRect = pygame.Rect(Pipeline.wallx, 500,
                                   Pipeline.pineDown.get_width() - 10,
                                   Pipeline.pineDown.get_height())
            # 检测小鸟与上下方管子是否碰撞
            if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect):
                Bird.dead = True
            # 检测小鸟是否飞出上下边界
            if not 0 < Bird.birdRect[1] < height:
                Bird.dead = True
                return True
            else:
                return False

        def getResutl():
            final_text1 = "Game Over"
            final_text2 = "Your final score is:  " + str(score)
            ft1_font = pygame.font.SysFont("Arial", 70)  # 设置第一行文字字体
            ft1_surf = font.render(final_text1, 1, (242, 3, 36))  # 设置第一行文字颜色
            ft2_font = pygame.font.SysFont("Arial", 50)  # 设置第二行文字字体
            ft2_surf = font.render(final_text2, 1, (253, 177, 6))  # 设置第二行文字颜色
            screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
            screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])  # 设置第二行文字显示位置
            pygame.display.flip()  # 更新整个待显示的Surface对象到屏幕上

        if __name__ == '__main__':
            """主程序"""
            pygame.init()  # 初始化pygame
            pygame.font.init()  # 初始化字体
            font = pygame.font.SysFont("Arial", 50)  # 设置字体和大小
            size = width, height = 400, 680  # 设置窗口
            pygame.display.set_caption("flappybird")
            screen = pygame.display.set_mode(size)  # 显示窗口
            clock = pygame.time.Clock()  # 设置时钟
            Pipeline = Pipeline()  # 实例化管道类
            Bird = Bird()  # 实例化鸟类
            speed = 10  # 速度（随着分数增加，值增大
            while True:
                if score > 2:
                    speed = 10 * ((score // 2) + 1)
                clock.tick(speed)  # 每秒执行speed次
                # 轮询事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:
                        Bird.jump = True  # 跳跃
                        Bird.gravity = 5  # 重力
                        Bird.jumpSpeed = 10  # 跳跃速度

                background = pygame.image.load("assets/background.png")  # 加载背景图片
                if checkDead():  # 检测小鸟生命状态
                    getResutl()  # 如果小鸟死亡，显示游戏总分数
                else:
                    createMap()  # 创建地图
    def ball():
        # -*- coding:utf-8 -*-
        import sys  # 导入sys模块
        import pygame  # 导入pygame模块

        pygame.init()  # 初始化pygame
        size = width, height = 640, 400  # 设置窗口
        screen = pygame.display.set_mode(size)  # 显示窗口
        pygame.display.set_caption("小球游戏")
        background = pygame.image.load("background.png") # 加载背景图片

        ball = pygame.image.load("./ballas.png")  # 加载图片
        ballrect = ball.get_rect()  # 获取矩形区域

        speed = [5, 5]  # 设置移动的X轴、Y轴距离
        clock = pygame.time.Clock()  # 设置时钟
        # 执行死循环，确保窗口一直显示
        while True:
            clock.tick(60)  # 每秒执行60次
            # 检查事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 如果点击关闭窗口，则退出
                    pygame.quit()  # 退出pygame
                    sys.exit()

            ballrect = ballrect.move(speed)  # 移动小球
            # 碰到左右边缘
            if ballrect.left < 0 or ballrect.right > width:
                speed[0] = -speed[0]
            # 碰到上下边缘
            if ballrect.top < 0 or ballrect.bottom > height:
                speed[1] = -speed[1]

            screen.blit(pygame.transform.scale(background, [640,480]), (0, 0))   # 填入到背景

            screen.blit(ball, ballrect)  # 将图片画到窗口上
            pygame.display.flip()  # 更新全部显示
    def cunmin():
        import pygame
        import sys
        import pygame.freetype

        color = (255,255,255)
        def init():
            pygame.init()
            size = width,height = 1000,800
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption("村民崩溃")
            cunmin = pygame.image.load("cunmin.png")
            yanjiang = pygame.image.load("yanjiang.jpg")
            wanjia = pygame.image.load("wanjia.png")
            cunmin = pygame.transform.scale(cunmin, (100, 200))
            wanjia = pygame.transform.scale(wanjia, (100, 200))
            yanjiang = pygame.transform.scale(yanjiang, (1000, 200))
            cunminrect = cunmin.get_rect()
            number = 0
            com = 1
            cunmin.set_colorkey((255,255,255))
            final_text1 = "村民:我招谁惹谁了啊！"
            font1 = pygame.font.Font('./STSONG.TTF', 20)
            ft1_surf = font1.render(final_text1, 1, (242, 3, 36))
            final_text2 = "史蒂夫:让你当奸商！"
            font1 = pygame.font.Font('./STSONG.TTF', 20)
            ft2_surf = font1.render(final_text2, 1, (242, 3, 36))
            final_text3 = "村民:放了我吧，我再也不改了！"
            font1 = pygame.font.Font('./STSONG.TTF', 20)
            ft3_surf = font1.render(final_text3, 1, (242, 3, 36))
            final_text4 = "史蒂夫:你说什么？！！"
            font1 = pygame.font.Font('./STSONG.TTF', 20)
            ft4_surf = font1.render(final_text4, 1, (242, 3, 36))
            final_text5 = "村民:我说，我再也不敢了！"
            font1 = pygame.font.Font('./STSONG.TTF', 20)
            ft5_surf = font1.render(final_text5, 1, (242, 3, 36))
            final_text6 = "史蒂夫:算你识相，再烤几年吧！"
            font1 = pygame.font.Font('./STSONG.TTF', 20)
            ft6_surf = font1.render(final_text6, 1, (242, 3, 36))
            final_text7 = "村民:不要啊！！！"
            font1 = pygame.font.Font('./STSONG.TTF', 20)
            ft7_surf = font1.render(final_text7, 1, (242, 3, 36))
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                screen.fill(color)
                if not number == 570:
                    number = number+com
                else:
                    number = 0
                screen.fill((255,255,255))
                screen.blit(yanjiang, (0, 600))
                screen.blit(cunmin, (300, number))
                screen.blit(wanjia, (800,600))
                screen.blit(ft1_surf,(0,0))
                screen.blit(ft2_surf, (800, 50))
                screen.blit(ft3_surf, (0, 100))
                screen.blit(ft4_surf, (800, 150))
                screen.blit(ft5_surf, (0, 200))
                screen.blit(ft6_surf, (710, 250))
                screen.blit(ft7_surf, (0, 300))
                pygame.display.flip()
        if __name__ == '__main__':
            init()
    def AI_five():
        """五子棋之人机对战"""

        import sys
        import random
        import pygame
        import pygame.gfxdraw

        Chessman = namedtuple('Chessman', 'Name Value Color')
        Point = namedtuple('Point', 'X Y')

        BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
        WHITE_CHESSMAN = Chessman('白子', 2, (219, 219, 219))

        offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

        class Checkerboard:
            def __init__(self, line_points):
                self._line_points = line_points
                self._checkerboard = [[0] * line_points for _ in range(line_points)]

            def _get_checkerboard(self):
                return self._checkerboard

            checkerboard = property(_get_checkerboard)

            # 判断是否可落子
            def can_drop(self, point):
                return self._checkerboard[point.Y][point.X] == 0

            def drop(self, chessman, point):
                """
                落子
                :param chessman:
                :param point:落子位置
                :return:若该子落下之后即可获胜，则返回获胜方，否则返回 None
                """
                # 把黑棋/白棋落子的坐标打印出来
                print(f'{chessman.Name} ({point.X}, {point.Y})')
                self._checkerboard[point.Y][point.X] = chessman.Value

                # 打印获胜方出来
                if self._win(point):
                    print(f'{chessman.Name}获胜')
                    return chessman

            # 判断是否赢了
            def _win(self, point):
                cur_value = self._checkerboard[point.Y][point.X]
                for os in offset:
                    if self._get_count_on_direction(point, cur_value, os[0], os[1]):
                        return True

            # 判断是否赢了的代码，从这里往上看，代码都是正着写，反着看，写代码思路缺什么补什么，所以从这里开始看
            # 声明一个函数，按方向数数，数满5个就获胜。
            # 一个二维坐标上，判断上下、左右、两个45度直线，是否有五个相同的直连棋子，只要满足五颗子，则游戏结束:
            def _get_count_on_direction(self, point, value, x_offset, y_offset):
                count = 1
                for step in range(1, 5):
                    x = point.X + step * x_offset
                    y = point.Y + step * y_offset
                    if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                        count += 1
                    else:
                        break
                for step in range(1, 5):
                    x = point.X - step * x_offset
                    y = point.Y - step * y_offset
                    if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                        count += 1
                    else:
                        break

                return count >= 5

        SIZE = 30  # 棋盘每个点时间的间隔
        Line_Points = 19  # 棋盘每行/每列点数
        Outer_Width = 20  # 棋盘外宽度
        Border_Width = 4  # 边框宽度
        Inside_Width = 4  # 边框跟实际的棋盘之间的间隔
        Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width  # 边框线的长度
        Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width  # 网格线起点（左上角）坐标
        SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2  # 游戏屏幕的高
        SCREEN_WIDTH = SCREEN_HEIGHT + 200  # 游戏屏幕的宽

        Stone_Radius = SIZE // 2 - 3  # 棋子半径
        Stone_Radius2 = SIZE // 2 + 3
        Checkerboard_Color = (0xE3, 0x92, 0x65)  # 棋盘颜色，0x是16进制表示哦
        BLACK_COLOR = (0, 0, 0)
        WHITE_COLOR = (255, 255, 255)
        RED_COLOR = (200, 30, 30)
        BLUE_COLOR = (30, 30, 200)

        RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10

        def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
            imgText = font.render(text, True, fcolor)
            screen.blit(imgText, (x, y))

        def main():
            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption('AI五子棋')

            font1 = pygame.font.SysFont('SimHei', 32)  # 字体：黑体，32号
            font2 = pygame.font.SysFont('SimHei', 72)  # 字体：黑体，72号
            fwidth, fheight = font2.size('黑方获胜')

            checkerboard = Checkerboard(Line_Points)
            cur_runner = BLACK_CHESSMAN
            winner = None
            computer = AI(Line_Points, WHITE_CHESSMAN)

            # 设置黑白双方初始连子为0
            black_win_count = 0
            white_win_count = 0

            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            if winner is not None:
                                winner = None
                                cur_runner = BLACK_CHESSMAN
                                checkerboard = Checkerboard(Line_Points)
                                computer = AI(Line_Points, WHITE_CHESSMAN)
                    elif event.type == MOUSEBUTTONDOWN:  # 检测鼠标落下
                        if winner is None:  # 检测是否有一方胜出
                            pressed_array = pygame.mouse.get_pressed()
                            if pressed_array[0]:
                                mouse_pos = pygame.mouse.get_pos()
                                click_point = _get_clickpoint(mouse_pos)
                                if click_point is not None:  # 检测鼠标是否在棋盘内点击
                                    if checkerboard.can_drop(click_point):
                                        winner = checkerboard.drop(cur_runner, click_point)
                                        if winner is None:  # 再次判断是否有胜出
                                            # 一个循环内检测两次，意思就是人出一次检测一下，电脑出一次检测一下。
                                            cur_runner = _get_next(cur_runner)
                                            computer.get_opponent_drop(click_point)
                                            AI_point = computer.AI_drop()
                                            winner = checkerboard.drop(cur_runner, AI_point)
                                            if winner is not None:
                                                white_win_count += 1
                                            cur_runner = _get_next(cur_runner)
                                        else:
                                            black_win_count += 1
                                else:
                                    print('超出棋盘区域')

                # 画棋盘
                _draw_checkerboard(screen)

                # 画棋盘上已有的棋子
                for i, row in enumerate(checkerboard.checkerboard):
                    for j, cell in enumerate(row):
                        if cell == BLACK_CHESSMAN.Value:
                            _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                        elif cell == WHITE_CHESSMAN.Value:
                            _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)

                _draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count)

                if winner:
                    print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2,
                               winner.Name + '获胜',
                               RED_COLOR)

                pygame.display.flip()

        def _get_next(cur_runner):
            if cur_runner == BLACK_CHESSMAN:
                return WHITE_CHESSMAN
            else:
                return BLACK_CHESSMAN

        # 画棋盘
        def _draw_checkerboard(screen):
            # 填充棋盘背景色
            screen.fill(Checkerboard_Color)
            # 画棋盘网格线外的边框
            pygame.draw.rect(screen, BLACK_COLOR, (Outer_Width, Outer_Width, Border_Length, Border_Length), Border_Width)
            # 画网格线
            for i in range(Line_Points):
                pygame.draw.line(screen, BLACK_COLOR,
                                 (Start_Y, Start_Y + SIZE * i),
                                 (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
                                 1)
            for j in range(Line_Points):
                pygame.draw.line(screen, BLACK_COLOR,
                                 (Start_X + SIZE * j, Start_X),
                                 (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
                                 1)
            # 画星位和天元
            for i in (3, 9, 15):
                for j in (3, 9, 15):
                    if i == j == 9:
                        radius = 5
                    else:
                        radius = 3
                    # pygame.draw.circle(screen, BLACK, (Start_X + SIZE * i, Start_Y + SIZE * j), radius)
                    pygame.gfxdraw.aacircle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)
                    pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)

        # 画棋子
        def _draw_chessman(screen, point, stone_color):
            # pygame.draw.circle(screen, stone_color, (Start_X + SIZE * point.X, Start_Y + SIZE * point.Y), Stone_Radius)
            pygame.gfxdraw.aacircle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)
            pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius,
                                         stone_color)

        # 画右侧信息显示
        def _draw_left_info(screen, font, cur_runner, black_win_count, white_win_count):
            _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2), BLACK_CHESSMAN.Color)
            _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2 * 4), WHITE_CHESSMAN.Color)

            print_text(screen, font, RIGHT_INFO_POS_X, Start_X + 3, '玩家', BLUE_COLOR)
            print_text(screen, font, RIGHT_INFO_POS_X, Start_X + Stone_Radius2 * 3 + 3, '电脑', BLUE_COLOR)

            print_text(screen, font, SCREEN_HEIGHT, SCREEN_HEIGHT - Stone_Radius2 * 8, '战况：', BLUE_COLOR)
            _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - int(Stone_Radius2 * 4.5)),
                               BLACK_CHESSMAN.Color)
            _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - Stone_Radius2 * 2),
                               WHITE_CHESSMAN.Color)
            print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - int(Stone_Radius2 * 5.5) + 3, f'{black_win_count} 胜',
                       BLUE_COLOR)
            print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - Stone_Radius2 * 3 + 3, f'{white_win_count} 胜',
                       BLUE_COLOR)

        def _draw_chessman_pos(screen, pos, stone_color):
            pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
            pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)

        # 根据鼠标点击位置，返回游戏区坐标
        def _get_clickpoint(click_pos):
            pos_x = click_pos[0] - Start_X
            pos_y = click_pos[1] - Start_Y
            if pos_x < -Inside_Width or pos_y < -Inside_Width:
                return None
            x = pos_x // SIZE
            y = pos_y // SIZE
            if pos_x % SIZE > Stone_Radius:
                x += 1
            if pos_y % SIZE > Stone_Radius:
                y += 1
            if x >= Line_Points or y >= Line_Points:
                return None

            return Point(x, y)

        class AI:
            def __init__(self, line_points, chessman):
                self._line_points = line_points
                self._my = chessman
                self._opponent = BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
                self._checkerboard = [[0] * line_points for _ in range(line_points)]

            def get_opponent_drop(self, point):
                self._checkerboard[point.Y][point.X] = self._opponent.Value

            def AI_drop(self):
                point = None
                score = 0
                for i in range(self._line_points):
                    for j in range(self._line_points):
                        if self._checkerboard[j][i] == 0:
                            _score = self._get_point_score(Point(i, j))
                            if _score > score:
                                score = _score
                                point = Point(i, j)
                            elif _score == score and _score > 0:
                                r = random.randint(0, 100)
                                if r % 2 == 0:
                                    point = Point(i, j)
                self._checkerboard[point.Y][point.X] = self._my.Value
                return point

            def _get_point_score(self, point):
                score = 0
                for os in offset:
                    score += self._get_direction_score(point, os[0], os[1])
                return score

            def _get_direction_score(self, point, x_offset, y_offset):
                count = 0  # 落子处我方连续子数
                _count = 0  # 落子处对方连续子数
                space = None  # 我方连续子中有无空格
                _space = None  # 对方连续子中有无空格
                both = 0  # 我方连续子两端有无阻挡
                _both = 0  # 对方连续子两端有无阻挡

                # 如果是 1 表示是边上是我方子，2 表示敌方子
                flag = self._get_stone_color(point, x_offset, y_offset, True)
                if flag != 0:
                    for step in range(1, 6):
                        x = point.X + step * x_offset
                        y = point.Y + step * y_offset
                        if 0 <= x < self._line_points and 0 <= y < self._line_points:
                            if flag == 1:
                                if self._checkerboard[y][x] == self._my.Value:
                                    count += 1
                                    if space is False:
                                        space = True
                                elif self._checkerboard[y][x] == self._opponent.Value:
                                    _both += 1
                                    break
                                else:
                                    if space is None:
                                        space = False
                                    else:
                                        break  # 遇到第二个空格退出
                            elif flag == 2:
                                if self._checkerboard[y][x] == self._my.Value:
                                    _both += 1
                                    break
                                elif self._checkerboard[y][x] == self._opponent.Value:
                                    _count += 1
                                    if _space is False:
                                        _space = True
                                else:
                                    if _space is None:
                                        _space = False
                                    else:
                                        break
                        else:
                            # 遇到边也就是阻挡
                            if flag == 1:
                                both += 1
                            elif flag == 2:
                                _both += 1

                if space is False:
                    space = None
                if _space is False:
                    _space = None

                _flag = self._get_stone_color(point, -x_offset, -y_offset, True)
                if _flag != 0:
                    for step in range(1, 6):
                        x = point.X - step * x_offset
                        y = point.Y - step * y_offset
                        if 0 <= x < self._line_points and 0 <= y < self._line_points:
                            if _flag == 1:
                                if self._checkerboard[y][x] == self._my.Value:
                                    count += 1
                                    if space is False:
                                        space = True
                                elif self._checkerboard[y][x] == self._opponent.Value:
                                    _both += 1
                                    break
                                else:
                                    if space is None:
                                        space = False
                                    else:
                                        break  # 遇到第二个空格退出
                            elif _flag == 2:
                                if self._checkerboard[y][x] == self._my.Value:
                                    _both += 1
                                    break
                                elif self._checkerboard[y][x] == self._opponent.Value:
                                    _count += 1
                                    if _space is False:
                                        _space = True
                                else:
                                    if _space is None:
                                        _space = False
                                    else:
                                        break
                        else:
                            # 遇到边也就是阻挡
                            if _flag == 1:
                                both += 1
                            elif _flag == 2:
                                _both += 1

                ''' 下面这一串score（分数）的含义：评估棋格获胜分数。
                使计算机计算获胜分值越高的棋格，就能确定能让自己的棋子最有可能达成联机的位置，也就是最佳进攻位置，
                而一旦计算机能确定自己的最高分值的位置，计算机就具备了进攻能力。
                同理，计算机能计算出玩家的最大分值位置，并抢先玩家获得该位置，这样计算机就具有了防御的能力。
    
                在计算机下棋之前，会计算空白棋格上的获胜分数，根据分数高低获取最佳位置。
                计算机会将棋子下在获胜分数最高的地方。
                当已放置4颗棋子时，必须在第五个空棋格上设置绝对高的分值。也就是10000
                当获胜组合上有部分位置已被对手的棋格占据而无法连成五子时，获胜组合上空棋格的获胜分数会直接设置为0。（四颗棋子，你把中间断了）
                当有两组及其以上的获胜组合位置交叉时，对该位置的分数进行叠加，形成分数比周围位置明显高。（五子棋中三三相连）'''

                score: int = 0
                if count == 4:
                    score = 10000
                elif _count == 4:
                    score = 9000
                elif count == 3:
                    if both == 0:
                        score = 1000
                    elif both == 1:
                        score = 100
                    else:
                        score = 0
                elif _count == 3:
                    if _both == 0:
                        score = 900
                    elif _both == 1:
                        score = 90
                    else:
                        score = 0
                elif count == 2:
                    if both == 0:
                        score = 100
                    elif both == 1:
                        score = 10
                    else:
                        score = 0
                elif _count == 2:
                    if _both == 0:
                        score = 90
                    elif _both == 1:
                        score = 9
                    else:
                        score = 0
                elif count == 1:
                    score = 10
                elif _count == 1:
                    score = 9
                else:
                    score = 0

                if space or _space:
                    score /= 2

                return score

            # 判断指定位置处在指定方向上是我方子、对方子、空
            def _get_stone_color(self, point, x_offset, y_offset, next):
                x = point.X + x_offset
                y = point.Y + y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if self._checkerboard[y][x] == self._my.Value:
                        return 1
                    elif self._checkerboard[y][x] == self._opponent.Value:
                        return 2
                    else:
                        if next:
                            return self._get_stone_color(Point(x, y), x_offset, y_offset, False)
                        else:
                            return 0
                else:
                    return 0

        if __name__ == '__main__':
            main()
    def five():
        # 调用pygame库
        import pygame
        import sys
        # 调用常用关键字常量
        import numpy as np
        # 初始化pygame
        pygame.init()
        # 获取对显示系统的访问，并创建一个窗口screen
        # 窗口大小为670x670
        screen = pygame.display.set_mode((670, 670))
        pygame.display.set_caption("五子棋")
        screen_color = [238, 154, 73]  # 设置画布颜色,[238,154,73]对应为棕黄色
        line_color = [0, 0, 0]  # 设置线条颜色，[0,0,0]对应黑色

        def check_win(over_pos):  # 判断五子连心
            mp = np.zeros([15, 15], dtype=int)
            for val in over_pos:
                x = int((val[0][0] - 27) / 44)
                y = int((val[0][1] - 27) / 44)
                if val[1] == white_color:
                    mp[x][y] = 2  # 表示白子
                else:
                    mp[x][y] = 1  # 表示黑子

            for i in range(15):
                pos1 = []
                pos2 = []
                for j in range(15):
                    if mp[i][j] == 1:
                        pos1.append([i, j])
                    else:
                        pos1 = []
                    if mp[i][j] == 2:
                        pos2.append([i, j])
                    else:
                        pos2 = []
                    if len(pos1) >= 5:  # 五子连心
                        return [1, pos1]
                    if len(pos2) >= 5:
                        return [2, pos2]

            for j in range(15):
                pos1 = []
                pos2 = []
                for i in range(15):
                    if mp[i][j] == 1:
                        pos1.append([i, j])
                    else:
                        pos1 = []
                    if mp[i][j] == 2:
                        pos2.append([i, j])
                    else:
                        pos2 = []
                    if len(pos1) >= 5:
                        return [1, pos1]
                    if len(pos2) >= 5:
                        return [2, pos2]
            for i in range(15):
                for j in range(15):
                    pos1 = []
                    pos2 = []
                    for k in range(15):
                        if i + k >= 15 or j + k >= 15:
                            break
                        if mp[i + k][j + k] == 1:
                            pos1.append([i + k, j + k])
                        else:
                            pos1 = []
                        if mp[i + k][j + k] == 2:
                            pos2.append([i + k, j + k])
                        else:
                            pos2 = []
                        if len(pos1) >= 5:
                            return [1, pos1]
                        if len(pos2) >= 5:
                            return [2, pos2]
            for i in range(15):
                for j in range(15):
                    pos1 = []
                    pos2 = []
                    for k in range(15):
                        if i + k >= 15 or j - k < 0:
                            break
                        if mp[i + k][j - k] == 1:
                            pos1.append([i + k, j - k])
                        else:
                            pos1 = []
                        if mp[i + k][j - k] == 2:
                            pos2.append([i + k, j - k])
                        else:
                            pos2 = []
                        if len(pos1) >= 5:
                            return [1, pos1]
                        if len(pos2) >= 5:
                            return [2, pos2]
            return [0, []]

        def find_pos(x, y):  # 找到显示的可以落子的位置
            for i in range(27, 670, 44):
                for j in range(27, 670, 44):
                    L1 = i - 22
                    L2 = i + 22
                    R1 = j - 22
                    R2 = j + 22
                    if x >= L1 and x <= L2 and y >= R1 and y <= R2:
                        return i, j
            return x, y

        def check_over_pos(x, y, over_pos):  # 检查当前的位置是否已经落子
            for val in over_pos:
                if val[0][0] == x and val[0][1] == y:
                    return False
            return True  # 表示没有落子

        flag = False
        tim = 0

        over_pos = []  # 表示已经落子的位置
        white_color = [255, 255, 255]  # 白棋颜色
        black_color = [0, 0, 0]  # 黑棋颜色

        while True:  # 不断训练刷新画布

            for event in pygame.event.get():  # 获取事件，如果鼠标点击右上角关闭按钮，关闭
                if event.type == QUIT:
                    sys.exit()

            screen.fill(screen_color)  # 清屏
            for i in range(27, 670, 44):
                # 先画竖线
                if i == 27 or i == 670 - 27:  # 边缘线稍微粗一些
                    pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 4)
                else:
                    pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 2)
                # 再画横线
                if i == 27 or i == 670 - 27:  # 边缘线稍微粗一些
                    pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 4)
                else:
                    pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 2)

            # 在棋盘中心画个小圆表示正中心位置
            pygame.draw.circle(screen, line_color, [27 + 44 * 7, 27 + 44 * 7], 8, 0)

            for val in over_pos:  # 显示所有落下的棋子
                pygame.draw.circle(screen, val[1], val[0], 20, 0)

            # 判断是否存在五子连心
            res = check_win(over_pos)
            if res[0] != 0:
                for pos in res[1]:
                    pygame.draw.rect(screen, [238, 48, 167], [pos[0] * 44 + 27 - 22, pos[1] * 44 + 27 - 22, 44, 44], 2, 1)
                pygame.display.update()  # 刷新显示
                continue  # 游戏结束，停止下面的操作
            # 获取鼠标坐标信息
            x, y = pygame.mouse.get_pos()

            x, y = find_pos(x, y)
            if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再显示
                pygame.draw.rect(screen, [0, 229, 238], [x - 22, y - 22, 44, 44], 2, 1)

            keys_pressed = pygame.mouse.get_pressed()  # 获取鼠标按键信息

            # 鼠标左键表示落子,tim用来延时的，因为每次循环时间间隔很断，容易导致明明只按了一次左键，却被多次获取，认为我按了多次
            if keys_pressed[0] and tim == 0 or pygame.event == KEYDOWN:
                flag = True
                if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再落子
                    if len(over_pos) % 2 == 0:  # 黑子
                        over_pos.append([[x, y], black_color])
                    else:
                        over_pos.append([[x, y], white_color])
            mykeyslist = pygame.key.get_pressed()  # 获取按键元组信息
            if mykeyslist[pygame.K_RIGHT]:  # 如果按键按下，这个值为1
                flag = True
                if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再落子
                    if len(over_pos) % 2 == 0:  # 黑子
                        over_pos.append([[x, y], black_color])
                    else:
                        over_pos.append([[x, y], white_color])

            # 鼠标左键延时作用
            if flag:
                tim += 1
            if tim % 50 == 0:  # 延时200ms
                flag = False
                tim = 0

            pygame.display.update()  # 刷新显示
    def g2048():
        # main.py
        """
         功能：2048小游戏
         作者：指尖魔法师
         QQ：14555110
        """

        import pygame
        import cfg

        def main(cfg):
            # 初始化pygame
            pygame.init()

            pygame.mixer.music.load(cfg.BGMPATH)
            pygame.mixer.music.play(-1)

            # 创建一个窗口
            screen = pygame.display.set_mode(cfg.SCREENSIZE, 0, 32)

            # 设置窗口标题
            pygame.display.set_caption("2048小游戏")
            # 实例化Game2048
            game_2048 = Game2048(matrix_size=cfg.GAME_MATRIX_SIZE, max_score_filepath=cfg.MAX_SCORE_FILEPATH)

            # 游戏主循环
            is_running = True
            while is_running:
                # 填充背景颜色
                screen.fill(pygame.Color(cfg.BG_COLOR))

                # 按键检测
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 接受到退出事件后退出
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                            game_2048.setDirection(
                                {pygame.K_UP: 'UP', pygame.K_DOWN: 'DOWN', pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT'}[
                                    event.key])

                # 更新游戏状态
                game_2048.update()
                if game_2048.isGameOver:
                    print('游戏结束')
                    is_running = False
                    game_2048.saveMaxScore()

                # 将元素画到屏幕上
                drawGameMatrix(screen, game_2048.game_matrix, cfg)
                (start_x, start_y) = drawScore(screen, game_2048.score, game_2048.max_score, cfg)
                drawGameIntro(screen, start_x, start_y, cfg)

                # 刷新画面
                pygame.display.update()

            # 游戏结束界面
            return endInterface(screen, cfg)

        if __name__ == '__main__':
            while True:
                if not main(cfg):
                    break
            import sys
            pygame.quit()
            sys.exit()
    def snack():
        import pygame
        import sys
        import time
        import random

        pygame.init()

        white = (255, 255, 255)
        yellow = (255, 255, 102)
        black = (0, 0, 0)
        red = (213, 50, 80)
        green = (0, 255, 0)
        blue = (50, 153, 213)

        dis_width = 800
        dis_height = 600

        dis = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('贪吃蛇')

        clock = pygame.time.Clock()

        snake_block = 10
        snake_speed = 15

        font_style = pygame.font.Font("./simfang.ttf", 25)
        score_font = pygame.font.Font("./simfang.ttf", 35)

        def Your_score(score):
            value = score_font.render("Score: " + str(score), True, yellow)
            dis.blit(value, [0, 0])

        def our_snake(snake_block, snake_list):
            for x in snake_list:
                pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

        def message(msg, color):
            mesg = font_style.render(msg, True, color)
            dis.blit(mesg, [dis_width / 6, dis_height / 3])

        def gameLoop():
            game_over = False
            game_close = False

            x1 = dis_width / 2
            y1 = dis_height / 2

            x1_change = 0
            y1_change = 0

            snake_List = []
            Length_of_snake = 1

            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

            while not game_over:

                while game_close == True:
                    dis.fill(blue)
                    message("游戏结束，按Q退出或按P重新开始", red)
                    Your_score(Length_of_snake - 1)
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_over = True
                                game_close = False
                            if event.key == pygame.K_p:
                                gameLoop()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            x1_change = -snake_block
                            y1_change = 0
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            x1_change = snake_block
                            y1_change = 0
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            y1_change = -snake_block
                            x1_change = 0
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            y1_change = snake_block
                            x1_change = 0

                if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                    game_close = True
                x1 += x1_change
                y1 += y1_change
                dis.fill(blue)
                pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
                snake_Head = []
                snake_Head.append(x1)
                snake_Head.append(y1)
                snake_List.append(snake_Head)
                if len(snake_List) > Length_of_snake:
                    del snake_List[0]

                for x in snake_List[:-1]:
                    if x == snake_Head:
                        game_close = True

                our_snake(snake_block, snake_List)
                Your_score(Length_of_snake - 1)

                pygame.display.update()

                if x1 == foodx and y1 == foody:
                    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                    Length_of_snake += 1

                clock.tick(snake_speed)

            pygame.quit()
            sys.exit()

        gameLoop()
    def eluosi():
        """
        作者：it项目实例网
        更多项目实例，请访问：www.itprojects.cn
        """

        import random
        import sys
        import time

        import pygame


        SCREEN_WIDTH, SCREEN_HEIGHT = 450, 750
        BG_COLOR = (40, 40, 60)  # 背景色
        BLOCK_COL_NUM = 10  # 每行的方格数
        SIZE = 30  # 每个小方格大小
        BLOCK_ROW_NUM = 25  # 每列的方个数
        BORDER_WIDTH = 4  # 游戏区边框宽度
        RED = (200, 30, 30)  # 红色，GAME OVER 的字体颜色

        def judge_game_over(stop_all_block_list):
            """
            判断游戏是否结束
            """
            if "O" in stop_all_block_list[0]:
                return True

        def change_speed(score):
            speed_level = [("1", 0.5, 0, 20), ("2", 0.4, 21, 50), ("3", 0.3, 51, 100), ("4", 0.2, 101, 200),
                           ("5", 0.1, 201, None)]
            for speed_info, speed, score_start, score_stop in speed_level:
                if score_stop and score_start <= score <= score_stop:
                    return speed_info, speed
                elif score_stop is None and score >= score_start:
                    return speed_info, speed

        def judge_lines(stop_all_block_list):
            """
            判断是否有同一行的方格，如果有则消除
            """
            # 记录刚刚消除的行数
            move_row_list = list()
            # 消除满格的行
            for row, line in enumerate(stop_all_block_list):
                if "." not in line:
                    # 如果这一行没有. 那么就意味着全部是O，则消除这一行
                    stop_all_block_list[row] = ['.' for _ in range(len(line))]
                    move_row_list.append(row)

            # 如果没有满格的行，则结束此函数
            if not move_row_list:
                return 0

            # 移动剩余的行到下一行
            for row in move_row_list:
                stop_all_block_list.pop(row)
                stop_all_block_list.insert(0, ['.' for _ in range(len(line))])

            return len(move_row_list) * 10

        def add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row,
                                       current_block_start_col):
            """
            将当前已经停止移动的block添加到列表中
            """
            for row, line in enumerate(current_block):
                for col, block in enumerate(line):
                    if block != '.':
                        stop_all_block_list[current_block_start_row + row][current_block_start_col + col] = "O"

        def change_current_block_style(current_block):
            """
            改变图形的样式
            """
            # 计算出，当前图形样式属于哪个图形
            current_block_style_list = None
            for block_style_list in [block_s, block_i, block_j, block_l, block_o, block_t, block_z]:
                if current_block in block_style_list:
                    current_block_style_list = block_style_list

            # 得到当前正在用的图形的索引（下标）
            index = current_block_style_list.index(current_block)
            # 它的下一个图形的索引
            index += 1
            # 防止越界
            index = index % len(current_block_style_list)
            # 返回下一个图形
            return current_block_style_list[index]

        def judge_move_right(current_block, current_block_start_col):
            """
            判断是否可以向右移动
            """
            # 先判断列的方式是从右到左
            for col in range(len(current_block[0]) - 1, -1, -1):
                # 得到1列的所有元素
                col_list = [line[col] for line in current_block]
                # 判断是否碰到右边界
                if 'O' in col_list and current_block_start_col + col >= BLOCK_COL_NUM:
                    return False
            return True

        def judge_move_left(current_block, current_block_start_col):
            """
            判断是否可以向左移动
            """
            # 先判断列的方式是从左到右
            for col in range(len(current_block[0])):
                # 得到1列的所有元素
                col_list = [line[col] for line in current_block]
                # 判断是否碰到右边界
                if 'O' in col_list and current_block_start_col + col < 0:
                    return False
            return True

        def judge_move_down(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
            """
            判断是否碰撞到其它图形或者底边界
            """
            # 得到其它图形所有的坐标
            stop_all_block_position = list()
            for row, line in enumerate(stop_all_block_list):
                for col, block in enumerate(line):
                    if block != ".":
                        stop_all_block_position.append((row, col))
            # print(stop_all_block_position)

            # 判断碰撞
            for row, line in enumerate(current_block):
                if 'O' in line and current_block_start_row + row >= BLOCK_ROW_NUM:
                    # 如果当前行有0，且从起始行开始算+当前显示的行，超过了总行数，那么就认为碰到了底部
                    return False
                for col, block in enumerate(line):
                    if block != "." and (
                    current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                        return False

            return True

        def get_block():
            """
            创建一个图形
            """
            block_style_list = random.choice([block_s, block_i, block_j, block_l, block_o, block_t, block_z])
            return random.choice(block_style_list)

        def main():
            pygame.init()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption('俄罗斯方块')

            current_block = get_block()  # 当前图形
            current_block_start_row = -2  # 当前图片从哪一行开始显示图形
            current_block_start_col = 4  # 当前图形从哪一列开始显示
            next_block = get_block()  # 下一个图形
            last_time = time.time()
            speed = 0.5  # 降落的速度
            speed_info = '1'  # 显示的速度等级

            # 定义一个列表，用来存储所有的已经停止移动的形状
            stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]

            # 字体
            font = pygame.font.Font('yh.ttf', 24)  # 黑体24
            game_over_font = pygame.font.Font("yh.ttf", 72)
            game_over_font_width, game_over_font_height = game_over_font.size('GAME OVER')
            game_again_font_width, game_again_font_height = font.size('鼠标点击任意位置，再来一局')

            # 得分
            score = 0

            # 标记游戏是否结束
            game_over = False

            # 创建计时器（防止while循环过快，占用太多CPU的问题）
            clock = pygame.time.Clock()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if judge_move_left(current_block, current_block_start_col - 1):
                                current_block_start_col -= 1
                        elif event.key == pygame.K_RIGHT:
                            if judge_move_right(current_block, current_block_start_col + 1):
                                current_block_start_col += 1
                        elif event.key == pygame.K_UP:
                            current_block_next_style = change_current_block_style(current_block)
                            if judge_move_left(current_block_next_style, current_block_start_col) and \
                                    judge_move_right(current_block_next_style, current_block_start_col) and \
                                    judge_move_down(current_block, current_block_start_row, current_block_start_col,
                                                    stop_all_block_list):
                                # 判断新的样式没有越界
                                current_block = current_block_next_style
                        elif event.key == pygame.K_DOWN:
                            # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
                            if judge_move_down(current_block, current_block_start_row + 1, current_block_start_col,
                                               stop_all_block_list):
                                current_block_start_row += 1
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                        if game_over:
                            # 重置游戏用到的变量
                            current_block = get_block()  # 当前图形
                            current_block_start_row = -2  # 当前图片从哪一行开始显示图形
                            current_block_start_col = 4  # 当前图形从哪一列开始显示
                            next_block = get_block()  # 下一个图形
                            stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]
                            score = 0
                            game_over = False

                # 判断是否修改当前图形显示的起始行
                if not game_over and time.time() - last_time > speed:
                    last_time = time.time()
                    # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
                    if judge_move_down(current_block, current_block_start_row + 1, current_block_start_col,
                                       stop_all_block_list):
                        current_block_start_row += 1
                    else:
                        # 将这个图形存储到统一的列表中，这样便于判断是否成为一行
                        add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row,
                                                   current_block_start_col)
                        # 判断是否有同一行的，如果有就消除，且加上分数
                        score += judge_lines(stop_all_block_list)
                        # 判断游戏是否结束（如果第一行中间有O那么就表示游戏结束）
                        game_over = judge_game_over(stop_all_block_list)
                        # 调整速度
                        speed_info, speed = change_speed(score)
                        # 创建新的图形
                        current_block = next_block
                        next_block = get_block()
                        # 重置数据
                        current_block_start_col = 4
                        current_block_start_row = -2

                # 画背景（填充背景色）
                screen.fill(BG_COLOR)

                # 画游戏区域分隔线
                pygame.draw.line(screen, (100, 40, 200), (SIZE * BLOCK_COL_NUM, 0), (SIZE * BLOCK_COL_NUM, SCREEN_HEIGHT),
                                 BORDER_WIDTH)

                # 显示当前图形
                for row, line in enumerate(current_block):
                    for col, block in enumerate(line):
                        if block != '.':
                            pygame.draw.rect(screen, (20, 128, 200), (
                            (current_block_start_col + col) * SIZE, (current_block_start_row + row) * SIZE, SIZE, SIZE), 0)

                # 显示所有停止移动的图形
                for row, line in enumerate(stop_all_block_list):
                    for col, block in enumerate(line):
                        if block != '.':
                            pygame.draw.rect(screen, (20, 128, 200), (col * SIZE, row * SIZE, SIZE, SIZE), 0)

                # 画网格线 竖线
                for x in range(BLOCK_COL_NUM):
                    pygame.draw.line(screen, (0, 0, 0), (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
                # 画网格线 横线
                for y in range(BLOCK_ROW_NUM):
                    pygame.draw.line(screen, (0, 0, 0), (0, y * SIZE), (BLOCK_COL_NUM * SIZE, y * SIZE), 1)

                # 显示右侧（得分、速度、下一行图形）
                # 得分
                score_show_msg = font.render('得分: ', True, (255, 255, 255))
                screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 10))
                score_show_msg = font.render(str(score), True, (255, 255, 255))
                screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 50))
                # 速度
                speed_show_msg = font.render('速度: ', True, (255, 255, 255))
                screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 100))
                speed_show_msg = font.render(speed_info, True, (255, 255, 255))
                screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 150))
                # 下一个图形（文字提示）
                next_style_msg = font.render('下一个: ', True, (255, 255, 255))
                screen.blit(next_style_msg, (BLOCK_COL_NUM * SIZE + 10, 200))
                # 下一个图形（图形）
                for row, line in enumerate(next_block):
                    for col, block in enumerate(line):
                        if block != '.':
                            pygame.draw.rect(screen, (20, 128, 200),
                                             (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE, SIZE, SIZE), 0)
                            # 显示这个方格的4个边的颜色
                            # 左
                            pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE),
                                             (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                            # 上
                            pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE),
                                             (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), 1)
                            # 下
                            pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE),
                                             (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                            # 右
                            pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE),
                                             (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)

                # 显示游戏结束画面
                if game_over:
                    game_over_tips = game_over_font.render('GAME OVER', True, RED)
                    screen.blit(game_over_tips,
                                ((SCREEN_WIDTH - game_over_font_width) // 2, (SCREEN_HEIGHT - game_over_font_height) // 2))
                    # 显示"鼠标点击任意位置，再来一局"
                    game_again = font.render('鼠标点击任意位置，再来一局', True, RED)
                    screen.blit(game_again, (
                    (SCREEN_WIDTH - game_again_font_width) // 2, (SCREEN_HEIGHT - game_again_font_height) // 2 + 80))

                # 刷新显示（此时窗口才会真正的显示）
                pygame.display.update()
                # FPS（每秒钟显示画面的次数）
                clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次

        if __name__ == '__main__':
            main()
    def gamefox():
        def youxihezi():
            import time
            t = 500
            for n in range(t + 1):
                loading = round(n / t * 100)
                # 通过加\r每次输出完跳回，用end=""替换默认的换行，只要数字在改变，因此表面上展现进度刷新
                print(f"\r游戏盒子加载中....   {loading}%", end="")
                # 由于没有放入复杂程序，如果直接打印，展示不出效果，因此用time.sleep模拟加载过程
                time.sleep(0.001)

                print("\n")
                time.sleep(1)
                caidan()

        # 游戏盒子菜单函数
        def caidan():
            print('小游戏盒子'.center(50, '*'))  # 用center将文字显示于中间，并用50各*字符填充制作基本菜单样式
            print('*'.ljust(53, ' '), '*')  # 用ljust左靠齐生成53各空格字符
            print('*', end='')
            print("1.猜拳游戏".center(49), end='')
            print('*')
            print('\n')
            print('*', end='')
            print("2.猜大小 ".center(49), end='')  ###################制作小游戏界面，同时采用time模块模拟游戏盒子的加载界面
            print(' *')
            print('*'.ljust(53, ' '), '*')  # 用ljust左靠齐生成53各空格字符
            print('*' * 54)  # 字符串*54就是输出54个相同字符串
            s = int(input("\n请选择一个游戏（输入0退出小游戏盒子T_T）:"))
            if s == 2:
                print('-----猜大小-----')
                caidaxiao()
            elif s == 1:
                print('---猜拳游戏----')
                caiquan()
            else:
                print('即将退出游戏盒子，欢迎下次游玩！')
                exit()

        ## 猜拳游戏函数
        def caiquan():
            import time
            t = 100
            for n in range(t + 1):
                loading = round(n / t * 100)
                # 通过加\r每次输出完跳回，用end=""替换默认的换行，只要数字在改变，因此表面上展现进度刷新
                print(f"\r加载中{loading}%", end="")
                # 由于没有放入复杂程序，如果直接打印，展示不出效果，因此用time.sleep模拟加载过程
                time.sleep(0.01)

            print('\n--------------猜拳游戏----------------\n\n')
            import random  # 导入随机模块

            ying = 0
            shu = 0
            while True:
                if shu == 2:
                    print('\n\n三局两胜  你输了！\n游戏结束！')
                    youxi()
                elif ying == 2:
                    print('\n\n三局两胜  你赢了！\n游戏结束！')
                    youxi()
                user = int(input('请出拳 0（石头） 1（剪刀） 2（布）：'))
                if user > 2:
                    print('没有这个手势哦！请重新输入！')
                else:
                    data = ['石头', '剪刀', '布']
                    com = random.randint(0, 2)
                    print('您出的是', data[user], '电脑出的是', data[com])
                    if user == com:
                        print('平局')
                        continue
                    elif (user == 0 and com == 1) or (user == 1 and com == 2) or (user == 2 and com == 0):
                        print('你赢了')
                        ying += 1
                    else:
                        print('你输了')
                        shu += 1

        # 是否进行新游戏的判断函数
        def youxi():
            q = int(input('是否继续游戏？\n键入0退出该游戏，返回游戏盒子\n键入1开始新游戏\n键入2直接退出整个游戏盒子\n'))
            if q == 0:
                caidan()
            elif q == 1:
                caiquan()
            elif q == 2:
                print('\n即将退出游戏盒子，欢迎下次游玩！\n')
                exit()

        def youxi1():
            q = int(input('是否继续游戏？\n键入0退出该游戏，返回游戏盒子\n键入1开始新游戏\n键入2直接退出整个游戏盒子\n'))
            if q == 0:
                caidan()
            elif q == 1:
                caidaxiao()
            elif q == 2:
                print('\n即将退出游戏盒子，欢迎下次游玩！\n')
                exit()

        ## 猜大小游戏函数
        def caidaxiao():
            import time
            import random
            # 让用户注册
            name = input('请填写用户名：')
            age = int(input('您好，请输入您年龄:'))
            user_info = {'name': name, 'age': age}  # 用户信息
            user_properties = ['X3 x1-5']  # 用于存放用户道具 默认道具
            properties = ['X3 (250G)', 'X1-5 (300G)']  # 道具列表 显示用

            # 根据用户年龄 给与不同的初始金币
            if 10 < user_info['age'] < 18:
                glod = 1000
            elif 18 <= user_info['age'] <= 30:
                glod = 1100
            else:
                glod = 500
            user_info['glod'] = glod

            # 输出相关提示信息
            print("{}您好，欢迎游玩本游戏，您的初始金币为：{}".format(user_info['name'], user_info['glod']))
            print("\n")
            time.sleep(1)
            print('游戏说明'.center(50, '*'))  # 用center将文字显示于中间，并用50各*字符填充制作基本菜单样式
            print('*'.ljust(53, ' '), '*')  # 用ljust左靠齐生成53各空格字符
            print('*', end='')
            print("电脑每次投掷三枚骰子，总点数>=10为大，否则为小".center(32), end='')
            print('*')
            print('*'.ljust(53, ' '), '*')  # 用ljust左靠齐生成53各空格字符
            print('*' * 54)  # 字符串*54就是输出54个相同字符串
            print("\n")

            # 开始游戏
            result = input('是否开始游戏 yes or no :  ')

            if (result.lower() == 'yes'):
                while True:
                    dices = []
                    # 开始投掷
                    for i in range(0, 3):
                        dices.append(random.randint(1, 6))
                    total = sum(dices)  # 计算总和
                    user_input = input('请输入big OR small : ')  # 等待用户输入
                    u_input = user_input.strip().lower()
                    time.sleep(1)
                    # 判断用户输入
                    print('骰子点数为：{}'.format(dices), end=' ')
                    if (total >= 10 and u_input == 'big') or (total < 10 and u_input == 'small'):
                        print('您赢了!!!')
                        multi = 1  # 倍数
                        if len(user_properties) > 0:  # 如果用户有道具 选择是否使用道具
                            use_pro = input('是否使用道具： ')
                            if use_pro.lower() == 'yes':
                                use_pro = int(input('请选择使用第几个道具{} ：'.format(user_properties)))
                                use_pro -= 1
                                # 判断道具类型
                                if user_properties[use_pro] == 'X 3':
                                    multi = 3
                                    print('奖金翻3倍')
                                elif user_properties[use_pro] == 'X 1-5':
                                    multi = random.randint(1, 5)
                                    print('奖金翻{}倍'.format(multi))
                                user_properties.remove(user_properties[use_pro])  # 删除道具
                        user_info['glod'] += 100 * multi;  # 金额增加
                    else:
                        print('您输了!')
                        user_info['glod'] -= 100;  # 错误 用户金币减 100
                    # 判断用户金币 是否够下次玩 不够则退出程序
                    if (user_info['glod'] <= 0):
                        print('您的金币已经用完，感谢您的游玩')
                        break
                    if user_info['glod'] % 1000 == 0:  # 用户金币 是1000的倍数是 可购买道具
                        shop = input('您现在有金币:{}，是否购买道具 yes or no: '.format(user_info['glod']))
                        if shop.lower() == 'yes':
                            good_num = int(input('请选择要购买第几个道具 {}'.format(properties)))
                            if good_num == 1:
                                user_properties.append('X 3')  # 给用户添加道具
                                user_info['glod'] -= 250
                                print('购买成功！消耗金币250')
                            elif good_num == 2:
                                user_properties.append('X 1-5')  # 给用户添加道具
                                user_info['glod'] -= 300  # 用户金币减 300
                                print('购买成功！消耗金币300')
                            else:
                                print('没有该道具，您失去了这次机会')
                    else:
                        print('您现在有金币:{} '.format(user_info['glod']))
            else:
                youxi1()

        ## 调用函数以进行游戏盒子程序
        youxihezi()

        ##程序结束
    def home():
        import pygame
        import sys
        import time
        pygame.init()
        pygame.font.init()
        x, y = pygame.mouse.get_pos()
        size = width,heigh = 400,680
        screen = pygame.display.set_mode(size=size)
        pygame.display.set_caption("游戏包")
        final_text1 = "按下0：小球游戏。"
        final_text2 = "按下1：flappybird。"
        final_text3 = "按下2：村民的末日。"
        final_text4 = "按下3：五子棋（人机）。"
        final_text5 = "按下4：五子棋（人人）。"
        final_text6 = "按下5：2048小游戏。"
        final_text7 = "按下6：贪吃蛇。"
        final_text8 = "按下7：俄罗斯方块"
        final_text9 = "按下8：游戏盒子"
        Quit = "按下Q退出游戏包"

        font1 = pygame.font.Font('./STSONG.TTF',20)
        ft1_surf = font1.render(final_text1, 1, (242, 3, 36))
        ft2_surf = font1.render(final_text2, 1, (242, 3, 36))
        ft3_surf = font1.render(final_text3, 1, (242, 3, 36))
        ft4_surf = font1.render(final_text4, 1, (242, 3, 36))
        ft5_surf = font1.render(final_text5, 1, (242, 3, 36))
        ft6_surf = font1.render(final_text6, 1, (242, 3, 36))
        ft7_surf = font1.render(final_text7, 1, (242, 3, 36))
        ft8_surf = font1.render(final_text8, 1, (242, 3, 36))
        ft9_surf = font1.render(final_text9, 1, (242, 3, 36))
        Quit_surf = font1.render(Quit, 1, (242, 3, 36))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_1]:
                    flappybird()
                elif keys_pressed[pygame.K_0]:
                    ball()
                elif keys_pressed[pygame.K_2]:
                    cunmin()
                elif keys_pressed[pygame.K_3]:
                    AI_five()
                elif keys_pressed[pygame.K_4]:
                    five()
                elif keys_pressed[pygame.K_5]:
                    g2048()
                elif keys_pressed[pygame.K_6]:
                    snack()
                elif keys_pressed[pygame.K_7]:
                    eluosi()
                elif keys_pressed[pygame.K_8]:
                    pygame.quit()
                    gamefox()
                    sys.exit()
                elif keys_pressed[pygame.K_q]:
                    pygame.quit()
                    num = 0
                    while not num == 100:
                        num+=1
                        time.sleep(0.01)
                        print(f"\r关闭中…… {num}%", end="")
                    print("")
                    print("关闭完成，游戏包欢迎您下次再来！")
                    time.sleep(1)
                    sys.exit()
            screen.blit(ft1_surf, [0, 0])
            screen.blit(ft2_surf, [0, 50])
            screen.blit(ft3_surf, [0, 100])
            screen.blit(ft4_surf, [0, 150])
            screen.blit(ft5_surf, [0, 200])
            screen.blit(ft6_surf, [0, 250])
            screen.blit(ft7_surf, [0, 300])
            screen.blit(ft8_surf, [0, 350])
            screen.blit(ft9_surf, [0, 400])
            screen.blit(Quit_surf, [0, 650])
            pygame.display.update()
    if __name__ == '__main__':
        home()
games()
