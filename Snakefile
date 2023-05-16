
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
#     cache
#         True
    output:
        "src/data/stars_args.pkl",
        "src/data/planets_args.pkl",
        "src/data/sample.pkl"
    script:
        "src/scripts/hzied_pipeline.py"
