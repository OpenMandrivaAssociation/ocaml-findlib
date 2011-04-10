%define up_name	findlib

Summary:	A module packaging tool for OCaml
Name:		ocaml-%{up_name}
Version:	1.2.7
Release:	1
Group:		Development/Other
License:	MIT-style
Url:		http://www.ocaml-programming.de/packages/documentation/findlib/
Source0:	http://www.ocaml-programming.de/packages/%{up_name}-%{version}.tar.gz
BuildRequires:	ocaml >= 0:3.10
BuildRequires:	camlp4
BuildRequires:	ocaml-labltk
BuildRequires:	ncurses-devel
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
make all
%ifnarch %arm %mips
make opt
%endif

%install
%make prefix=%{buildroot} PREFIX=%{buildroot} install 

# don't ship META files for standard library in this package,
# they are included in ocaml package,
# [IMPORTANT] so when this package is updated, update too
# the tarball that contain these files (Source5) in the ocaml package!
rm -f %{buildroot}%{_libdir}/ocaml/bigarray/META
rm -f %{buildroot}%{_libdir}/ocaml/camlp4/META
rm -f %{buildroot}%{_libdir}/ocaml/dbm/META
rm -f %{buildroot}%{_libdir}/ocaml/dynlink/META
rm -f %{buildroot}%{_libdir}/ocaml/graphics/META
rm -f %{buildroot}%{_libdir}/ocaml/labltk/META
rm -f %{buildroot}%{_libdir}/ocaml/num/META
rm -f %{buildroot}%{_libdir}/ocaml/num-top/META
rm -f %{buildroot}%{_libdir}/ocaml/stdlib/META
rm -f %{buildroot}%{_libdir}/ocaml/str/META
rm -f %{buildroot}%{_libdir}/ocaml/threads/META
rm -f %{buildroot}%{_libdir}/ocaml/unix/META
rm -f %{buildroot}%{_libdir}/ocaml/ocamlbuild/META
# In order to update the [Source5] field of ocaml.spec,
# in the findlib source directory run the ./configure script
# with camlp4 and ocaml-labltk properly installed, then:
# tar cfj  findlib-1.2.4-ocaml-3.11.1-meta-files.tar.bz2  site-lib-src/*/META

%files
%doc LICENSE
%config(noreplace) %{_sysconfdir}/findlib.conf
%{_bindir}/*
%{_mandir}/man*/*
%{_libdir}/ocaml/findlib
%{_libdir}/ocaml/topfind
%{_libdir}/ocaml/num-top
%exclude %{_libdir}/ocaml/findlib/*.a
%exclude %{_libdir}/ocaml/findlib/*.cmxa
%exclude %{_libdir}/ocaml/findlib/*.mli
%exclude %{_libdir}/ocaml/findlib/Makefile.config
%exclude %{_libdir}/ocaml/findlib/make_wizard
%exclude %{_libdir}/ocaml/findlib/make_wizard.pattern

%files devel
%doc LICENSE doc doc/README doc/guide-html
%{_libdir}/ocaml/findlib/*.a
%{_libdir}/ocaml/findlib/*.cmxa
%{_libdir}/ocaml/findlib/*.mli
%{_libdir}/ocaml/findlib/Makefile.config
%{_libdir}/ocaml/findlib/make_wizard
%{_libdir}/ocaml/findlib/make_wizard.pattern
