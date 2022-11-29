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

NAME = 1000

:start
    set rga 5
    set rgb 7
    add rga rgb
    mov rfr rgb

:loop
    inc rga
    rndc rgc 100
    jmp loop