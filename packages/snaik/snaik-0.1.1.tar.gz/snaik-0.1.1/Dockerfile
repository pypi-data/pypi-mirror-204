FROM python:3.10 as snaik

COPY . /snaik
WORKDIR /snaik

RUN apt-get update
RUN apt-get install --no-install-recommends -qqy \
          libxkbcommon-x11-0 \
          x11-utils \
          libyaml-dev \
          libegl1-mesa \
          libxcb-icccm4 \
          libxcb-image0 \
          libxcb-keysyms1 \
          libxcb-randr0 \
          libxcb-render-util0 \
          libxcb-xinerama0 \
          libopengl0 \
          libdbus-1-3 \
          libxcb-cursor0 \
          && apt-get clean


# Install dependencies
# Make a temp copy so rebuilds are fast when requirements don't change
COPY requirements-pinned.txt /tmp/requirements-pinned.txt
RUN pip install \
    --no-cache-dir --no-warn-script-location -r /tmp/requirements-pinned.txt \
    && rm /tmp/requirements-pinned.txt

RUN pip install --no-cache-dir -e . --no-dependencies

FROM snaik as compile
WORKDIR /snaik

RUN pip install --no-cache-dir pyinstaller

RUN pyinstaller \
        snaik/__main__.py \
        --clean \
        --noconfirm \
        --log-level=WARN \
        --add-data "snaik/resources:snaik/resources" \
        --name=snaik.app \
        --distpath=/dist

CMD ["/bin/bash"]
