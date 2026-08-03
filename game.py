class Game(object):
    # 定义一个类记录总积分
    top_score = 0

    def __init__(self, name):
        self.player_name = name

    @staticmethod
    def show_help():
        print('help')

    @classmethod
    def show_all_score(cls):
        print(f'总分为{cls.all_score()}')

    # 定义成员方法: 玩家玩游戏
    def start_game(self):
        print(f"{self.name}玩家玩了一局,总积分+1")
