# Compiler

This project is about the development of a **compiler** for a language that combine elements from C & Pascal, written in Python.

Taking as input some code ec: sourceFile.txt and export the final-programm. This **compiler** can identify every *error* and *warning* that violates the rules and prints them on the user's screen.

Code is analysed via 7 phases:
 * Verbal analysis (states diagram)
 * Editorial analysis (LL(1) grammar)
 * Semantic analysis
 * Production of Intermediate code (Scopes, Entities, Arguments)
 * Optimization of Intermadiate code
 * Production of Final code (assembly via MIPS)
 * Optimization of Final code
 
 ***Note***: By running *Final.py*, three more files are generated, *cFile.c* for testing purpuses, *asciiFile.asm* containing the MIPS's ascii commands and *intFile.int* containing the production of Intermediate code.
