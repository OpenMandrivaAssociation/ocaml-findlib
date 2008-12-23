%define name	findlib
%define version	1.2.2
%define release	%mkrel 2

Summary:	A module packaging tool for OCaml
Name:		findlib
Version:	%{version}
Release:	%{release}
Epoch:		0
Group:		Development/Other
License:	MIT-style
Url:		http://www.ocaml-programming.de/packages/documentation/findlib/
Source0:	http://www.ocaml-programming.de/packages/%{name}-%{version}.tar.gz
BuildRequires:	ocaml >= 0:3.10
BuildRequires:	camlp4
BuildRequires:	ocaml-labltk
BuildRequires:	ncurses-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%package -n	ocamlfind-mini
Summary:	Minimal findlib script to be distributed with user libraries
Group:		Development/Other
Requires:	%{name} = %{epoch}:%{version}-%release

%description
The findlib library provides a scheme to manage reusable software
components (packages), and includes tools that support this scheme.
Packages are collections of OCaml modules for which metainformation can
be stored. The packages are kept in the filesystem hierarchy, but with
strict directory structure. The library contains functions to look the
directory up that stores a package, to query metainformation about a
package, and to retrieve dependency information about multiple packages.
There is also a tool that allows the user to enter queries on the
command-line. In order to simplify compilation and linkage, there are
new frontends of the various OCaml compilers that can directly deal with
packages.

%description -n ocamlfind-mini
ocamlfind-mini is an OCaml script that implements a subset of the full
functionality of ocamlfind. It consists only of one file, so it is easy
to distribute it with any software.

The subset is normally sufficient to compile a library and to install
the library; but it is insufficient to link the library into an
executable. 

%prep
%setup -q

%build
./configure -mandir %{_mandir} -config %{_sysconfdir}/findlib.conf
make all opt

%install
rm -rf %{buildroot}
%make prefix=%{buildroot} PREFIX=%{buildroot} install 

install -d -m 755 %{buildroot}%{_libdir}/ocaml/ocamlfind-mini
cp -a mini/* %{buildroot}%{_libdir}/ocaml/ocamlfind-mini

# don't ship META files for standard library in this package,
# they are included in ocaml package
rm -rf %{buildroot}%{_libdir}/ocaml/site-lib/{unix,str,stdlib,threads,num,labltk,graphics,dynlink,dbm,camlp4,bigarray}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README INSTALL LICENSE doc
%config(noreplace) %{_sysconfdir}/findlib.conf
%{_bindir}/*
%{_libdir}/ocaml/site-lib  
%{_libdir}/ocaml/topfind
%{_mandir}/man*/*

%files -n ocamlfind-mini
%defattr(-,root,root)
%{_libdir}/ocaml/ocamlfind-mini/*

