.ORIG x3500
        LD    R0, Target      ; PC-relative load (9-bit offset)
        ST    R0, Target      ; PC-relative store
        LDI   R1, IndirectLoc ; Indirect load
        STI   R1, IndirectLoc ; Indirect store
        LDR   R2, R0, #5      ; Base + offset load (6-bit offset)
        STR   R2, R0, #-8     ; Base + offset store
        LEA   R3, Target      ; Load effective address
        HALT

Target  .FILL x3000
IndirectLoc .FILL x4000
        .END
