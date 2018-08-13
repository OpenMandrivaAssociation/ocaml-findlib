%define up_name	findlib
%define debug_package          %{nil}
# hacky workaround to be fixed!
%define __noautoreq '/usr/bin/ocamlrun'

Summary:	A module packaging tool for OCaml
Name:		ocaml-%{up_name}
Version:	1.8.0
Release:	1
Group:		Development/Other
License:	MIT-style
Url:            http://projects.camlcity.org/projects/findlib.html
Source0:        http://download.camlcity.org/download/%{up_name}-%{version}.tar.gz
BuildRequires:  ocaml-compiler
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-camlp4
BuildRequires:  ocaml-x11
BuildRequires:	pkgconfig(ncurses)
Requires:       ocaml-compiler = %(rpm -q --qf '%{VERSION}' ocaml-compiler)
Obsoletes:      %{up_name}

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

%package	devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{up_name}-%{version}

%build
./configure \
	-mandir %{_mandir} \
	-config %{_sysconfdir}/findlib.conf \
	-sitelib `ocamlc -where` \
	-with-toolbox
%make all
%ifnarch %arm %mips
%make opt
%endif

%install
%make prefix=%{buildroot} PREFIX=%{buildroot} install 

%files
%doc LICENSE
%config(noreplace) %{_sysconfdir}/findlib.conf
%{_bindir}/*
%{_mandir}/man*/*
%{_libdir}/ocaml/bigarray
%{_libdir}/ocaml/bytes
%{_libdir}/ocaml/compiler-libs/META
%{_libdir}/ocaml/dynlink
%{_libdir}/ocaml/findlib
%{_libdir}/ocaml/graphics
%{_libdir}/ocaml/stdlib
%{_libdir}/ocaml/str
%{_libdir}/ocaml/threads/META
%{_libdir}/ocaml/topfind
%{_libdir}/ocaml/raw_spacetime/META
%{_libdir}/ocaml/ocamldoc/META

%{_libdir}/ocaml/unix
%ifnarch %arm
%exclude %{_libdir}/ocaml/findlib/*.a
%exclude %{_libdir}/ocaml/findlib/*.cmxa
%endif
%exclude %{_libdir}/ocaml/findlib/*.mli
%exclude %{_libdir}/ocaml/findlib/Makefile.config

%files devel
%doc LICENSE doc doc/README doc/guide-html
%ifnarch %arm
%{_libdir}/ocaml/findlib/*.a
%{_libdir}/ocaml/findlib/*.cmxa
%endif
%{_libdir}/ocaml/findlib/*.mli
%{_libdir}/ocaml/findlib/Makefile.config
