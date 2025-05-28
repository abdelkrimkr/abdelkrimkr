import subprocess
import os
import shutil # shutil is not used in the current version, but kept for potential future use
import sys

def compile_latex():
    project_root = os.path.abspath(os.path.dirname(__file__))
    latex_file_name = "main.tex"
    src_dir = os.path.join(project_root, "src")
    output_dir = project_root # Output PDF and aux files to project root
    log_file_path = os.path.join(project_root, "build_log.txt")

    latex_file_path = os.path.join(src_dir, latex_file_name)
    
    # Command templates
    pdflatex_cmd_template = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-output-directory", 
        output_dir,
        latex_file_path
    ]
    
    bibtex_cmd_template = [
        "bibtex",
        os.path.join(output_dir, "main") # Runs on main.aux in output_dir
    ]

    commands = [
        ("pdflatex_pass_1", pdflatex_cmd_template),
        ("bibtex", bibtex_cmd_template),
        ("pdflatex_pass_2", pdflatex_cmd_template),
        ("pdflatex_pass_3", pdflatex_cmd_template),
    ]

    with open(log_file_path, "w") as log_file:
        for step_name, command in commands:
            log_file.write(f"--- Running {step_name} ---\n")
            print(f"Running {step_name}...")
            try:
                # Determine CWD for the command
                # Bibtex should run where the .aux file is (output_dir)
                # pdflatex can run from project_root as paths are absolute or specified
                cwd_for_command = output_dir if "bibtex" in step_name else project_root
                
                process = subprocess.run(command, capture_output=True, text=True, cwd=cwd_for_command, check=False)
                
                log_file.write(f"Command: {' '.join(command)}\n")
                log_file.write(f"Return Code: {process.returncode}\n")
                log_file.write("Stdout:\n")
                log_file.write(process.stdout + "\n")
                log_file.write("Stderr:\n")
                log_file.write(process.stderr + "\n")

                if process.returncode != 0:
                    print(f"Error during {step_name}. Check build_log.txt for details.")
                    log_file.write(f"\n--- {step_name} FAILED ---\n")
                    log_file.write("--- BUILD FAILED ---\n")
                    print("BUILD FAILED")
                    return False
                
                print(f"{step_name} completed successfully.")
                log_file.write(f"--- {step_name} completed successfully ---\n\n")

            except FileNotFoundError as e:
                error_message = f"Error: Command not found during {step_name} - {e.filename}. Ensure LaTeX (pdflatex, bibtex) is installed and in your PATH."
                print(error_message)
                log_file.write(error_message + "\n")
                log_file.write("--- BUILD FAILED ---\n")
                print("BUILD FAILED")
                return False
            except Exception as e: # Catch any other unexpected errors during subprocess execution
                error_message = f"An unexpected error occurred during {step_name}: {str(e)}"
                print(error_message)
                log_file.write(error_message + "\n")
                log_file.write("--- BUILD FAILED ---\n")
                print("BUILD FAILED")
                return False


        pdf_filename = os.path.join(output_dir, "main.pdf")
        if os.path.exists(pdf_filename):
            success_message = f"Successfully generated PDF: {pdf_filename}"
            print(success_message)
            log_file.write("\n" + success_message + "\n")
            log_file.write("--- BUILD SUCCESSFUL ---\n")
            print("BUILD SUCCESSFUL")
            return True
        else:
            error_message = f"Error: PDF file {pdf_filename} not found after compilation. Check build_log.txt for details."
            print(error_message)
            log_file.write("\n" + error_message + "\n")
            log_file.write("--- BUILD FAILED: PDF not found ---\n")
            print("BUILD FAILED")
            return False

if __name__ == "__main__":
    if compile_latex():
        print("LaTeX compilation successful.")
        sys.exit(0)
    else:
        # The detailed "BUILD FAILED" message and "check build_log.txt" is already printed by compile_latex()
        print("LaTeX compilation failed. See build_log.txt for details.")
        sys.exit(1)
