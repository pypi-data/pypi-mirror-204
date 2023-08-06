# Main dockerfile is from unix, windows is solely provided for building .exe artifacts
FROM tobix/pywine:3.10 as compile

COPY . /snaik
WORKDIR /snaik

# Install dependencies
# Make a temp copy so rebuilds are fast when requirements don't change
COPY requirements-pinned.txt /tmp/requirements-pinned.txt
RUN wine pip install \
    --no-cache-dir --no-warn-script-location -r /tmp/requirements-pinned.txt \
    && rm /tmp/requirements-pinned.txt

RUN wine pip install --no-cache-dir -e . --no-dependencies --no-warn-script-location

# Build release
RUN wine pyinstaller \
    snaik/__main__.py \
    --clean \
    --noconfirm \
    --log-level=WARN \
    --windowed \
    --add-data "snaik/resources;snaik/resources" \
    --name=snaik \
    --distpath="/dist"

CMD ["/bin/bash"]
