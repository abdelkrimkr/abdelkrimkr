[![Build LaTeX PDF](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/build_latex.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/build_latex.yml)

# LaTeX PDF Generation Project

This project provides a structure and a Python script to compile a LaTeX document into a PDF. The LaTeX source is organized into sections and includes bibliography management with BibTeX.

## Automated PDF Generation (GitHub Actions)

This project includes a GitHub Actions workflow (`.github/workflows/build_latex.yml`) that automatically compiles the LaTeX document and generates `main.pdf` whenever changes are pushed to the `main` (or `master`) branch.

You can also trigger the build manually from the "Actions" tab of the GitHub repository.

The generated PDF will be available as an artifact that can be downloaded from the summary page of the workflow run. Look for an artifact named "main-pdf".

## Project Structure

```
latex_project/
├── src/
│   ├── introduction/
│   │   └── introduction.tex
│   ├── methods/
│   │   └── methods.tex
│   ├── results/
│   │   └── results.tex
│   ├── discussion/
│   │   └── discussion.tex
│   ├── conclusion/
│   │   └── conclusion.tex
│   ├── main.tex          # Main LaTeX file
│   └── references.bib    # BibTeX bibliography file
├── build_pdf.py        # Python script to compile LaTeX to PDF
└── README.md           # This file
```

## Prerequisites

To compile the LaTeX document and generate the PDF, you need:

1.  **A LaTeX Distribution:**
    *   **TeX Live:** Recommended for Linux and Windows. ([https://www.tug.org/texlive/](https://www.tug.org/texlive/))
    *   **MiKTeX:** Common on Windows. ([https://miktex.org/](https://miktex.org/))
    *   **MacTeX:** For macOS. ([https://www.tug.org/mactex/](https://www.tug.org/mactex/))
    Ensure that `pdflatex` and `bibtex` commands are available in your system's PATH.

2.  **Python 3:**
    *   The `build_pdf.py` script is written for Python 3. ([https://www.python.org/downloads/](https://www.python.org/downloads/))

## How to Generate the PDF

1.  **Navigate to the project directory:**
    Open your terminal or command prompt and change to the `latex_project` directory.
    ```bash
    cd path/to/latex_project
    ```

2.  **Run the Python script:**
    Execute the `build_pdf.py` script.
    ```bash
    python build_pdf.py
    ```

3.  **Output:**
    If the compilation is successful, a `main.pdf` file will be generated in the `latex_project` directory. Log files (`.log`, `.aux`, etc.) will also be created in this directory.

## Customization

*   **Content:** Edit the `.tex` files within the `src` subdirectories to add your content. The main structure is defined in `src/main.tex`.
*   **Title/Author:** Modify the `	itle` and `uthor` commands in `src/main.tex`.
*   **Bibliography:** Add your references in BibTeX format to `src/references.bib`. Cite them in your `.tex` files using `\cite{key}`.
*   **LaTeX Packages:** Add or remove LaTeX packages in the preamble of `src/main.tex` as needed.
