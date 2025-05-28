import subprocess
import os
import shutil

def compile_latex():
    project_root = os.path.abspath(os.path.dirname(__file__))
    latex_file_name = "main.tex"
    src_dir = os.path.join(project_root, "src")
    output_dir = project_root # Output PDF in the project root

    # Ensure the output directory exists (it's the project root, so it does)
    # os.makedirs(output_dir, exist_ok=True)

    latex_file_path = os.path.join(src_dir, latex_file_name)
    
    # Command templates
    pdflatex_cmd_template = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-output-directory", 
        output_dir, # Output PDF and aux files to project root
        latex_file_path
    ]
    
    # Bibtex needs to run in the directory where the .aux file is.
    # If -output-directory is used with pdflatex, .aux files go there.
    # So, bibtex should run on 'main.aux' in the output_dir.
    bibtex_cmd_template = [
        "bibtex",
        os.path.join(output_dir, "main") # Runs on main.aux
    ]

    # LaTeX compilation sequence
    commands = [
        ("pdflatex_pass_1", pdflatex_cmd_template),
        ("bibtex", bibtex_cmd_template),
        ("pdflatex_pass_2", pdflatex_cmd_template),
        ("pdflatex_pass_3", pdflatex_cmd_template),
    ]

    for step_name, command in commands:
        print(f"Running {step_name}...")
        try:
            # For bibtex, the CWD should be output_dir if aux file is there
            # For pdflatex, it needs to find the main.tex in src_dir
            # The provided pdflatex command correctly specifies the full path to main.tex
            # and output-directory.
            # Bibtex is trickier with paths if not run in the dir with aux files.
            # A common pattern is to run bibtex in the directory where main.aux is.
            
            cwd_for_command = output_dir if "bibtex" in step_name else project_root

            process = subprocess.run(command, capture_output=True, text=True, check=True, cwd=cwd_for_command)
            print(f"{step_name} output:\n{process.stdout}")
            if process.stderr:
                print(f"{step_name} errors:\n{process.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error during {step_name}: {e}")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")
            return False
        except FileNotFoundError as e:
            print(f"Error: Command not found during {step_name} - {e.filename}. Ensure LaTeX (pdflatex, bibtex) is installed and in your PATH.")
            return False
        print(f"{step_name} completed successfully.")

    # Check if PDF was created
    pdf_filename = os.path.join(output_dir, "main.pdf")
    if os.path.exists(pdf_filename):
        print(f"Successfully generated PDF: {pdf_filename}")
        # Optional: Move PDF to a specific 'output' folder if desired
        # final_pdf_dir = os.path.join(project_root, "output")
        # os.makedirs(final_pdf_dir, exist_ok=True)
        # shutil.move(pdf_filename, os.path.join(final_pdf_dir, "document.pdf"))
        # print(f"Moved PDF to {os.path.join(final_pdf_dir, 'document.pdf')}")
        return True
    else:
        print(f"Error: PDF file {pdf_filename} not found after compilation.")
        return False

if __name__ == "__main__":
    if compile_latex():
        print("LaTeX compilation successful.")
    else:
        print("LaTeX compilation failed.")
