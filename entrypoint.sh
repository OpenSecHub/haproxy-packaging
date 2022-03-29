#!/bin/bash
set -ex

MODULE=haproxy


mkdir -p ~/rpmbuild/{BUILD,RPMS,SRPMS,SOURCES,SPECS}

cp -f ${MODULE}.spec     ~/rpmbuild/SPECS/
cp -f ${MODULE}.cfg      ~/rpmbuild/SOURCES/
cp -f ${MODULE}.service  ~/rpmbuild/SOURCES/

# download sources
spectool -g -R ~/rpmbuild/SPECS/${MODULE}.spec

# install build-deps
#yum-builddep -y ~/rpmbuild/SPECS/${MODULE}.spec

# build rpm package
rpmbuild -v -ba ~/rpmbuild/SPECS/${MODULE}.spec 2>&1 | tee ~/rpmbuild/build.log