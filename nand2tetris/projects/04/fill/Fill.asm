// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.
(START)
    @SCREEN
    D=A
    @addr
    M=D     // address = 16384 screen's base address
    
    @8192
    D=A
    @n
    M=D     // n = 8192
    @i
    M=1     // i = 1
    @KBD
    D=M
    @SET1
    D;JGT
    @SET0
    D;JEQ
    
(SET0)
    @R0
    M=0
    @LOOP
    0;JMP
(SET1)
    @R0
    M=-1
    @LOOP
    0;JMP
(LOOP)
    @i
    D=M
    @n
    D=D-M
    @END
    D;JGT   // if i>n goto END
    
    @R0
    D=M
    @addr
    A=M
    M=D    // RAM[addr] = RAM[0]
    
    @i
    M=M+1
    @1
    D=A
    @addr
    M=D+M   // addr = addr + 1
    @LOOP
    0;JMP
    
(END)   
    @START
    0;JMP