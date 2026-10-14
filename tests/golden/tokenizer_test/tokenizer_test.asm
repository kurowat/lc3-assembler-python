; =====================================================================
; Comprehensive LC-3 Tokenizer Test Suite
; Covers all Directives, Instructions, Trap aliases, Registers, & Formats
; =====================================================================

        .ORIG   x3000

; --- 1. ALU Operations & Register Variations ---
START   ADD     R0, R1, R2          ; ADD register mode
        ADD     R3, R4, #5          ; ADD positive immediate
        ADD     R5, R6, #-16        ; ADD negative immediate
        AND     R7, R0, R1          ; AND register mode
        AND     R2, R3, #0          ; AND immediate clear
        NOT     R4, R5              ; NOT invert

; --- 2. Memory Operations (Direct, Indirect, Base+Offset, LEA) ---
        LD      R0, DATA_VAL        ; LD PC-relative
        LDI     R1, PTR_VAL         ; LDI indirect
        LDR     R2, R6, #3          ; LDR base + positive offset
        LDR     R3, R7, #-4         ; LDR base + negative offset
        LEA     R4, MSG_STR         ; LEA address load

        ST      R0, DATA_VAL        ; ST store
        STI     R1, PTR_VAL         ; STI indirect store
        STR     R2, R6, #1          ; STR base + offset store

; --- 3. Branch Instructions (All 8 Condition Code Variations) ---
CHECK   BR      TARGET              ; Unconditional branch alias
        BRn     TARGET              ; Negative
        BRz     TARGET              ; Zero
        BRp     TARGET              ; Positive
        BRnz    TARGET              ; Negative or Zero
        BRnp    TARGET              ; Negative or Positive
        BRzp    TARGET              ; Zero or Positive
        BRnzp   TARGET              ; All conditions explicit

; --- 4. Control Flow & Subroutines ---
TARGET  JSR     SUB_ROUTINE         ; Jump to subroutine (label)
        JSRR    R4                  ; Jump to subroutine register
        JMP     R7                  ; Jump register
        RET                         ; Return from subroutine
        RTI                         ; Return from interrupt

; --- 5. Trap Instruction & Standard Trap Pseudo-Ops ---
        TRAP    x25                 ; Explicit TRAP call
        GETC                        ; Alias: TRAP x20
        OUT                         ; Alias: TRAP x21
        PUTS                        ; Alias: TRAP x22
        IN                          ; Alias: TRAP x23
        PUTSP                       ; Alias: TRAP x24
        HALT                        ; Alias: TRAP x25

; --- 6. Directives and Data Declarations ---
SUB_ROUTINE
DATA_VAL    .FILL   #-123           ; Decimal negative constant
DATA_HEX    .FILL   xFF00           ; Hex constant
PTR_VAL     .FILL   DATA_VAL        ; Label pointer address
BLOCK_MEM   .BLKW   #4              ; Block of words allocation
MSG_STR     .STRINGZ "Hello, LC-3 World! #123; not a comment"

        .END
