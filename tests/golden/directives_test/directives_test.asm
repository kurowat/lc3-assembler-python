.ORIG x3000
start   LD R0, Num1
        LD R1, Num2
        HALT

Num1    .FILL x1234
Num2    .FILL #-5
Msg     .STRINGZ "LC3"
Buffer  .BLKW #5
        .END
