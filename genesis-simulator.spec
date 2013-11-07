%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global realname genesis
%global instdir %{_datadir}/%{name}

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

libgenesis.a:
	@make -f \$(MF) CC="\$(CC)" TMPDIR="\$(TMPDIR)" LD="\$(LD)" CPP="\$(CPP)" YACC="\$(YACC)" LEX="\$(LEX)" LEXLIB="\$(LEXLIB)" OS="\$(OS)" MACHINE="\$(MACHINE)" INSTALLDIR="\$(INSTALLDIR)" INSTALLBIN="\$(INSTALLBIN)" CFLAGS_IN="\$(CFLAGS)" IRIX_HACK="\$(IRIX_HACK)" LDFLAGS="\$(LDFLAGS)" LIBS="\$(LIBS)" MF="\$(MF)" TERMCAP="\$(TERMCAP)" TERMOPT="\$(TERMOPT)" SUBDIR="\$(SUBDIR)" NXSUBDIR="\$(NXSUBDIR)" MINSUBDIR="\$(MINSUBDIR)" BASECODE="\$(BASECODE)" OBJLIBS="\$(OBJLIBS)" EXTRALIBS="\$(EXTRALIBS)" \$@
EOF
cat >>src/Makefile.BASE <<EOF
libgenesis.a: libs \$(GENESIS) \$(XODUS)
	\$(AR) rc \$@ \$(LDFLAGS) \$(GENESIS) \$(XODUS)
EOF

%build
# if arch == 32: CFLAGS='-O2 -D__NO_MATH_INLINES'
make -C src %{?_smp_mflags} genesis
make -C src %{?_smp_mflags} libgenesis.a
# doesn't work if done together :(

%install
test -n "%{buildroot}"
install -D src/genesis %{buildroot}%{_bindir}/genesis
install -D src/convert/convert %{buildroot}%{_bindir}/genesis-convert
install -D man/man1/convert.1 %{buildroot}%{_mandir}/man1/genesis-convert.1
mkdir -p %{buildroot}%{instdir}
cp -rp src/startup %{buildroot}%{instdir}/
cp -rp Scripts %{buildroot}%{instdir}/
install -D src/libgenesis.a %{buildroot}%{_libdir}/libgenesis.a
mkdir -p %{buildroot}%{_libexecdir}/genesis
cp src/sys/code_{func,g,lib,sym} %{buildroot}%{_libexecdir}/genesis/

mkdir -p %{buildroot}%{_pkgdocdir}
cp Doc Tutorials Hyperdoc -r %{buildroot}%{_pkgdocdir}/

cat >>%{buildroot}%{_datadir}/%{name}/startup/.simrc <<EOF
setenv SIMPATH . \
               %{instdir}/startup \
               %{instdir}/Scripts/neurokit \
               %{instdir}/Scripts/neurokit/prototypes
setenv SIMNOTES {getenv HOME}/.genesis-notes
setenv GENESIS_HELP %{_pkgdocdir}/Doc

# set up default schedule
schedule
EOF

# add emacs mode

#make NETCDFOBJ='$(SIMLIB)/netcdflib.o %{_libdir}/libnetcdf.a'

%files
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%doc AUTHORS COPYRIGHT CONTACTING.GENESIS ChangeLog GPLicense LGPLicense
%exclude %{_pkgdocdir}/Tutorials/
%exclude %{_pkgdocdir}/Hyperdoc/

%files devel
%doc COPYRIGHT
%{_libdir}/libgenesis.a
%{_libexecdir}/genesis/

%files docs
%dir %doc %{_pkgdocdir}
%doc %{_pkgdocdir}/Tutorials/
%doc %{_pkgdocdir}/Hyperdoc/
