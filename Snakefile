
# Copy over the static figures
rule static_figures:
    input:
        "src/static/optimistic_statpwr_H2O-f.pdf"
    output:
        "src/tex/figures/optimistic_statpwr_H2O-f.pdf"
    shell:
        "cp {input} {output}"