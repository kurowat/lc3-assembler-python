.ORIG x3000
        ADD R0, R1, R2        ; Register mode (bit 5 = 0)
        ADD R1, R1, #15       ; Max positive immediate (+15)
        ADD R2, R2, #-16      ; Max negative immediate (-16)
        AND R3, R1, R2        ; Bitwise AND register mode
        AND R4, R1, #7        ; Bitwise AND immediate mode
        NOT R5, R0            ; NOT instruction (all 1s in bits [5:3])
        HALT
        .END
