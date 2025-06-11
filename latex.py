import subprocess
import os


def render_latex(formula: str, output_pdf: str = "output.pdf"):
    # … remove delimitadores $$ … $$ se houver …
    if formula.startswith("$$") and formula.endswith("$$"):
        formula = formula[2:-2]

    # agora SIM criamos o tex_code como raw string,
    # preservando o '\' de '\times'
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

    # escreve o temp.tex apenas uma vez
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


render_latex("$$ sq(x) = ( ( ( 40 - x ) \\times x ) + ( 5 + 10 ) ) $$")
