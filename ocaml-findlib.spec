%define up_name	findlib
%define debug_package          %{nil}
# hacky workaround to be fixed!
%define __noautoreq '/usr/bin/ocamlrun'
%define __ocaml_requires %nil
%global ocaml_version %(rpm -q --qf '%{VERSION}' ocaml-compiler)

Summary:	A module packaging tool for OCaml
Name:		ocaml-%{up_name}
Version:	1.9.6
Release:	1
Group:		Development/Other
License:	MIT-style
Url:            http://projects.camlcity.org/projects/findlib.html
Source0:        http://download.camlcity.org/download/%{up_name}-%{version}.tar.gz
BuildRequires:  ocaml-compiler
BuildRequires:  ocaml-compiler-libs
BuildRequires:	ocaml-ocamlbuild
BuildRequires:	pkgconfig(ncurses)
Requires:       ocaml-compiler = %{ocaml_version}
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

ocamlc -version
ocamlc -where
(cd tools/extract_args && make)
tools/extract_args/extract_args -o src/findlib/ocaml_args.ml ocamlc ocamlcp ocamlmktop ocamlopt ocamldep ocamldoc ||:
cat src/findlib/ocaml_args.ml
./configure -config %{_sysconfdir}/ocamlfind.conf \
  -bindir %{_bindir} \
  -sitelib `ocamlc -where` \
  -mandir %{_mandir} \
  -with-toolbox
make all
%ifnarch %{arm}
make opt
%endif
rm doc/guide-html/TIMESTAMP
%make all

%install
%make prefix=%{buildroot} PREFIX=%{buildroot} install 

# We seem to get this from ocaml-compiler
rm -rf %{buildroot}%{_libdir}/ocaml/dynlink/META \
	%{buildroot}%{_libdir}/ocaml/ocamldoc/META \
	%{buildroot}%{_libdir}/ocaml/stdlib/META \
	%{buildroot}%{_libdir}/ocaml/str/META \
	%{buildroot}%{_libdir}/ocaml/threads/META \
	%{buildroot}%{_libdir}/ocaml/runtime_events/META \
	%{buildroot}%{_libdir}/ocaml/unix/META
# Empty directories are useless
# (They may have been emptied by deleting the superfluous
# duplicated META files)
for i in %{buildroot}%{_libdir}/ocaml/*; do
	rmdir $i || :
done

%files
%doc LICENSE
%config(noreplace) %{_sysconfdir}/ocamlfind.conf
%{_bindir}/*
%{_mandir}/man*/*
%{_libdir}/ocaml/bytes
#{_libdir}/ocaml/compiler-libs/META
%{_libdir}/ocaml/findlib
%{_libdir}/ocaml/topfind
#{_libdir}/ocaml/ocamlbuild/META
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
