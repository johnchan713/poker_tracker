# Poker Card Tracker (Python Version)

A Python 3 terminal-based card tracking system that helps you keep track of which cards have been played.

## Features

- **Visual Card Tracking**: See all 52 cards displayed with suit symbols (♠ ♥ ♦ ♣)
- **Color-Coded Display**: Used cards appear dimmed, available cards are bright
- **Real-Time Updates**: Card table updates immediately as you enter cards
- **Card Statistics**: Shows count of used/available cards
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

### Statistics Display

The program shows:

1. **Cards Used**: How many cards have been selected (out of 52)
2. **Available**: How many cards remain unselected
3. **Selected Cards**: List of all cards entered in order

## Usage Example

### Session Example

```
=== POKER CARD TRACKER ===

♠ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♥ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♦ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♣ | A  2  3  4  5  6  7  8  9 10  J  Q  K
★ | j  J

Cards Used: 0 / 52  |  Available: 52

Selected Cards: None

Enter card or command: h8

[Display updates showing 8 of Hearts dimmed]

=== POKER CARD TRACKER ===

♠ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♥ | A  2  3  4  5  6  7  8  9 10  J  Q  K (8 is dimmed)
♦ | A  2  3  4  5  6  7  8  9 10  J  Q  K
♣ | A  2  3  4  5  6  7  8  9 10  J  Q  K
★ | j  J

Cards Used: 1 / 52  |  Available: 51

Selected Cards: ♥8

Enter card or command: sA

[Display updates showing Ace of Spades dimmed]

Cards Used: 2 / 52  |  Available: 50

Selected Cards: ♥8 ♠A

[Continues tracking cards...]
```

## Tips

1. **Track all visible cards**: Enter any cards you can see on the table or in hands
2. **See what's left**: Bright cards show which cards are still available
3. **Use reset often**: Start fresh for new hands with `reset`
4. **Undo mistakes**: Made an error? Use `undo` to remove the last card
5. **Quick reference**: The counter shows exactly how many cards are left
6. **Exit quickly**: Press Ctrl+C to exit at any time

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (uses standard library only)
- **Display**: ANSI escape codes for colors and formatting
- **Card Tracking**: Real-time status updates
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

- Jokers are displayed for tracking but not counted in the 52-card statistics
- The tracker supports a standard 52-card deck
- Cards update in real-time as you enter them
- The program uses bright/dim colors to show card availability
- Uses only Python standard library - no pip install needed

## License

See LICENSE file in the repository root for details.

## Contributing

Feel free to submit issues or pull requests to improve the tracker!
