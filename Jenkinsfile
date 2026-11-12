
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
                        echo "RV64I Jenkins Pipeline"
                        echo "Checking tools..."

                        java -version
                        verilator --version
                        python3 --version

                        echo "Environment check passed"
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

    }

    post {
        always {
            echo 'RV64I Jenkins pipeline execution completed.'
        }
    }
}
