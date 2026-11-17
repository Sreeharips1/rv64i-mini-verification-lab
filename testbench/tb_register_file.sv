
module tb_register_file;

    logic clk;
    logic we;

    logic [4:0] rs1;
    logic [4:0] rs2;
    logic [4:0] rd;

    logic [63:0] wd;
    logic [63:0] rd1;
    logic [63:0] rd2;

    int pass_count = 0;
    int fail_count = 0;

    // Instantiate DUT
    rv64_register_file dut (
        .clk(clk),
        .we(we),
        .rs1(rs1),
        .rs2(rs2),
        .rd(rd),
        .wd(wd),
        .rd1(rd1),
        .rd2(rd2)
    );

    // Clock generation: 10 time-unit period
    initial clk = 0;
    always #5 clk <= ~clk;

    // Reusable checking task with detailed logging
    task automatic check(
        input logic [63:0] actual,
        input logic [63:0] expected,
        input string test_name,
        input logic write_enable,
        input logic [4:0] write_reg,
        input logic [63:0] write_data,
        input logic [4:0] read_reg
    );

        $display("----------------------------------------");
        $display("TEST       : %s", test_name);
        $display("WRITE EN   : %0b", write_enable);
        $display("WRITE REG  : x%0d", write_reg);
        $display("WRITE DATA : 0x%016h", write_data);
        $display("READ REG   : x%0d", read_reg);
        $display("READ DATA  : 0x%016h", actual);
        $display("EXPECTED   : 0x%016h", expected);

        if (actual === expected) begin
            $display("STATUS     : PASS");
            $display("ERROR      : None");
            pass_count++;
        end
        else begin
            $display("STATUS     : FAIL");
            $display("ERROR      : Read data does not match expected data");
            fail_count++;
        end

        $display("");

    endtask

    initial begin

        we  = 0;
        rs1 = 0;
        rs2 = 0;
        rd  = 0;
        wd  = 0;

        // Allow initial setup
        #2;

        // Test 1: Write 100 to x5
        @(negedge clk);
        we = 1;
        rd = 5;
        wd = 100;

        @(posedge clk);
        #1;

        we = 0;
        rs1 = 5;
        #1;

        check(rd1, 64'd100, "Write and read x5",
              1'b1, 5'd5, 64'd100, 5'd5);

        // Test 2: Write 200 to x6
        @(negedge clk);
        we = 1;
        rd = 6;
        wd = 200;

        @(posedge clk);
        #1;

        we = 0;
        rs1 = 5;
        rs2 = 6;
        #1;

        check(rd1, 64'd100, "Read x5",
              1'b0, 5'd6, 64'd200, 5'd5);

        check(rd2, 64'd200, "Read x6 simultaneously",
              1'b0, 5'd6, 64'd200, 5'd6);

        // Test 3: Attempt to write 999 to x0
        @(negedge clk);
        we = 1;
        rd = 0;
        wd = 999;

        @(posedge clk);
        #1;

        we = 0;
        rs1 = 0;
        #1;

        check(rd1, 64'd0, "x0 always returns zero",
              1'b1, 5'd0, 64'd999, 5'd0);

        // Test 4: Write disabled
        @(negedge clk);
        we = 0;
        rd = 5;
        wd = 999;

        @(posedge clk);
        #1;

        rs1 = 5;
        #1;

        check(rd1, 64'd100, "Write disabled preserves x5",
              1'b0, 5'd5, 64'd999, 5'd5);

        // Summary
        $display("----------------------------------------");
        $display("REGISTER FILE VERIFICATION SUMMARY");
        $display("PASS COUNT: %0d", pass_count);
        $display("FAIL COUNT: %0d", fail_count);

        if (fail_count == 0)
            $display("ALL TESTS PASSED");
        else
            $display("SOME TESTS FAILED");

        $finish;

    end

endmodule
