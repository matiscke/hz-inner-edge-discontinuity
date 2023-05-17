
# Copy over the static figures
rule static_figures:
    input:
        "src/static/*.pdf"
    output:
        "src/tex/figures/*.pdf"
    shell:
        "cp {input} {output}"

# run the pipeline
rule pipeline:
    conda:
        "environment.yml"
    output:
        directory("src/data/pipeline")
    cache:
        True
    script:
        "src/scripts/hzied_pipeline.py"
