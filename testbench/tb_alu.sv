
module tb_alu;

    logic [63:0] operand_a;
    logic [63:0] operand_b;
    logic [3:0]  alu_op;
    logic [63:0] result;

    int pass_count = 0;
    int fail_count = 0;

    // Instantiate the ALU (DUT)
    rv64_alu dut (
        .operand_a(operand_a),
        .operand_b(operand_b),
        .alu_op(alu_op),
        .result(result)
    );

    // Task to check ALU results
    task automatic check_result(
        input string test_name,
        input logic [3:0] op,
        input logic [63:0] a,
        input logic [63:0] b,
        input logic [63:0] expected
    );

        alu_op = op;
        operand_a = a;
        operand_b = b;

        #1;

        if (result === expected) begin
            $display("PASS: %s", test_name);
            pass_count++;
        end
        else begin
            $display("FAIL: %s expected=%h actual=%h",
                     test_name, expected, result);
            fail_count++;
        end

    endtask

    initial begin

        $display("Starting RV64 ALU verification");

        // Basic ALU operations
        check_result("ADD basic", 4'b0000, 10, 20, 30);
        check_result("SUB basic", 4'b0001, 30, 10, 20);

        check_result("AND operation", 4'b0010, 64'hA, 64'hC, 64'h8);
        check_result("OR operation",  4'b0011, 64'hA, 64'hC, 64'hE);
        check_result("XOR operation", 4'b0100, 64'hA, 64'hC, 64'h6);

        check_result("SLL basic", 4'b0101, 1, 3, 8);
        check_result("SRL basic", 4'b0110, 16, 2, 4);
        check_result("SRA basic negative", 4'b0111,
                     64'hFFFFFFFFFFFFFFF0, 2,
                     64'hFFFFFFFFFFFFFFFC);

        check_result("SLT signed negative comparison", 4'b1000,
                     64'hFFFFFFFFFFFFFFFB, 3, 1);
        check_result("SLTU unsigned comparison", 4'b1001,
                     64'hFFFFFFFFFFFFFFFB, 3, 0);

        // Boundary and corner-case tests

        check_result("ADD 64-bit overflow", 4'b0000,
                     64'hFFFFFFFFFFFFFFFF,
                     64'h0000000000000001,
                     64'h0000000000000000);

        check_result("SUB zero minus one", 4'b0001,
                     64'h0000000000000000,
                     64'h0000000000000001,
                     64'hFFFFFFFFFFFFFFFF);

        check_result("SLL maximum shift 63", 4'b0101,
                     64'h0000000000000001,
                     64'd63,
                     64'h8000000000000000);

        check_result("SRL logical right shift", 4'b0110,
                     64'hFFFFFFFFFFFFFFFF,
                     64'd2,
                     64'h3FFFFFFFFFFFFFFF);

        check_result("SRA arithmetic right shift", 4'b0111,
                     64'hFFFFFFFFFFFFFFF0,
                     64'd2,
                     64'hFFFFFFFFFFFFFFFC);

        check_result("SLT signed minus one less than zero", 4'b1000,
                     64'hFFFFFFFFFFFFFFFF,
                     64'h0000000000000000,
                     64'd1);

        check_result("SLTU unsigned maximum value comparison", 4'b1001,
                     64'hFFFFFFFFFFFFFFFF,
                     64'h0000000000000000,
                     64'd0);

        check_result("Invalid ALU operation", 4'b1010,
                     64'd10, 64'd20, 64'd0);

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

