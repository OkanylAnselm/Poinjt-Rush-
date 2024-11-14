import pygame
import random

# Initialize Pygame
pygame.init()

full_screen = False
screen_info = pygame.display.Info()
full_width, full_height = screen_info.current_w, screen_info.current_h
half_width, half_height = full_width // 2, full_height // 2

# Display starting at half screen size
width, height = half_width, half_height  # Set initial dimensions
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ideclare")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARD_COLOR = (34, 139, 34)  # Green

# Card Variables
card_width, card_height = 100, 150
card_spacing = 20

# Game Variables
player_score = 0
ai_score = 0
win_condition = 20  # Score needed to win
deck = list(range(1, 11))  # Unique values from 1 to 10
random.shuffle(deck)  # Shuffle the deck

# Function to draw cards
def draw_cards(font):
    x = card_spacing
    for i, card_value in enumerate(deck):
        card_rect = pygame.Rect(x, height // 2 - card_height // 2, card_width, card_height)
        pygame.draw.rect(win, CARD_COLOR, card_rect)
        pygame.draw.rect(win, BLACK, card_rect, 3)  # Border around card
        text = font.render(str(card_value), True, WHITE)
        win.blit(text, (x + card_width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        x += card_width + card_spacing

# Function to display winning screen
def show_winner(font, winner):
    win.fill((0, 128, 128))  # Clear screen
    win_text = font.render(f"{winner} Wins!", True, WHITE)
    win.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # Show winning screen for 2 seconds

# Main game loop
def main():
    global player_score, ai_score, full_screen, win, width, height
    run = True
    font = pygame.font.SysFont(None, 36)
    player_turn = True  # Start with the player's turn

    while run and deck:  # Continue until the deck is empty
        win.fill((0, 128, 128))  # Background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # Toggle full screen when 'F' key is pressed
                if event.key == pygame.K_f:
                    full_screen = not full_screen
                    if full_screen:
                        width, height = full_width, full_height
                        win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        width, height = half_width, half_height
                        win = pygame.display.set_mode((width, height))
                # Optionally press ESC to exit full screen or end game
                elif event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, card_value in enumerate(deck):
                    x = i * (card_width + card_spacing) + card_spacing
                    card_rect = pygame.Rect(x, height // 2 - card_height // 2, card_width, card_height)
                    if card_rect.collidepoint(mouse_x, mouse_y):
                        player_score += card_value  # Add card value to player score
                        deck.pop(i)  # Remove the card from the deck
                        player_turn = False  # Switch to AI's turn
                        break

        # AI's turn
        if not player_turn and deck:
            ai_choice = random.choice(deck)
            ai_score += ai_choice  # Add selected card value to AI score
            deck.remove(ai_choice)  # Remove the card from the deck
            player_turn = True  # Switch back to player's turn

        # Draw cards, score, and game status
        draw_cards(font)
        score_text = font.render(f"Player Score: {player_score} | AI Score: {ai_score}", True, WHITE)
        win.blit(score_text, (50, 50))  # Display scores at the top-left corner

        # Check win conditions
        if player_score >= win_condition:
            show_winner(font, "Player")
            run = False
        elif ai_score >= win_condition:
            show_winner(font, "AI")
            run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
