%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global realname genesis

Name: genesis-simulator
Summary: A general purpose simulation platform
Version: 2.3
Release: 1%{?dist}
Url: http://www.genesis-sim.org/GENESIS/
Source0: http://www.genesis-sim.org/GENESIS/genesis-ftp/%{realname}-%{version}-src.tar.bz2
License: GPLv2.1+ plus LGPLv2.1+

BuildRequires: bison flex flex-devel
BuildRequires: ncurses-devel
BuildRequires: libX11-devel libXt-devel

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

%package docs
Summary: Documentation for %{name}
%description docs
%{_summary}.

%ifarch x86_64
%global extraflags -DLONGWORDS
%endif

%prep
%setup -q -n %{realname}-%{version}/%{realname}
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
LIBS=\$(LEXLIB) -lm
TERMCAP=-lncurses
TERMOPT=-DTERMIO -DDONT_USE_SIGIO
EOF

%build
# if arch == 32: CFLAGS='-O2 -D__NO_MATH_INLINES'
make -C src %{?_smp_mflags}

%install
test -n "%{buildroot}"
install -D src/genesis %{buildroot}%{_bindir}/genesis
install -D src/convert/convert %{buildroot}%{_bindir}/genesis-convert
install -D man/man1/convert.1 %{buildroot}%{_mandir}/man1/genesis-convert.1
#find %{buildroot}%{_datarootdir}/%{name} -name *.o -delete

mkdir -p %{buildroot}%{_pkgdocdir}
cp Doc -r %{buildroot}%{_pkgdocdir}/
cp Tutorials -r %{buildroot}%{_pkgdocdir}/
cp Hyperdoc -r %{buildroot}%{_pkgdocdir}/Manual

%files
%{_bindir}/*
%{_mandir}/man1/*
%doc AUTHORS COPYRIGHT CONTACTING.GENESIS ChangeLog GPLicense LGPLicense
%exclude %{_pkgdocdir}/Tutorials/
%exclude %{_pkgdocdir}/Manual/

%files docs
%dir %doc %{_pkgdocdir}
%doc %{_pkgdocdir}/Tutorials/
%doc %{_pkgdocdir}/Manual/
