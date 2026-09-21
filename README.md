# Solo Chess Solver 

### Version 1.0.0

A fast, command-line solver for the Solo Chess puzzle variant, built entirely in standard library Python. 

It helps chess enthusiasts and developers find the exact sequence of FIDE-compliant captures needed to clear the board. 

**Just input your pieces, and the engine will calculate the solution while you watch!**

### How to Use

1. Open a Solo Chess puzzle.
2. Run the solver in your terminal or command prompt:
   ```
   python solo_chess_solver.py
   ```
3. Look at your puzzle and write down the pieces using their coordinates. 
   * **Pieces:** Use the standard uppercase letter + coordinate (e.g., `Bf4`, `Kc6`).
   * **Pawns:** Just type the coordinate without a letter (e.g., `e3`).
4. Type them all into the prompt separated by spaces.

**Example:**
If the board has a Bishop on f4, a Pawn on e3, a King on c6, and a Rook on c5, type exactly this:
`Bf4 e3 Kc6 Rc5`
