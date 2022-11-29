.OVERRUN 320 * 320                      ; set size of ram for the display buffer

PROGRAM_OFFSET = 9                      ; how long the program is, i need
                                        ; to implement this as a constant directive or something

:loop
    rnd     rgb                         ; color
    rndc    rgc     320*320             ; coordinate

    set     rga     PROGRAM_OFFSET      ; i really need to implement add constant
    add     rgc     rga                 ; so i dont need to do this

    mov     rfr     rgc                 ; overwrite the coordinate with offseted coordinate
    storer  rgb     rgc                 ; write to display buffer
    jmp     loop                        ; infinite loop
