
module rv64_alu (

    input  logic [63:0] operand_a,
    input  logic [63:0] operand_b,

    input  logic [3:0] alu_op,

    output logic [63:0] result

);

    always_comb begin

        // Default result
        result = 64'b0;

        case (alu_op)

            4'b0000: result = operand_a + operand_b;  // ADD

            4'b0001: result = operand_a - operand_b;  // SUB

            4'b0010: result = operand_a & operand_b;  // AND

            4'b0011: result = operand_a | operand_b;  // OR

            4'b0100: result = operand_a ^ operand_b;  // XOR

            4'b0101: result = operand_a << operand_b[5:0]; // SLL

            4'b0110: result = operand_a >> operand_b[5:0]; // SRL

            4'b0111: result = $signed(operand_a) >>> operand_b[5:0]; // SRA

            4'b1000: result = {63'b0, ($signed(operand_a) < $signed(operand_b))}; // SLT

            4'b1001: result = {63'b0, (operand_a < operand_b)}; // SLTU

            default: result = 64'b0;

        endcase

    end

endmodule