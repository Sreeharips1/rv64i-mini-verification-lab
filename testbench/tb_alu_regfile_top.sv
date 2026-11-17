
module tb_alu_regfile_top;

    logic clk;
    logic [4:0] rs1, rs2, rd;
    logic [3:0] alu_op;
    logic reg_write;

    logic [63:0] external_write_data;
    logic writeback_from_external;

    logic [63:0] alu_result;
    logic [63:0] read_data1, read_data2;

    int pass_count = 0;
    int fail_count = 0;

    // Instantiate DUT
    rv64_alu_regfile_top dut (
        .clk(clk),
        .rs1(rs1),
        .rs2(rs2),
        .rd(rd),
        .alu_op(alu_op),
        .reg_write(reg_write),
        .external_write_data(external_write_data),
        .writeback_from_external(writeback_from_external),
        .alu_result(alu_result),
        .read_data1(read_data1),
        .read_data2(read_data2)
    );

    // Clock generation: 10 time-unit period
    initial clk = 0;
    always #5 clk <= ~clk;

    // Reusable checking task with detailed logging
    task automatic check(
        input logic [63:0] actual,
        input logic [63:0] expected,
        input string test_name,
        input logic [4:0] source_reg1,
        input logic [4:0] source_reg2,
        input logic [63:0] source_data1,
        input logic [63:0] source_data2,
        input logic [4:0] destination_reg,
        input logic [3:0] operation,
        input logic write_enable,
        input logic external_writeback
    );

        $display("------------------------------------------------");
        $display("TEST              : %s", test_name);
        $display("SOURCE REG 1      : x%0d", source_reg1);
        $display("SOURCE DATA 1     : 0x%016h", source_data1);
        $display("SOURCE REG 2      : x%0d", source_reg2);
        $display("SOURCE DATA 2     : 0x%016h", source_data2);
        $display("ALU OPERATION     : 0x%h", operation);
        $display("DESTINATION REG   : x%0d", destination_reg);
        $display("REGISTER WRITE    : %0b", write_enable);
        $display("EXTERNAL WRITEBACK: %0b", external_writeback);
        $display("EXPECTED RESULT   : 0x%016h", expected);
        $display("ACTUAL RESULT     : 0x%016h", actual);

        if (actual === expected) begin
            $display("STATUS            : PASS");
            pass_count++;
        end
        else begin
            $display("STATUS            : FAIL");
            $display("ERROR             : Expected and actual results do not match");
            fail_count++;
        end

        $display("");

    endtask

    initial begin

        // Initialize all inputs
        rs1 = 0;
        rs2 = 0;
        rd = 0;
        alu_op = 0;
        reg_write = 0;
        external_write_data = 0;
        writeback_from_external = 0;

        // Allow initial setup
        #2;

        // --------------------------------
        // STEP 1: Write 10 into x5
        // --------------------------------

        @(negedge clk);
        rd = 5;
        external_write_data = 64'd10;
        writeback_from_external = 1;
        reg_write = 1;

        @(posedge clk);
        #1;

        reg_write = 0;

        // --------------------------------
        // STEP 2: Write 20 into x6
        // --------------------------------

        @(negedge clk);
        rd = 6;
        external_write_data = 64'd20;
        reg_write = 1;

        @(posedge clk);
        #1;

        reg_write = 0;

        // --------------------------------
        // STEP 3: Read x5 and x6
        // --------------------------------

        @(negedge clk);
        rs1 = 5;
        rs2 = 6;
        #1;

        check(read_data1, 64'd10, "Read x5",
              5'd5, 5'd6,
              read_data1, read_data2,
              5'd0, 4'b0000, 1'b0, 1'b0);

        check(read_data2, 64'd20, "Read x6",
              5'd5, 5'd6,
              read_data1, read_data2,
              5'd0, 4'b0000, 1'b0, 1'b0);

        // --------------------------------
        // STEP 4: Execute ADD
        // x7 = x5 + x6
        // --------------------------------

        alu_op = 4'b0000;
        writeback_from_external = 0;
        rd = 7;
        reg_write = 1;

        #1;

        check(alu_result, 64'd30, "ALU computes 10 + 20",
              5'd5, 5'd6,
              read_data1, read_data2,
              5'd7, 4'b0000, 1'b1, 1'b0);

        @(posedge clk);
        #1;

        reg_write = 0;

        // --------------------------------
        // STEP 5: Read x7 and verify
        // --------------------------------

        rs1 = 7;
        #1;

        check(read_data1, 64'd30, "Result written into x7",
              5'd7, 5'd6,
              read_data1, read_data2,
              5'd7, 4'b0000, 1'b0, 1'b0);

        // --------------------------------
        // SUMMARY
        // --------------------------------

        $display("------------------------------------------------");
        $display("INTEGRATED DATAPATH VERIFICATION SUMMARY");
        $display("PASS COUNT: %0d", pass_count);
        $display("FAIL COUNT: %0d", fail_count);

        if (fail_count == 0)
            $display("ALL TESTS PASSED");
        else
            $display("SOME TESTS FAILED");

        $finish;

    end

endmodule
