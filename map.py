import pygame

class Map:
    
    def Central_hill(screen:pygame.display):
        pygame.draw.rect(screen, (100, 100, 100), (200, 400, 50, 100))  # Left obstacle
        pygame.draw.rect(screen, (100, 100, 100), (750, 400, 50, 100))  # Right obstacle
        pygame.draw.polygon(screen, (139, 69, 19), [(400, 500), (500, 450), (600, 500)])  # Central hill
        
    def Canyon_with_bridges(screen):
        pygame.draw.rect(screen, (139, 69, 19), (150, 450, 50, 150))  # Left cliff
        pygame.draw.rect(screen, (139, 69, 19), (800, 450, 50, 150))  # Right cliff
        pygame.draw.rect(screen, (0, 0, 255), (300, 550, 400, 100))  # Canyon
        pygame.draw.rect(screen, (169, 169, 169), (450, 500, 100, 10))  # Bridge over the canyon
    
    def Forest_Battle(screen):
        pygame.draw.rect(screen, (100, 100, 100), (100, 450, 50, 100))  # Left bunker
        pygame.draw.rect(screen, (100, 100, 100), (850, 450, 50, 100))  # Right bunker
        tree_positions = [(400, 400), (500, 350), (600, 450), (450, 250), (550, 500)]
        for pos in tree_positions:
            pygame.draw.circle(screen, (34, 139, 34), pos, 30)  # Tree (small green circle)

