
pipeline {
    agent any

    environment {
        PROJECT_DIR = '/mnt/c/cdac_files/rv64_learning/rv64i-mini-verification-lab'
    }

    stages {

        stage('Environment Check') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                        set -e
                        echo "RV64I Jenkins Pipeline"
                        java -version
                        verilator --version
                        python3 --version
                    '''
                }
            }
        }

        stage('RTL Lint') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                        set -e

                        verilator --lint-only -Wall \
                            --top-module rv64_alu \
                            rtl/rv64_alu.sv

                        verilator --lint-only -Wall \
                            --top-module rv64_register_file \
                            rtl/rv64_register_file.sv

                        verilator --lint-only -Wall \
                            --top-module rv64_alu_regfile_top \
                            rtl/rv64_register_file.sv \
                            rtl/rv64_alu.sv \
                            rtl/rv64_alu_regfile_top.sv

                        echo "RTL LINT PASSED"
                    '''
                }
            }
        }

        stage('ALU Simulation') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                        set -e
                        mkdir -p obj_dir/alu reports

                        verilator --binary --timing -Wall \
                            --Mdir obj_dir/alu \
                            --top-module tb_alu \
                            rtl/rv64_alu.sv \
                            testbench/tb_alu.sv

                        ./obj_dir/alu/Vtb_alu \
                            > reports/alu-simulation.log

                        cat reports/alu-simulation.log

                        python3 scripts/generate_junit.py \
                            reports/alu-simulation.log \
                            reports/alu-results.xml
                    '''
                }
            }
        }

        stage('Register File Simulation') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                        set -e
                        mkdir -p obj_dir/regfile reports

                        verilator --binary --timing -Wall \
                            --Mdir obj_dir/regfile \
                            --top-module tb_register_file \
                            rtl/rv64_register_file.sv \
                            testbench/tb_register_file.sv

                        ./obj_dir/regfile/Vtb_register_file \
                            > reports/register-file-simulation.log

                        cat reports/register-file-simulation.log

                        python3 scripts/generate_junit.py \
                            reports/register-file-simulation.log \
                            reports/register-file-results.xml
                    '''
                }
            }
        }

        stage('Datapath Simulation') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                        set -e
                        mkdir -p obj_dir/datapath reports

                        verilator --binary --timing -Wall \
                            --Mdir obj_dir/datapath \
                            --top-module tb_alu_regfile_top \
                            rtl/rv64_register_file.sv \
                            rtl/rv64_alu.sv \
                            rtl/rv64_alu_regfile_top.sv \
                            testbench/tb_alu_regfile_top.sv

                        ./obj_dir/datapath/Vtb_alu_regfile_top \
                            > reports/datapath-simulation.log

                        cat reports/datapath-simulation.log

                        python3 scripts/generate_junit.py \
                            reports/datapath-simulation.log \
                            reports/datapath-results.xml
                    '''
                }
            }
        }
    }

    post {
        always {
            dir("${PROJECT_DIR}") {
                junit allowEmptyResults: true,
                      testResults: 'reports/*-results.xml'

                archiveArtifacts allowEmptyArchive: true,
                    artifacts: 'reports/**'
            }

            echo 'RV64I verification pipeline completed.'
        }
    }
}
