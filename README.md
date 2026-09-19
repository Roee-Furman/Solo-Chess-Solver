# Solo-Chess-Solver
## Version 1
A fast, command-line solver for the Solo Chess puzzle variant, built entirely in standard library Python. 

It helps chess enthusiasts and developers find the exact sequence of FIDE-compliant captures needed to clear the board. 

**Just input your pieces, and the engine will calculate the solution while you watch!**

*Re8 Qe8 Ne7 Bb6 f6 Bh6 d5 Qe4 Ng4 Na3 Rd3 Qe3 Bf3 Nc2 d2 e2 Kg2 Ra1 Nf1*

![Solo Chess Solver V1 GIF](https://github.com/user-attachments/assets/decb1e28-0777-4d5f-953a-8e10dbb618da)

### Current Features
* **Zero Dependencies:** Runs on 100% pure Python. No external libraries required.
* **Search Engine:** Uses DFS with state memoization to prune invalid branches.
* **Smart SAN Notation:** Strictly follows FIDE algebraic notation rules.
* **Threaded UI:** Features a smooth, non-blocking background animation that keeps the terminal clean while calculating.
