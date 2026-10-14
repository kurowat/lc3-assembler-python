; =====================================================================
; LC-3 Label & Symbol Table Test Suite
; =====================================================================

        .ORIG   x3000

; --- Category 1: Standalone Labels (on their own line) ---
STANDALONE_LABEL
        ADD     R0, R0, #1

; --- Category 2: Labels on Opcode Instructions ---
LABEL_ADD   ADD     R1, R2, R3
LABEL_LD    LD      R4, DATA_CONST

; --- Category 3: Labels on Directives (.FILL, .BLKW, .STRINGZ) ---
DATA_CONST  .FILL   #42
BUFFER      .BLKW   #3
GREETING    .STRINGZ "Hi"

; --- Category 4: Multiple labels pointing to the same address ---
FIRST_TAG
SECOND_TAG
FINAL_OP    HALT

        .END
