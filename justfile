# set shell := ["cmd.exe", "/C"]

# Clean up generated files
clean-tsp-files:
    rm -f -- *.res *.sol *.000 *.sav *.pul

check-shell:
    echo "Shell: $0"

run-train-sl-ar:
    # call .\.venv\Scripts\activate
    # sh scripts/train-sl-ar.sh
    source .venv/Scripts/activate
    which python
    sh scripts/train-sl-ar.sh

run-eval:
    source .venv/Scripts/activate
    which python
    sh scripts/eval.sh

install:
    #!/bin/sh
    source ./.venv/Scripts/activate

    if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ .venv is not activated. Please make sure you have a .venv folder'" >&2
    exit 1
    fi

    echo "✅ .venv is activated. Installing requirements..."
    pip install -r requirements.txt
