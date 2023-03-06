%global oqs_version 0.4.0
Name:       oqsprovider
Version:    %{oqs_version}
Release:    1%{?dist}
Summary:    oqsprovider is an OpenSSL provider for quantum-safe algorithms based on liboqs

License:    MIT
URL:        https://github.com/open-quantum-safe/oqs-provider.git
Source:     https://github.com/open-quantum-safe/oqs-provider/archive/refs/tags/0.4.0.tar.gz

##-Werror is not future-compatible
#Patch:    01-nowerror.patch
##Fix some gcc13 warnings to build correctly on Fedora 38
#Patch:    02-oqs_status_fix.patch

Requires: liboqs
Requires: openssl
BuildRequires: ninja-build
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: liboqs-devel
BuildRequires: openssl-devel
#BuildRequires: python3-pytest
#BuildRequires: python3-pytest-xdist
#BuildRequires: unzip
#BuildRequires: xsltproc
##BuildRequires: doxygen
#BuildRequires: graphviz
#BuildRequires: python3-yaml
#BuildRequires: valgrind

%description
oqs-provider fully enables quantum-safe cryptography for KEM key
establishment in TLS1.3 including management of such keys via the OpenSSL (3.0)
provider interface and hybrid KEM schemes. Also, QSC signatures including CMS
functionality are available via the OpenSSL EVP interface. Key persistence is
provided via the encode/decode mechanism and X.509 data structures.

%prep
%setup -T -b 0 -q -n oqs-provider-%{oqs_version}

%build
%cmake -GNinja -DCMAKE_BUILD_TYPE=Debug -LAH ..
%cmake_build
#ninja gen_docs

%check
#TODO tests

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ossl-modules
install %{_vpath_builddir}/oqsprov/oqsprovider.so $RPM_BUILD_ROOT/%{_libdir}/ossl-modules

%files
%license LICENSE.txt
%{_libdir}/ossl-modules/oqsprovider.so

%changelog
* Mon Mar 6 2023 Dmitry Belyavskiy - 0.4.0-1
- Initial build of oqsprovider for Fedora

