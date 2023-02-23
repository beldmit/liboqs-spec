%global oqs_version 0.7.2
Name:       liboqs
Version:    %{oqs_version}
Release:    1%{?dist}
Summary:    liboqs is an open source C library for quantum-safe cryptographic algorithms.

#liboqs uses MIT license by itself but includes several files licensed under different terms.
#src/common/crypto/sha3/xkcp_low/.../KeccakP-1600-AVX2.s : BSD-like CRYPTOGAMS license
#src/common/rand/rand_nist.c: See file
#see https://github.com/open-quantum-safe/liboqs/blob/main/README.md#license for more details
License:    MIT AND Apache 2.0 AND BSD 3-Clause AND (BSD-3-Clause OR GPL-1.0-or-later) AND CC0-1.0 AND Unlicense
URL:        https://github.com/open-quantum-safe/liboqs.git
Source:     https://github.com/open-quantum-safe/liboqs/archive/refs/tags/0.7.2.tar.gz

#-Werror is not future-compatible
Patch:    01-nowerror.patch
#Fix some gcc13 warnings to build correctly on Fedora 38
Patch:    02-oqs_status_fix.patch

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
%cmake -GNinja -DBUILD_SHARED_LIBS=ON -DOQS_ALGS_ENABLED=NIST_R4 -DCMAKE_BUILD_TYPE=Debug -DOQS_USE_AVX2_INSTRUCTIONS=OFF -DOQS_USE_AVX512_INSTRUCTIONS=OFF -LAH ..
%cmake_build
#ninja gen_docs

%check
#TODO tests
cd "%{_vpath_builddir}"
ninja run_tests

%install
%cmake_install
for i in liboqsTargets.cmake liboqsTargets-debug.cmake
do
  cp $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i /tmp/$i
  sed -e "s;$RPM_BUILD_ROOT;;g" /tmp/$i   > $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i
  rm /tmp/$i
done

%files
%license LICENSE.txt
%{_libdir}/liboqs.so.%{oqs_version}
%{_libdir}/liboqs.so.2

%files devel
%{_libdir}/liboqs.so
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
* Mon Feb 13 2023 Dmitry Belyavskiy - 0.7.2-1
- Initial build of liboqs for Fedora

