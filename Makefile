# Makefile for Poker Calculator

CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
TARGET = poker_calculator
SOURCE = poker_calculator.cpp

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

help:
	@echo "Poker Calculator Makefile"
	@echo "Available targets:"
	@echo "  make          - Build the poker calculator"
	@echo "  make clean    - Remove compiled binary"
	@echo "  make run      - Build and run the poker calculator"
	@echo "  make help     - Show this help message"
