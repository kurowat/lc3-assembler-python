.ORIG x3000
        AND R0, R0, #0        ; Clear R0 (Sets Z = 1)
        ADD R0, R0, #1        ; R0 = 1 (Sets P = 1)
        BRz   SkipForward     ; Should NOT branch
        
        ADD R1, R0, #-1       ; R1 = 0 (Sets Z = 1)
        BRnp  SkipForward     ; Should NOT branch
        BRz   TargetBack      ; SHOULD branch backward

SkipForward
        ADD R2, R2, #5        ; Should be skipped over if forward branch works

TargetBack
        BRnzp EndProgram      ; Unconditional branch forward
        NOP                   ; (or another dummy instruction)

EndProgram
        HALT
        .END
