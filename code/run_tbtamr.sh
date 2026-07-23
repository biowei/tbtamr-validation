#!/bin/bash
# tbtAMR runner wrapper — pins osx-64 emulated env + Java for snpEff
export HOME=/tmp/tbhome
export JAVA_HOME=/tmp/tbenv/lib/jvm
export PATH=/tmp/tbenv/lib/jvm/bin:/tmp/tbenv/bin:$PATH
export MAMBA_ROOT_PREFIX=/tmp/tbroot
exec "$@"
