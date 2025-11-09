#!/usr/bin/env python3
"""
Poker Card Tracker - A terminal-based card tracking system
Displays all 52 cards with visual indicators for used/available cards
"""

import sys
from enum import Enum
from typing import List


# ANSI color codes
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    BLACK = "\033[90m"
    DIM_RED = "\033[2;91m"
    DIM_BLACK = "\033[2;90m"
    BOLD = "\033[1m"
    CLEAR = "\033[2J\033[H"


class Suit(Enum):
    """Card suits"""
    SPADE = 0
    HEART = 1
    DIAMOND = 2
    CLUB = 3
    JOKER = 4

    def get_symbol(self) -> str:
        """Get suit symbol"""
        symbols = {
            Suit.SPADE: "♠",
            Suit.HEART: "♥",
            Suit.DIAMOND: "♦",
            Suit.CLUB: "♣",
            Suit.JOKER: "★"
        }
        return symbols[self]

    def is_red(self) -> bool:
        """Check if suit is red"""
        return self in (Suit.HEART, Suit.DIAMOND)


class Card:
    """Represents a playing card"""

    def __init__(self, suit: Suit, rank: int):
        self.suit = suit
        self.rank = rank  # 1-13 for regular cards, 14-15 for jokers
        self.used = False

    def get_suit_color(self) -> str:
        """Get ANSI color code for this card"""
        if self.used:
            return Color.DIM_RED if self.suit.is_red() else Color.DIM_BLACK
        else:
            return Color.RED if self.suit.is_red() else Color.BLACK

    def get_rank_string(self) -> str:
        """Get string representation of rank"""
        rank_map = {
            1: "A",
            11: "J",
            12: "Q",
            13: "K",
            14: "j",  # small joker
            15: "J"   # large joker
        }
        return rank_map.get(self.rank, str(self.rank))

    def __str__(self) -> str:
        return f"{self.get_suit_color()}{self.suit.get_symbol()}{self.get_rank_string()}{Color.RESET}"

    def __repr__(self) -> str:
        return f"Card({self.suit}, {self.rank})"


class PokerDeck:
    """Manages a deck of cards"""

    def __init__(self):
        self.cards: List[Card] = []
        self.selected_cards: List[Card] = []
        self._initialize_deck()

    def _initialize_deck(self):
        """Initialize a standard 52-card deck plus jokers"""
        # Add regular cards
        for suit in [Suit.SPADE, Suit.HEART, Suit.DIAMOND, Suit.CLUB]:
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

        # Add jokers
        self.cards.append(Card(Suit.JOKER, 14))  # small joker
        self.cards.append(Card(Suit.JOKER, 15))  # large joker

    def select_card(self, suit_char: str, rank_str: str = "") -> bool:
        """
        Select a card from the deck

        Args:
            suit_char: Suit character (s/h/d/c/j/J)
            rank_str: Rank string (A/2-10/J/Q/K or empty for jokers)

        Returns:
            True if card was successfully selected, False otherwise
        """
        # Handle jokers
        if suit_char == 'j' and not rank_str:
            suit = Suit.JOKER
            rank = 14  # small joker
        elif suit_char == 'J' and not rank_str:
            suit = Suit.JOKER
            rank = 15  # large joker
        else:
            # Parse suit
            suit_map = {
                's': Suit.SPADE,
                'h': Suit.HEART,
                'd': Suit.DIAMOND,
                'c': Suit.CLUB
            }
            suit = suit_map.get(suit_char)
            if suit is None:
                return False

            # Parse rank
            if rank_str.upper() == 'A':
                rank = 1
            elif rank_str == 'J':
                rank = 11
            elif rank_str == 'Q':
                rank = 12
            elif rank_str == 'K':
                rank = 13
            else:
                try:
                    rank = int(rank_str)
                    if rank < 1 or rank > 13:
                        return False
                except ValueError:
                    return False

        # Find and mark card as used
        for card in self.cards:
            if card.suit == suit and card.rank == rank and not card.used:
                card.used = True
                self.selected_cards.append(card)
                return True

        return False

    def display(self):
        """Display all cards in the deck"""
        print(Color.CLEAR)
        print(f"{Color.BOLD}=== POKER CARD TRACKER ==={Color.RESET}\n")

        # Display each suit
        for suit in [Suit.SPADE, Suit.HEART, Suit.DIAMOND, Suit.CLUB]:
            self._display_suit(suit)

        # Display jokers
        self._display_jokers()

        # Show statistics
        used_count = sum(1 for card in self.cards if card.used and card.suit != Suit.JOKER)
        available_count = sum(1 for card in self.cards if not card.used and card.suit != Suit.JOKER)

        print(f"\n{Color.BOLD}Cards Used: {Color.RESET}{used_count} / 52", end="")
        print(f"  |  {Color.BOLD}Available: {Color.RESET}{available_count}")

        # Display selected cards
        print(f"\n{Color.BOLD}Selected Cards: {Color.RESET}", end="")
        if not self.selected_cards:
            print("None")
        else:
            for card in self.selected_cards:
                print(card, end=" ")
            print()

    def _display_suit(self, suit: Suit):
        """Display all cards of a specific suit"""
        print(f"{suit.get_symbol()} | ", end="")

        for rank in range(1, 14):
            card = next((c for c in self.cards if c.suit == suit and c.rank == rank), None)
            if card:
                print(f"{card.get_suit_color()}{card.get_rank_string():>2}{Color.RESET} ", end="")

        print()

    def _display_jokers(self):
        """Display jokers"""
        print(f"{Suit.JOKER.get_symbol()} | ", end="")

        for rank in [14, 15]:
            card = next((c for c in self.cards if c.suit == Suit.JOKER and c.rank == rank), None)
            if card:
                print(f"{card.get_suit_color()}{card.get_rank_string():>2}{Color.RESET} ", end="")

        print()

    def reset(self):
        """Reset all cards to unused state"""
        for card in self.cards:
            card.used = False
        self.selected_cards.clear()

    def remove_last_card(self) -> bool:
        """Remove the last selected card"""
        if not self.selected_cards:
            return False

        last_card = self.selected_cards.pop()

        for card in self.cards:
            if card.suit == last_card.suit and card.rank == last_card.rank:
                card.used = False
                return True

        return False


def main():
    """Main program loop"""
    deck = PokerDeck()

    print(f"{Color.BOLD}Welcome to Poker Card Tracker!{Color.RESET}")
    print("Track which cards have been played.\n")
    print("Commands:")
    print("  Enter card: <suit><rank> (e.g., h8, sA, d10, cK)")
    print("    Suits: s(spade), h(heart), d(diamond), c(club)")
    print("    Ranks: A,2,3,4,5,6,7,8,9,10,J,Q,K")
    print("  Jokers: j (small), J (large)")
    print("  Commands: reset, undo, quit")
    print("\nPress Enter to continue...")
    input()

    while True:
        deck.display()

        print(f"\n{Color.BOLD}Enter card or command: {Color.RESET}", end="")
        user_input = input().strip()

        if not user_input:
            continue

        # Handle commands
        if user_input.lower() in ('quit', 'q', 'exit'):
            break
        elif user_input.lower() in ('reset', 'r'):
            deck.reset()
        elif user_input.lower() in ('undo', 'u'):
            if not deck.remove_last_card():
                print("No cards to undo!")
                input("Press Enter to continue...")
        elif user_input in ('j', 'J'):
            # Handle jokers
            if not deck.select_card(user_input, ""):
                print("Invalid joker or already used!")
                input("Press Enter to continue...")
        elif len(user_input) >= 2:
            # Parse card input
            suit_char = user_input[0]
            rank_str = user_input[1:]

            if not deck.select_card(suit_char, rank_str):
                print("Invalid card or already used!")
                input("Press Enter to continue...")
        else:
            print("Invalid input!")
            input("Press Enter to continue...")

    print(Color.CLEAR)
    print("Thanks for using Poker Card Tracker!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.CLEAR}Thanks for using Poker Card Tracker!")
        sys.exit(0)
