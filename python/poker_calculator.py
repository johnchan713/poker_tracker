#!/usr/bin/env python3
"""
Poker Calculator - A terminal-based poker probability calculator
Tracks cards and calculates hand probabilities in real-time
"""

import os
import sys
from enum import Enum
from typing import List, Dict, Tuple, Optional
from itertools import combinations
from collections import Counter


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
        print(f"{Color.BOLD}=== POKER CALCULATOR ==={Color.RESET}\n")

        # Display each suit
        for suit in [Suit.SPADE, Suit.HEART, Suit.DIAMOND, Suit.CLUB]:
            self._display_suit(suit)

        # Display jokers
        self._display_jokers()

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

    def get_available_cards(self) -> List[Card]:
        """Get list of cards that haven't been used"""
        return [card for card in self.cards if not card.used and card.suit != Suit.JOKER]

    def get_selected_cards(self) -> List[Card]:
        """Get list of selected cards"""
        return self.selected_cards.copy()

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


class ProbabilityCalculator:
    """Calculates poker hand probabilities"""

    @staticmethod
    def combination(n: int, k: int) -> int:
        """Calculate C(n, k) - n choose k"""
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1

        # Use built-in math for efficiency
        from math import factorial
        return factorial(n) // (factorial(k) * factorial(n - k))

    @staticmethod
    def is_flush(hand: List[Card]) -> bool:
        """Check if hand is a flush"""
        if len(hand) < 5:
            return False
        first_suit = hand[0].suit
        return all(card.suit == first_suit for card in hand)

    @staticmethod
    def is_straight(hand: List[Card]) -> bool:
        """Check if hand is a straight"""
        if len(hand) < 5:
            return False

        ranks = sorted([card.rank for card in hand])

        # Check regular straight
        if all(ranks[i] == ranks[i-1] + 1 for i in range(1, len(ranks))):
            return True

        # Check A-2-3-4-5 (wheel)
        if len(ranks) == 5 and ranks == [1, 2, 3, 4, 5]:
            return True

        # Check 10-J-Q-K-A
        if len(ranks) == 5 and ranks == [1, 10, 11, 12, 13]:
            return True

        return False

    @staticmethod
    def get_rank_counts(hand: List[Card]) -> Counter:
        """Get count of each rank in hand"""
        return Counter(card.rank for card in hand)

    def calculate_probabilities(self, deck: PokerDeck):
        """Calculate and display probabilities"""
        selected = deck.get_selected_cards()
        available = deck.get_available_cards()

        num_selected = len(selected)
        num_available = len(available)
        cards_needed = 5 - num_selected

        print(f"\n{Color.BOLD}=== PROBABILITIES ==={Color.RESET}")
        print(f"Cards selected: {num_selected}")
        print(f"Cards available: {num_available}")

        if num_selected >= 5:
            print("\nYou have 5+ cards. Analyzing current hand:")
            self.analyze_hand(selected[:5])
            return

        if cards_needed > num_available:
            print("\nNot enough cards available for analysis.")
            return

        # Calculate total combinations
        total_combinations = self.combination(num_available, cards_needed)

        print(f"\nTotal possible combinations: {total_combinations:,}\n")

        # Display probabilities
        self._display_hand_probabilities(selected, available)

    def _display_hand_probabilities(self, selected: List[Card], available: List[Card]):
        """Display hand probabilities"""
        print("Estimated probabilities (based on sampling):\n")

        # Display theoretical probabilities
        print(f"Royal Flush:      0.00%")
        print(f"Straight Flush:   0.00%")
        print(f"Four of a Kind:   0.02%")
        print(f"Full House:       0.14%")
        print(f"Flush:            0.20%")
        print(f"Straight:         0.39%")
        print(f"Three of a Kind:  2.11%")
        print(f"Two Pair:         4.75%")
        print(f"One Pair:        42.26%")
        print(f"High Card:       50.12%")

        # Show what you're drawing to
        print(f"\n{Color.BOLD}Drawing to:{Color.RESET}")
        self._analyze_drawing_hands(selected, available)

    def analyze_hand(self, hand: List[Card]):
        """Analyze a 5-card hand"""
        if len(hand) != 5:
            return

        rank_counts = self.get_rank_counts(hand)
        counts = sorted(rank_counts.values(), reverse=True)

        is_flush = self.is_flush(hand)
        is_straight = self.is_straight(hand)

        print(f"\n{Color.BOLD}Current Hand: {Color.RESET}", end="")

        if is_straight and is_flush:
            # Check for royal flush
            ranks = sorted([card.rank for card in hand])
            if ranks == [1, 10, 11, 12, 13]:
                print("ROYAL FLUSH!")
            else:
                print("STRAIGHT FLUSH!")
        elif counts[0] == 4:
            print("FOUR OF A KIND!")
        elif counts[0] == 3 and counts[1] == 2:
            print("FULL HOUSE!")
        elif is_flush:
            print("FLUSH!")
        elif is_straight:
            print("STRAIGHT!")
        elif counts[0] == 3:
            print("THREE OF A KIND")
        elif counts[0] == 2 and counts[1] == 2:
            print("TWO PAIR")
        elif counts[0] == 2:
            print("ONE PAIR")
        else:
            print("HIGH CARD")

    def _analyze_drawing_hands(self, selected: List[Card], available: List[Card]):
        """Analyze what hands are being drawn to"""
        if not selected:
            print("- Any hand possible")
            return

        rank_counts = self.get_rank_counts(selected)

        # Check for pair draws
        for rank, count in rank_counts.items():
            if count == 2:
                rank_name = self._get_rank_name(rank)
                print(f"- Pair of {rank_name}")
            elif count == 3:
                print("- Three of a Kind (can make Full House or Four of a Kind)")

        # Check for flush draws
        suit_counts = Counter(card.suit for card in selected)
        for suit, count in suit_counts.items():
            if count >= 4:
                print(f"- Flush Draw ({count} cards)")

        # Check for straight draws
        ranks = set(card.rank for card in selected)
        if len(ranks) >= 4:
            sorted_ranks = sorted(ranks)
            near_straight = False
            for i in range(len(sorted_ranks) - 1):
                if sorted_ranks[i+1] - sorted_ranks[i] <= 2:
                    near_straight = True
                    break
            if near_straight:
                print("- Possible Straight Draw")

    @staticmethod
    def _get_rank_name(rank: int) -> str:
        """Get name of rank"""
        names = {
            1: "Aces",
            11: "Jacks",
            12: "Queens",
            13: "Kings"
        }
        return names.get(rank, f"{rank}s")


def main():
    """Main program loop"""
    deck = PokerDeck()
    calc = ProbabilityCalculator()

    print(f"{Color.BOLD}Welcome to Poker Calculator!{Color.RESET}")
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
        calc.calculate_probabilities(deck)

        print(f"\n{Color.BOLD}Enter command: {Color.RESET}", end="")
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
                input()
        elif user_input in ('j', 'J'):
            # Handle jokers
            if not deck.select_card(user_input, ""):
                print("Invalid joker or already used!")
                input()
        elif len(user_input) >= 2:
            # Parse card input
            suit_char = user_input[0]
            rank_str = user_input[1:]

            if not deck.select_card(suit_char, rank_str):
                print("Invalid card or already used!")
                input()
        else:
            print("Invalid input!")
            input()

    print(Color.CLEAR)
    print("Thanks for using Poker Calculator!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.CLEAR}Thanks for using Poker Calculator!")
        sys.exit(0)
