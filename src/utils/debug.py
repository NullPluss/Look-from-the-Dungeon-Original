def draw_fps(screen, clock, font):
    fps = int(clock.get_fps())
    text = font.render(f"FPS: {fps}", True, (255,255,255))
    screen.blit(text, (10,10))

def log(msg):
    print(f"[DEBUG] {msg}")