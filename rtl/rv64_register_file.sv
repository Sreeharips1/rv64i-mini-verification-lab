
module rv64_register_file (

    input  logic        clk,
    input  logic        we,

    input  logic [4:0]  rs1,
    input  logic [4:0]  rs2,
    input  logic [4:0]  rd,

    input  logic [63:0] wd,

    output logic [63:0] rd1,
    output logic [63:0] rd2

);

    // 32 registers, each 64 bits wide
    logic [63:0] registers [0:31];

    // Synchronous write
    always_ff @(posedge clk) begin

        if (we && rd != 5'd0) begin
            registers[rd] <= wd;
        end

    end

    // Asynchronous read
    always_comb begin

        rd1 = (rs1 == 5'd0) ? 64'd0 : registers[rs1];

        rd2 = (rs2 == 5'd0) ? 64'd0 : registers[rs2];

    end

endmodule
