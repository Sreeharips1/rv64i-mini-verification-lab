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

    // Clock generation
    initial clk = 0;
    always #5 clk <= ~clk;

    task automatic check(
        input logic [63:0] actual,
        input logic [63:0] expected,
        input string test_name
    );
        if (actual === expected) begin
            $display("PASS: %s", test_name);
            pass_count++;
        end else begin
            $display("FAIL: %s expected=%h actual=%h",
                     test_name, expected, actual);
            fail_count++;
        end
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

        // Stop writing
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

        check(read_data1, 64'd10, "Read x5");
        check(read_data2, 64'd20, "Read x6");

        // --------------------------------
        // STEP 4: Execute ADD
        // x7 = x5 + x6
        // --------------------------------

        alu_op = 4'b0000;
        writeback_from_external = 0;
        rd = 7;
        reg_write = 1;

        #1;
        check(alu_result, 64'd30, "ALU computes 10 + 20");

        @(posedge clk);
        #1;

        reg_write = 0;

        // --------------------------------
        // STEP 5: Read x7 and verify
        // --------------------------------

        rs1 = 7;
        #1;

        check(read_data1, 64'd30, "Result written into x7");

        // --------------------------------
        // SUMMARY
        // --------------------------------

        $display("--------------------------------");
        $display("PASS COUNT: %0d", pass_count);
        $display("FAIL COUNT: %0d", fail_count);

        if (fail_count == 0)
            $display("ALL TESTS PASSED");
        else
            $display("SOME TESTS FAILED");

        $finish;

    end

endmodule
