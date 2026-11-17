# RV64I Mini Verification Lab

**A 64-bit RISC-V RTL Design and Functional Verification Project using SystemVerilog, Verilator, GitLab CI/CD and Jenkins.**

## 1. Project Overview

The **RV64I Mini Verification Lab** is an educational RTL design and verification project focused on developing and testing fundamental datapath components of a 64-bit RISC-V processor.

The project implements a 64-bit Arithmetic Logic Unit (ALU), a 32-entry register file and an integrated ALU-register file datapath.

SystemVerilog is used for RTL design and testbench development, while Verilator is used for RTL linting, compilation and simulation.

Automated verification is implemented using GitLab CI/CD and Jenkins. Python scripts generate JUnit XML, HTML and PDF verification reports.

### Project Objectives

- Understand the architecture and fundamental datapath operations of RV64I.
- Design basic processor components using SystemVerilog.
- Develop functional testbenches for RTL verification.
- Perform RTL linting and simulation using Verilator.
- Automate verification using CI/CD pipelines.
- Generate structured verification reports.

## 2. Features

- 64-bit arithmetic and logical operations.
- 32 × 64-bit RISC-V register file.
- Two combinational read ports and one synchronous write port.
- Hardwired zero register (x0).
- Integrated ALU and register file datapath.
- SystemVerilog functional testbenches.
- Verilator-based RTL linting and simulation.
- Automated GitLab CI/CD and Jenkins pipelines.
- JUnit XML test result generation.
- Automated HTML and PDF verification reports.
- Git commit, branch and IST timestamp information in reports.

## 3. Architecture

The project consists of three main RTL modules.

### 3.1 RV64I ALU

**File:** `rtl/rv64_alu.sv`

The Arithmetic Logic Unit performs arithmetic, logical and shift operations on 64-bit operands.

Implemented operations:

| Operation | Description              |
| --------- | ------------------------ |
| ADD       | Addition                 |
| SUB       | Subtraction              |
| AND       | Bitwise AND              |
| OR        | Bitwise OR               |
| XOR       | Bitwise XOR              |
| SLL       | Shift Left Logical       |
| SRL       | Shift Right Logical      |
| SRA       | Shift Right Arithmetic   |
| SLT       | Set Less Than (Signed)   |
| SLTU      | Set Less Than (Unsigned) |

### 3.2 RV64 Register File

**File:** `rtl/rv64_register_file.sv`

The register file provides storage for the integer registers used by the RISC-V processor.

Specifications:

- 32 registers (x0–x31).
- 64-bit width per register.
- Two combinational read ports.
- One synchronous write port.
- Register x0 always returns zero.

### 3.3 Integrated ALU and Register File Datapath

**File:** `rtl/rv64_alu_regfile_top.sv`

This module integrates the ALU and register file.

Basic operation:

1. Read two operands from the register file.
2. Send the operands to the ALU.
3. Execute the selected ALU operation.
4. Write the result into the destination register.

This integration allows verification of interactions between the individual RTL components.

**Note:** This project implements a basic RV64I datapath, not a complete RISC-V processor.

## 4. Project Directory Structure

```text
rv64i-mini-verification-lab/
│
├── rtl/
│   ├── rv64_alu.sv
│   ├── rv64_register_file.sv
│   └── rv64_alu_regfile_top.sv
│
├── testbench/
│   ├── tb_alu.sv
│   ├── tb_register_file.sv
│   └── tb_alu_regfile_top.sv
│
├── tests/
│   ├── arithmetic/
│   ├── branch/
│   └── logical/
│
├── scripts/
│   ├── generate_junit.py
│   ├── generate_html.py
│   └── generate_pdf.py
│
├── reports/
│
├── Jenkinsfile
├── .gitlab-ci.yml
└── README.md
```

## 5. Tools and Technologies

| Tool / Technology | Purpose                                |
| ----------------- | -------------------------------------- |
| SystemVerilog     | RTL design and testbench development   |
| Verilator 5.020   | RTL linting and simulation             |
| Python 3.12       | Test automation and report generation  |
| ReportLab 4.1.0   | PDF report generation                  |
| Jenkins 2.580.2   | Continuous Integration                 |
| GitLab            | Source control and GitLab CI/CD        |
| GitHub            | Source repository for Jenkins          |
| Ubuntu 24.04 LTS  | Linux development environment          |
| WSL2              | Ubuntu environment on Windows          |
| G++               | Compilation of Verilator-generated C++ |
| Make              | Build automation                       |
| Git               | Version control                        |

## 6. Requirements

The development environment used for this project:

- Windows with WSL2.
- Ubuntu 24.04 LTS.
- Verilator 5.020.
- Python 3.12.
- G++ compiler.
- GNU Make.
- Git.
- ReportLab 4.1.0 for PDF report generation.

Install the main dependencies on Ubuntu:

```bash
sudo apt update

sudo apt install -y \
    verilator \
    python3 \
    python3-reportlab \
    g++ \
    make \
    git
```

Verify the installations:

```bash
verilator --version
python3 --version
g++ --version
make --version
git --version
```

## 7. Running RTL Verification Locally

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Sreeharips1/rv64i-mini-verification-lab.git

cd rv64i-mini-verification-lab
```

### 7.1 RTL Linting

Lint the ALU:

```bash
verilator --lint-only -Wall \
    --top-module rv64_alu \
    rtl/rv64_alu.sv
```

Lint the register file:

```bash
verilator --lint-only -Wall \
    --top-module rv64_register_file \
    rtl/rv64_register_file.sv
```

Lint the integrated datapath:

```bash
verilator --lint-only -Wall \
    --top-module rv64_alu_regfile_top \
    rtl/rv64_register_file.sv \
    rtl/rv64_alu.sv \
    rtl/rv64_alu_regfile_top.sv
```

### 7.2 ALU Simulation

```bash
verilator --binary --timing -Wall \
    --top-module tb_alu \
    rtl/rv64_alu.sv \
    testbench/tb_alu.sv

./obj_dir/Vtb_alu
```

### 7.3 Register File Simulation

```bash
verilator --binary --timing -Wall \
    --top-module tb_register_file \
    rtl/rv64_register_file.sv \
    testbench/tb_register_file.sv

./obj_dir/Vtb_register_file
```

### 7.4 Integrated Datapath Simulation

```bash
verilator --binary --timing -Wall \
    --top-module tb_alu_regfile_top \
    rtl/rv64_register_file.sv \
    rtl/rv64_alu.sv \
    rtl/rv64_alu_regfile_top.sv \
    testbench/tb_alu_regfile_top.sv

./obj_dir/Vtb_alu_regfile_top
```

## 8. Verification Results

The project currently contains 27 functional test cases across three testbenches.

| Testbench           | Test Cases |
| ------------------- | ---------: |
| ALU                 |         18 |
| Register File       |          5 |
| Integrated Datapath |          4 |
| **Total**           |     **27** |

### Latest Jenkins Build Results

| Metric       |  Result |
| ------------ | ------: |
| Build Number |      #3 |
| Build Status | SUCCESS |
| Total Tests  |      27 |
| Passed       |      27 |
| Failed       |       0 |

All 27 functional tests passed in Jenkins Build #3.

## 9. Automated Verification Using GitLab CI/CD

The project includes a `.gitlab-ci.yml` configuration.

The GitLab CI pipeline automates:

1. RTL linting.
2. ALU simulation.
3. Register file simulation.
4. Integrated datapath simulation.
5. JUnit XML generation.
6. Verification report generation and artifact collection.

The CI pipeline helps identify RTL and functional issues whenever project changes are submitted.

## 10. Jenkins Continuous Integration Pipeline

A Jenkins pipeline is configured using the `Jenkinsfile`.

### Pipeline Stages

| Stage                    | Description                                    |
| ------------------------ | ---------------------------------------------- |
| Environment Check        | Checks Java, Verilator and Python versions     |
| Prepare Workspace        | Cleans and prepares the build workspace        |
| RTL Lint                 | Performs RTL lint checks                       |
| ALU Simulation           | Executes ALU testbench                         |
| Register File Simulation | Executes register file testbench               |
| Datapath Simulation      | Executes integrated datapath testbench         |
| Generate Reports         | Generates HTML and PDF reports                 |
| Post Actions             | Publishes JUnit results and archives artifacts |

### Jenkins Repository

GitHub repository:

https://github.com/Sreeharips1/rv64i-mini-verification-lab

Jenkins checks out the `main` branch and executes the pipeline defined in `Jenkinsfile`.

### Running the Pipeline

1. Open the Jenkins dashboard.
2. Select `RV64I_Verification_Fresh`.
3. Click **Build Now**.
4. Open the corresponding build.
5. Check Console Output, Tests and Build Artifacts.

## 11. Verification Reports

Python scripts automate the generation of verification reports.

| Script              | Function                                |
| ------------------- | --------------------------------------- |
| `generate_junit.py` | Converts simulation logs into JUnit XML |
| `generate_html.py`  | Generates an HTML verification report   |
| `generate_pdf.py`   | Generates a PDF verification report     |

### Generated Artifacts

```text
reports/
│
├── alu-simulation.log
├── alu-results.xml
│
├── register-file-simulation.log
├── register-file-results.xml
│
├── datapath-simulation.log
├── datapath-results.xml
│
├── verification-report.html
└── verification-report.pdf
```

The generated reports include project information, Git commit, branch, IST timestamp, and verification test results.

Jenkins archives these files as build artifacts for later inspection and download.

## 12. Project Scope and Future Improvements

The current implementation focuses on basic RV64I datapath components and functional verification.

Planned improvements:

- Implement an RV64I instruction decoder.
- Develop processor control logic.
- Implement branch and jump operations.
- Develop a load/store unit.
- Integrate a program counter.
- Build a more complete RV64I processor datapath.
- Use Spike as a reference simulator for architectural comparison.
- Introduce randomized testing.
- Add SystemVerilog assertions.
- Implement functional coverage.
- Expand verification to processor-level testing.

## 13. Project Status

The current project has completed:

- Basic RV64I ALU RTL design.
- Register file RTL design.
- Integrated datapath RTL design.
- SystemVerilog testbench development.
- 27 functional test cases.
- Verilator-based linting and simulation.
- GitLab CI/CD integration.
- Jenkins CI integration.
- Automated JUnit, HTML and PDF report generation.
- Jenkins artifact archiving.

Further development will focus on instruction-level verification and expanding the processor architecture.

## 14. Author

**Sreehari P Shaiju**

B.Tech – Electronics and Communication Engineering

GitHub: https://github.com/Sreeharips1

Portfolio: https://sreeharipsportfolio.netlify.app/

---

**RV64I Mini Verification Lab — Learning, Designing and Verifying RISC-V Hardware.**
