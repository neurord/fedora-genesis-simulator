%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global realname genesis
%global instdir %{_datadir}/%{name}

Name: %{realname}-simulator
Summary: A general purpose simulation platform
Version: 2.3
Release: 2%{?dist}
Url: http://www.genesis-sim.org/GENESIS/
Source0: http://www.genesis-sim.org/GENESIS/genesis-ftp/%{realname}-%{version}-src.tar.bz2
License: GPLv2.1+ and LGPLv2.1+

BuildRequires: bison flex flex-devel
BuildRequires: ncurses-devel
BuildRequires: libX11-devel libXt-devel
BuildRequires: netcdf-devel

%description
GENESIS (short for GEneral NEural SImulation System) is a general
purpose simulation platform that was developed to support the
simulation of neural systems ranging from subcellular components and
biochemical reactions to complex models of single neurons, simulations
of large networks, and systems-level models. As such, GENESIS, and its
version for parallel and networked computers (PGENESIS) was the first
broad scale modeling system in computational biology to encourage
modelers to develop and share model features and components. Most
current GENESIS applications involve realistic simulations of
biological neural systems. Although the software can also model more
abstract networks, other simulators are more suitable for
backpropagation and similar connectionist modeling.

%package devel
Summary: Static library and tools for building genesis extensions
%description devel
%{_summary}.

%package docs
BuildArch: noarch
Summary: Documentation for %{name}
%description docs
%{_summary}.

%ifarch x86_64
%global extraflags -DLONGWORDS
%endif

%prep
%setup -q -n %{realname}-%{version}/%{realname}
rm -rf ./src/diskio/interface/netcdf/netcdf-3.4
sed -i 's/netcdflib.o: netcdflib/netcdflib.o:/' ./src/diskio/interface/netcdf/Makefile
cp src/Makefile.dist src/Makefile
cat >>src/Makefile <<EOF
MACHINE=Linux
OS=BSD
XLIB=%{_libdir}
CC=gcc
CPP=cpp -P
CFLAGS=-O2 -D__NO_MATH_INLINES %{?extraflags}
LD=ld
RANLIB=ranlib
AR=ar
YACC=bison -y
LEX=flex -l
LEXLIB=-lfl
LIBS=\$(LEXLIB) -lm -lnetcdf
TERMCAP=-lncurses
TERMOPT=-DTERMIO -DDONT_USE_SIGIO
NETCDFOBJ = \
        \$(DISKIODIR)/interface/\$(NETCDFSUBDIR)/netcdflib.o
EOF

%build
# if arch == 32: CFLAGS='-O2 -D__NO_MATH_INLINES'
make -C src %{?_smp_mflags} genesis

%install
make -C src install INSTALLDIR=%{buildroot}%{_libdir}/genesis
rm -r %{buildroot}%{_libdir}/genesis/{src,man}
rm -v %{buildroot}%{_libdir}/genesis/.*simrc
chmod -x %{buildroot}%{_libdir}/genesis/startup/*

mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_libdir}/genesis/genesis %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_includedir}
mv %{buildroot}%{_libdir}/genesis/include %{buildroot}%{_includedir}/genesis

mkdir -p %{buildroot}%{_pkgdocdir}
mv %{buildroot}%{_libdir}/genesis/{Doc,Tutorials,Hyperdoc} %{buildroot}%{_pkgdocdir}/

mv %{buildroot}%{_libdir}/genesis/bin/convert %{buildroot}%{_bindir}/genesis-convert
install -D man/man1/convert.1 %{buildroot}%{_mandir}/man1/genesis-convert.1
cp src/libsh %{buildroot}%{_libdir}/genesis/lib

find %{buildroot}%{_libdir}/genesis/startup/ -name '*simrc' -exec \
    sed -i 's|%{buildroot}||g' {} \;

# add emacs mode

%files
%{_bindir}/*
%{_libdir}/%{realname}
%exclude %{_libdir}/%{realname}/lib
%exclude %{_libdir}/%{realname}/*make
%{_mandir}/man1/*
%doc AUTHORS COPYRIGHT CONTACTING.GENESIS ChangeLog GPLicense LGPLicense
%exclude %{_pkgdocdir}/Tutorials/
%exclude %{_pkgdocdir}/Hyperdoc/

%files devel
%doc COPYRIGHT
%{_includedir}/%{realname}/
%{_libdir}/%{realname}/lib
%{_libdir}/%{realname}/*make

%files docs
%dir %doc %{_pkgdocdir}
%doc %{_pkgdocdir}/Tutorials/
%doc %{_pkgdocdir}/Hyperdoc/
