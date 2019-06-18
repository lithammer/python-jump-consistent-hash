#!/bin/sh -ex

if [ -z "$PLAT" ]; then
    echo environment variable \$PLAT not set
    exit 1
fi

python() {
    [ -z "$pybin" ] && exit 1
    "$pybin/python" "$@"
}

pip() {
    python -m pip "$@"
}

pytest() {
    python -m pytest "$@"
}

# Compile wheels.
for pybin in /opt/python/*/bin; do
    pip wheel /shared -w wheelhouse/
done

# Bundle external shared libraries into the wheels.
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat "$PLAT" -w /shared/wheelhouse/
done

# Install packages and test.
for pybin in /opt/python/*/bin; do
    pip install jump-consistent-hash --no-index -f /shared/wheelhouse/
    pip install pytest
    pytest /shared/tests
done
