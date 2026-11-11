module rv64_alu_regfile_top (
    input logic clk,

    // Register addresses
    input logic [4:0] rs1,
    input logic [4:0] rs2,
    input logic [4:0] rd,

    // ALU control
    input logic [3:0] alu_op,

    // Register write control
    input logic reg_write,

    // External write-back data
    input logic [63:0] external_write_data,
    input logic writeback_from_external,

    // Outputs
    output logic [63:0] alu_result,
    output logic [63:0] read_data1,
    output logic [63:0] read_data2
);

    logic [63:0] write_data;

    // Register File
    rv64_register_file reg_file (
        .clk(clk),
        .we(reg_write),
        .rs1(rs1),
        .rs2(rs2),
        .rd(rd),
        .wd(write_data),
        .rd1(read_data1),
        .rd2(read_data2)
    );

    // ALU
    rv64_alu alu (
        .operand_a(read_data1),
        .operand_b(read_data2),
        .alu_op(alu_op),
        .result(alu_result)
    );

    // Write-back multiplexer
    always_comb begin
        if (writeback_from_external)
            write_data = external_write_data;
        else
            write_data = alu_result;
    end

endmodule
