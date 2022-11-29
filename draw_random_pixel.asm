; contoh comment
;;;;;;;;;;;;;;;;; HUEHUEHEUHEU ;;;;
; .margin 10000

; :SECTION_ONE
;     set rga 7382      ; set register RGA to 64
;     set rgb 0x7382      ; set register RGA to 64
;     set rgc 0b11011010111      ; set register RGA to 64
;     mov rga rfb     ; move from rga to rgb

; :SECTION_TWO
; ; comments firstline
;     add rga rgb     ;some other comments 1 +  2
;     mov rgb rgc     ; another
;     cmp rgc rgb
;     jez SECTION_TWO
;     jmp SECTION_ONE

; :SECTION_THREE
;     load 123123 rga
.OVERRUN 320 * 320

PROGRAM_OFFSET = 15

:loop
    rnd rgb             ; color
    rndc rgc 320*320    ; coordinate
    set rga PROGRAM_OFFSET
    add rgc rga
    mov rfr rgc
    storer rgb rgc
    jmp loop
