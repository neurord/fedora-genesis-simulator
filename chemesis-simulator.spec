%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global realname chemesis
%global instdir %{_datadir}/%{name}

Name:    %{realname}-simulator
Summary: A simulation platform for biochemical reactions
Version: 2.4
Release: 4%{?dist}
Url:     http://krasnow1.gmu.edu/CENlab/software.html
Source0: http://krasnow1.gmu.edu/CENlab/software/chemesis%{version}.tgz
License: GPLv2.1+ and LGPLv2.1+

BuildRequires: bison flex flex-devel
BuildRequires: ncurses-devel
BuildRequires: libX11-devel libXt-devel libXext-devel libXmu-devel
BuildRequires: netcdf-devel
BuildRequires: genesis-simulator-devel

%description
Chemesis is a library of biochemical reaction objects for modeling calcium
concentration. It is an extension of the genesis simulator.

%ifarch x86_64
%global extraflags -DLONGWORDS
%endif

%prep
%setup -q -n %{realname}%{version}

cat >>Makefile <<EOF
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
LIBS += \$(LEXLIB) -lm -lnetcdf
TERMCAP=-lncurses
TERMOPT=-DTERMIO -DDONT_USE_SIGIO
EOF

make clean
rm -f chemesis

%build
make GENESIS_LIB=%{_libdir}/genesis/lib \
     GENESIS_INCLUDE=-I%{_includedir}/genesis \
     SIMLIB='$(GENESIS_LIB)' \
     NETCDFOBJ='$(GENESIS_LIB)/netcdflib.o' \
     SIMSRC='$(SIMLIB)'

%install
install -D chemesis %{buildroot}%{_bindir}/chemesis
mkdir -p %{buildroot}%{_datadir}/chemesis
cp -pr Scripts %{buildroot}%{_datadir}/chemesis/

cp %{_docdir}/genesis-simulator-devel*/COPYRIGHT .

%files
%{_bindir}/chemesis
%{_datadir}/chemesis
%doc COPYRIGHT
