# Poker Calculator (Python Version)

A Python 3 terminal-based poker probability calculator that helps you track cards and calculate hand probabilities in real-time.

## Features

- **Visual Card Tracking**: See all 52 cards displayed with suit symbols (♠ ♥ ♦ ♣)
- **Color-Coded Display**: Used cards appear dimmed, available cards are bright
- **Real-Time Probability Calculations**: Get instant probability updates for poker hands
- **Texas Hold'em Hand Analysis**: Calculates probabilities for all poker hands
- **Joker Support**: Includes both small (j) and large (J) jokers
- **Interactive Interface**: Easy card entry and management
- **Pure Python**: No external dependencies required

## Requirements

- Python 3.6 or higher
- Terminal with ANSI color support (most modern terminals)

## Installation

No installation required! The program uses only Python standard library.

```bash
# Make the script executable (optional)
chmod +x poker_calculator.py
```

## How to Use

### Starting the Program

```bash
# Run directly
python3 poker_calculator.py

# Or if executable
./poker_calculator.py
```

### Card Entry Format

Enter cards using the format: `<suit><rank>`

**Suits** (lowercase letter):
- `s` - Spade (♠)
- `h` - Heart (♥)
- `d` - Diamond (♦)
- `c` - Club (♣)

**Ranks**:
- `A` or `a` - Ace
- `2` through `10` - Number cards
- `J` - Jack (11)
- `Q` - Queen (12)
- `K` - King (13)

**Jokers**:
- `j` - Small joker
- `J` - Large joker

### Examples

```
h8    - Eight of Hearts
sA    - Ace of Spades
d10   - Ten of Diamonds
cK    - King of Clubs
h2    - Two of Hearts
sJ    - Jack of Spades
dQ    - Queen of Diamonds
c3    - Three of Clubs
j     - Small Joker
J     - Large Joker
```

### Commands

- **Enter a card**: Type the card code (e.g., `h8`, `sA`)
- **`reset`** or **`r`**: Clear all selected cards and start over
- **`undo`** or **`u`**: Remove the last entered card
- **`quit`**, **`q`**, or **`exit`**: Exit the program
- **Ctrl+C**: Emergency exit

## Display Explanation

### Card Display

The screen shows all cards organized by suit:

```
♠ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♥ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♦ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♣ | A  2  3  4  5  6  7  8  9 10  J  Q  K
★ | j  J
```

- **Bright colors**: Available cards (not yet selected)
- **Dimmed colors**: Used/selected cards
- **Red suits**: Hearts (♥) and Diamonds (♦)
- **Black suits**: Spades (♠) and Clubs (♣)

### Probability Display

The program shows:

1. **Number of cards selected**: How many cards you've entered
2. **Cards available**: How many cards remain unselected
3. **Hand probabilities**: Chances of getting different poker hands
4. **Drawing to**: What hands you're currently building toward

### Poker Hands (Ranked)

From highest to lowest:

1. **Royal Flush**: A-K-Q-J-10 of the same suit
2. **Straight Flush**: Five consecutive cards of the same suit
3. **Four of a Kind**: Four cards of the same rank
4. **Full House**: Three of a kind + a pair
5. **Flush**: Five cards of the same suit
6. **Straight**: Five consecutive cards (any suit)
7. **Three of a Kind**: Three cards of the same rank
8. **Two Pair**: Two different pairs
9. **One Pair**: Two cards of the same rank
10. **High Card**: No matching cards

## Usage Example

### Session Example

```
=== POKER CALCULATOR ===

♠ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♥ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♦ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♣ | A  2  3  4  5  6  7  8  9 10  J  Q  K
★ | j  J

Selected Cards: None

=== PROBABILITIES ===
Cards selected: 0
Cards available: 52

Enter command: h8

[Display updates showing 8 of Hearts dimmed]

Selected Cards: ♥8

=== PROBABILITIES ===
Cards selected: 1
Cards available: 51

Drawing to:
- Any hand possible

Enter command: hK

[Display updates showing King of Hearts dimmed]

Selected Cards: ♥8 ♥K

=== PROBABILITIES ===
Cards selected: 2
Cards available: 50

Drawing to:
- Possible Flush Draw

Enter command: h2

[Continues building hand...]
```

## Tips

1. **Track opponent's cards**: Enter cards you've seen to calculate what's left
2. **Calculate outs**: See what cards remain to complete your hand
3. **Use reset often**: Start fresh for new hands with `reset`
4. **Undo mistakes**: Made an error? Use `undo` to remove the last card
5. **Watch for draws**: The program shows what you're drawing to (flush, straight, etc.)
6. **Exit quickly**: Press Ctrl+C to exit at any time

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (uses standard library only)
- **Display**: ANSI escape codes for colors and formatting
- **Probability Calculation**: Combinatorial analysis
- **Platform**: Linux/macOS/Windows (with ANSI support)
- **Code Style**: Type hints, enums, and object-oriented design

## Python-Specific Features

- **Type Hints**: Full type annotations for better code clarity
- **Enums**: Clean enum-based suit representation
- **List Comprehensions**: Efficient card filtering
- **Counter**: Built-in collections for rank counting
- **Graceful Exit**: Handles Ctrl+C cleanly

## Troubleshooting

### Colors not displaying?
- Ensure your terminal supports ANSI colors
- On Windows, use Windows Terminal or enable ANSI support
- Try running in a different terminal emulator

### Cards not registering?
- Check format: suit letter (lowercase) + rank
- Ensure card hasn't already been used
- Use `reset` to clear and start over

### Probability seems off?
- The program uses theoretical Texas Hold'em probabilities
- Probabilities change as you select more cards

### Python version error?
```bash
# Check your Python version
python3 --version

# Should be 3.6 or higher
```

## Differences from C++ Version

The Python version offers the same functionality as the C++ version with these differences:

- **No compilation required**: Run directly with Python interpreter
- **Platform independent**: Works on any system with Python 3.6+
- **More readable code**: Python's syntax makes the logic clearer
- **Type hints**: Optional type annotations for better IDE support
- **Same features**: All functionality is identical to C++ version

## Notes

- Jokers are displayed but excluded from probability calculations
- The calculator assumes a standard 52-card deck
- Probabilities are based on 5-card poker hands
- The program uses bright/dim colors to show card availability
- Uses only Python standard library - no pip install needed

## License

See LICENSE file in the repository root for details.

## Contributing

Feel free to submit issues or pull requests to improve the calculator!
