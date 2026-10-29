module alu8 (
    input        clk,
    input  [7:0] a,
    input  [7:0] b,
    input  [1:0] op,      // 00 add, 01 sub, 10 and, 11 or
    output reg [7:0] result,
    output reg       carry,
    output reg       zero
);
    reg [8:0] full;

    always @(posedge clk) begin
        case (op)
            2'b00: full = {1'b0, a} + {1'b0, b};
            2'b01: full = {1'b0, a} - {1'b0, b};
            2'b10: full = {1'b0, a & b};
            2'b11: full = {1'b0, a | b};
        endcase
        result <= full[7:0];
        carry  <= full[8];
        zero   <= (full[7:0] == 8'd0);
    end
endmodule