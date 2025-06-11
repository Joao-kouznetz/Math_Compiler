import subprocess
import os


def render_latex(formula: str, output_pdf: str = "output.pdf"):
    if formula.startswith("$$") and formula.endswith("$$"):
        formula = formula[2:-2]

    tex_code = rf"""
    \documentclass{{article}}
    \usepackage[margin=0pt]{{geometry}}
    \usepackage{{amsmath}}
    \pagestyle{{empty}}
    \begin{{document}}
    \[
    {formula}
    \]
    \end{{document}}
    """

    with open("temp.tex", "w") as f:
        f.write(tex_code)

    try:
        pdflatex = "/Library/TeX/texbin/pdflatex"
        subprocess.run([pdflatex, "temp.tex"], check=True)
        os.rename("temp.pdf", output_pdf)
        print(f"PDF gerado: {output_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao compilar LaTeX: {e}")
    finally:
        for ext in [".aux", ".log", ".tex"]:
            if os.path.exists("temp" + ext):
                os.remove("temp" + ext)


# Exemplo de uso
# render_latex("$$sq(x) = ( ( ( 40 - x ) \\times x ) + ( x + t ) )$$")
