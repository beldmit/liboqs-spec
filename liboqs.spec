%global oqs_version 0.7.2
Name:       liboqs
Version:    %{oqs_version}
Release:    0%{?dist}
Summary:    liboqs is an open source C library for quantum-safe cryptographic algorithms.

License:    MIT
URL:        https://github.com/open-quantum-safe/liboqs.git

Source:     liboqs-%{oqs_version}.tar.gz
Patch01:    01-nowerror.patch
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: astyle
BuildRequires: openssl-devel
BuildRequires: python3-pytest
BuildRequires: python3-pytest-xdist
BuildRequires: unzip
BuildRequires: xsltproc
#BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: python3-yaml
BuildRequires: valgrind

%description
liboqs provides:
 - a collection of open source implementations of quantum-safe key encapsulation mechanism (KEM) and digital signature algorithms; the full list can be found below
 - a common API for these algorithms
 - a test harness and benchmarking routines
liboqs is part of the Open Quantum Safe (OQS) project led by Douglas Stebila and Michele Mosca, which aims to develop and integrate into applications quantum-safe cryptography to facilitate deployment and testing in real world contexts. In particular, OQS provides prototype integrations of liboqs into TLS and SSH, through OpenSSL and OpenSSH.

%package devel
Summary:          Development libraries for liboqs
Requires:         liboqs%{?_isa} = %{version}-%{release}

%description devel
Header and Library files for doing development with liboqs.

%prep
%setup -T -b 0 -q -n liboqs-%{oqs_version}
%autopatch -p1

%build
#%cmake -GNinja -DBUILD_SHARED_LIBS=ON -DOQS_ALGS_ENABLED=STD -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT -DCMAKE_INSTALL_LIBDIR=$RPM_BUILD_ROOT/%{_libdir} -DCMAKE_INSTALL_INCLUDEDIR=$RPM_BUILD_ROOT/%{_includedir}
%cmake -GNinja -DBUILD_SHARED_LIBS=ON -DOQS_ALGS_ENABLED=STD -DCMAKE_BUILD_TYPE=Debug
#OQS_VERSION=$(grep OQS_VERSION_TEXT ../include/oqs/oqsconfig.h)
#OQS_VERSION=${OQS_VERSION##\#*OQS_VERSION_TEXT \"}
#OQS_VERSION=${OQS_VERSION%\"}
#echo $OQS_VERSION
#if [ "%{oqs_version}" != "${OQS_VERSION}" ]; then
#   echo "Spec oqs version %{oqs_version} != Library version ${OQS_VERSION}"
#   echo "Need to update the liboqs.spec"
#   exit 1;
#fi
%cmake_build
#ninja gen_docs
#TODO tests

%install
find . -name "*.cmake"
DESTDIR= cmake --install "%{_vpath_builddir}" -v
for i in liboqsTargets.cmake liboqsTargets-debug.cmake
do
  cp $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i /tmp/$i
  sed -e "s;$RPM_BUILD_ROOT;;g" /tmp/$i   > $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i
  rm /tmp/$i
done

%files
%{_libdir}/liboqs.so.%{oqs_version}

%files devel
%{_libdir}/liboqs.so
%{_libdir}/liboqs.so.2
%dir %{_includedir}/oqs
%{_includedir}/oqs/*
%dir %{_libdir}/cmake/liboqs
%{_libdir}/cmake/liboqs/liboqsTargets.cmake
%{_libdir}/cmake/liboqs/liboqsTargets-debug.cmake
%{_libdir}/cmake/liboqs/liboqsConfig.cmake
%{_libdir}/cmake/liboqs/liboqsConfigVersion.cmake
#%dir %%{_datadir}/doc/oqs
#%doc %%{_datadir}/doc/oqs/html/*
#%doc %%{_datadir}/doc/oqs/xml/*

%changelog
