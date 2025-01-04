import pygame

width = 630
height = 630

class Resources:
    _instance = None

    @staticmethod
    def get_instance():
        if Resources._instance is None:
            Resources._instance = Resources()
        return Resources._instance

    def __init__(self):
        # 如果已经有实例存在，则直接返回，不做任何初始化
        if Resources._instance is not None:
            return

        self.bg_img = pygame.image.load("assets/images/others/background.png")
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))

        self.add_sound = pygame.mixer.Sound("assets/audios/add.wav")
        self.bang_sound = pygame.mixer.Sound("assets/audios/bang.wav")
        self.blast_sound = pygame.mixer.Sound("assets/audios/blast.wav")
        self.fire_sound = pygame.mixer.Sound("assets/audios/fire.wav")
        self.Gunfire_sound = pygame.mixer.Sound("assets/audios/Gunfire.wav")
        self.hit_sound = pygame.mixer.Sound("assets/audios/hit.wav")
        self.start_sound = pygame.mixer.Sound("assets/audios/start.wav")

        # 设置音效音量
        self.set_volume(1)

    def set_volume(self, volume):
        """设置所有音效的音量"""
        self.add_sound.set_volume(volume)
        self.bang_sound.set_volume(volume)
        self.blast_sound.set_volume(volume)
        self.fire_sound.set_volume(volume)
        self.Gunfire_sound.set_volume(volume)
        self.hit_sound.set_volume(volume)
        self.start_sound.set_volume(volume)
