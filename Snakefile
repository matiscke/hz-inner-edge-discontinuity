
# Copy over the static figures
rule static_figures:
    input:
        "src/static/*.pdf"
    output:
        "src/tex/figures/*.pdf"
    shell:
        "cp {input} {output}"