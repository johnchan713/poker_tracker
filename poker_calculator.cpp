#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>

// ANSI color codes
#define RESET   "\033[0m"
#define RED     "\033[91m"
#define BLACK   "\033[90m"
#define DIM_RED "\033[2;91m"
#define DIM_BLACK "\033[2;90m"
#define BOLD    "\033[1m"
#define CLEAR   "\033[2J\033[H"

// Card suits
enum Suit { SPADE, HEART, DIAMOND, CLUB, JOKER };

// Card structure
struct Card {
    Suit suit;
    int rank;  // 1-13 for regular cards, 14-15 for jokers
    bool used;

    Card(Suit s, int r) : suit(s), rank(r), used(false) {}

    std::string getSuitSymbol() const {
        switch(suit) {
            case SPADE:   return "♠";
            case HEART:   return "♥";
            case DIAMOND: return "♦";
            case CLUB:    return "♣";
            case JOKER:   return "★";
            default:      return "?";
        }
    }

    std::string getSuitColor() const {
        if (used) {
            return (suit == HEART || suit == DIAMOND) ? DIM_RED : DIM_BLACK;
        } else {
            return (suit == HEART || suit == DIAMOND) ? RED : BLACK;
        }
    }

    std::string getRankString() const {
        if (rank == 1) return "A";
        if (rank == 11) return "J";
        if (rank == 12) return "Q";
        if (rank == 13) return "K";
        if (rank == 14) return "j"; // small joker
        if (rank == 15) return "J"; // large joker
        return std::to_string(rank);
    }
};

// Deck class
class PokerDeck {
private:
    std::vector<Card> cards;
    std::vector<Card> selectedCards;

public:
    PokerDeck() {
        // Initialize 52 cards
        for (int suit = SPADE; suit <= CLUB; suit++) {
            for (int rank = 1; rank <= 13; rank++) {
                cards.push_back(Card(static_cast<Suit>(suit), rank));
            }
        }
        // Add jokers
        cards.push_back(Card(JOKER, 14)); // small joker
        cards.push_back(Card(JOKER, 15)); // large joker
    }

    bool selectCard(char suitChar, std::string rankStr) {
        Suit suit;
        int rank;

        // Handle jokers
        if (suitChar == 'j' && rankStr.empty()) {
            suit = JOKER;
            rank = 14; // small joker
        } else if (suitChar == 'J' && rankStr.empty()) {
            suit = JOKER;
            rank = 15; // large joker
        } else {
            // Parse suit
            switch(suitChar) {
                case 's': suit = SPADE; break;
                case 'h': suit = HEART; break;
                case 'd': suit = DIAMOND; break;
                case 'c': suit = CLUB; break;
                default: return false;
            }

            // Parse rank
            if (rankStr == "A" || rankStr == "a") {
                rank = 1;
            } else if (rankStr == "J") {
                rank = 11;
            } else if (rankStr == "Q") {
                rank = 12;
            } else if (rankStr == "K") {
                rank = 13;
            } else {
                try {
                    rank = std::stoi(rankStr);
                    if (rank < 1 || rank > 13) return false;
                } catch (...) {
                    return false;
                }
            }
        }

        // Find and mark card as used
        for (auto& card : cards) {
            if (card.suit == suit && card.rank == rank && !card.used) {
                card.used = true;
                selectedCards.push_back(card);
                return true;
            }
        }
        return false;
    }

    void display() const {
        std::cout << CLEAR;
        std::cout << BOLD << "=== POKER CARD TRACKER ===" << RESET << "\n\n";

        // Display each suit
        displaySuit(SPADE);
        displaySuit(HEART);
        displaySuit(DIAMOND);
        displaySuit(CLUB);
        displayJokers();

        // Show statistics
        int usedCount = 0;
        int availableCount = 0;
        for (const auto& card : cards) {
            if (card.suit != JOKER) {
                if (card.used) usedCount++;
                else availableCount++;
            }
        }

        std::cout << "\n" << BOLD << "Cards Used: " << RESET << usedCount << " / 52";
        std::cout << "  |  " << BOLD << "Available: " << RESET << availableCount << "\n";

        std::cout << "\n" << BOLD << "Selected Cards: " << RESET;
        if (selectedCards.empty()) {
            std::cout << "None\n";
        } else {
            for (const auto& card : selectedCards) {
                std::cout << card.getSuitColor() << card.getSuitSymbol()
                          << card.getRankString() << RESET << " ";
            }
            std::cout << "\n";
        }
    }

    void displaySuit(Suit suit) const {
        Card sample(suit, 1);
        std::cout << sample.getSuitSymbol() << " | ";

        for (int rank = 1; rank <= 13; rank++) {
            auto it = std::find_if(cards.begin(), cards.end(),
                [suit, rank](const Card& c) {
                    return c.suit == suit && c.rank == rank;
                });

            if (it != cards.end()) {
                std::cout << it->getSuitColor() << std::setw(2)
                          << it->getRankString() << RESET << " ";
            }
        }
        std::cout << "\n";
    }

    void displayJokers() const {
        std::cout << "★ | ";
        for (int rank = 14; rank <= 15; rank++) {
            auto it = std::find_if(cards.begin(), cards.end(),
                [rank](const Card& c) {
                    return c.suit == JOKER && c.rank == rank;
                });

            if (it != cards.end()) {
                std::cout << it->getSuitColor() << std::setw(2)
                          << it->getRankString() << RESET << " ";
            }
        }
        std::cout << "\n";
    }

    void reset() {
        for (auto& card : cards) {
            card.used = false;
        }
        selectedCards.clear();
    }

    bool removeLastCard() {
        if (selectedCards.empty()) return false;

        Card lastCard = selectedCards.back();
        selectedCards.pop_back();

        for (auto& card : cards) {
            if (card.suit == lastCard.suit && card.rank == lastCard.rank) {
                card.used = false;
                return true;
            }
        }
        return false;
    }
};

int main() {
    PokerDeck deck;

    std::cout << BOLD << "Welcome to Poker Card Tracker!" << RESET << "\n";
    std::cout << "Track which cards have been played.\n\n";
    std::cout << "Commands:\n";
    std::cout << "  Enter card: <suit><rank> (e.g., h8, sA, d10, cK)\n";
    std::cout << "    Suits: s(spade), h(heart), d(diamond), c(club)\n";
    std::cout << "    Ranks: A,2,3,4,5,6,7,8,9,10,J,Q,K\n";
    std::cout << "  Jokers: j (small), J (large)\n";
    std::cout << "  Commands: reset, undo, quit\n";
    std::cout << "\nPress Enter to continue...";
    std::cin.get();

    while (true) {
        deck.display();

        std::cout << "\n" << BOLD << "Enter card or command: " << RESET;
        std::string input;
        std::getline(std::cin, input);

        // Trim whitespace
        input.erase(0, input.find_first_not_of(" \t\n\r"));
        input.erase(input.find_last_not_of(" \t\n\r") + 1);

        if (input.empty()) continue;

        if (input == "quit" || input == "q" || input == "exit") {
            break;
        } else if (input == "reset" || input == "r") {
            deck.reset();
        } else if (input == "undo" || input == "u") {
            if (!deck.removeLastCard()) {
                std::cout << "No cards to undo!\n";
                std::cout << "Press Enter to continue...";
                std::cin.get();
            }
        } else if (input == "j" || input == "J") {
            // Handle jokers
            if (!deck.selectCard(input[0], "")) {
                std::cout << "Invalid joker or already used!\n";
                std::cout << "Press Enter to continue...";
                std::cin.get();
            }
        } else if (input.length() >= 2) {
            // Parse card input
            char suit = input[0];
            std::string rank = input.substr(1);

            if (!deck.selectCard(suit, rank)) {
                std::cout << "Invalid card or already used!\n";
                std::cout << "Press Enter to continue...";
                std::cin.get();
            }
        } else {
            std::cout << "Invalid input!\n";
            std::cout << "Press Enter to continue...";
            std::cin.get();
        }
    }

    std::cout << CLEAR;
    std::cout << "Thanks for using Poker Card Tracker!\n";

    return 0;
}
