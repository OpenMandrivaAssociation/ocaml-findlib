%define up_name	findlib
%define debug_package          %{nil}

Summary:	A module packaging tool for OCaml
Name:		ocaml-%{up_name}
Version:	1.3.3
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
%make all
%ifnarch %arm %mips
%make opt
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
%{_libdir}/ocaml/compiler-libs
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


%changelog
* Sun Apr 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.2.7-1
+ Revision: 652334
- do parallel build
- cleanups
- new version

* Wed Oct 06 2010 Funda Wang <fwang@mandriva.org> 1.2.6-2mdv2011.0
+ Revision: 583377
- rebuild for ocaml

* Mon Aug 23 2010 Florent Monnier <blue_prawn@mandriva.org> 1.2.6-1mdv2011.0
+ Revision: 572365
- updated to last version 1.2.6

* Fri Sep 25 2009 Olivier Blin <oblin@mandriva.com> 1.2.4-5mdv2010.0
+ Revision: 448919
- fix build on platforms without ocaml*opt, by disabling make opt on
  arm & mips (from Arnaud Patard)

* Fri Sep 11 2009 Florent Monnier <blue_prawn@mandriva.org> 1.2.4-4mdv2010.0
+ Revision: 438522
- restore the previous management of the META files of the standard library

* Wed Sep 09 2009 Florent Monnier <blue_prawn@mandriva.org> 1.2.4-3mdv2010.0
+ Revision: 435980
- along with the "revision 435784" of the package ocaml, it will be easier to keep these META files up to date in this package

* Sat Jun 27 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.4-2mdv2010.0
+ Revision: 389775
- rebuild

* Thu Jun 11 2009 Florent Monnier <blue_prawn@mandriva.org> 1.2.4-1mdv2010.0
+ Revision: 385095
- updated version

* Wed Dec 24 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.3-1mdv2009.1
+ Revision: 318141
- rename package from findlib, for general consistency with ocaml naming policy
- use standard ocaml lib directory root for packages installation, instead of
  site-libe hierarchy, as per fedora and debian policies
- new version
- no more mini subpackage, but new devel subpackage
- build toolbox, as per fedora package
- package renaming

* Tue Dec 09 2008 Pixel <pixel@mandriva.com> 0:1.2.2-2mdv2009.1
+ Revision: 312166
- rebuild

* Thu Aug 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0:1.2.2-1mdv2009.0
+ Revision: 272039
- new version

* Tue Mar 04 2008 Stefan van der Eijk <stefan@mandriva.org> 0:1.1.2-0.pl1.3mdv2008.1
+ Revision: 178241
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.1.2-0.pl1.2mdv2008.1
+ Revision: 136415
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0:1.1.2-0.pl1.2mdv2008.0
+ Revision: 89641
- rebuild

* Thu Jun 07 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 0:1.1.2-0.pl1.1mdv2008.0
+ Revision: 36818
- new release: 1.1.2pl3
- fix installation of safe_camlp4 (P0)
- wipe out buildroot before install

* Tue May 29 2007 Pixel <pixel@mandriva.com> 0:1.1.1-7mdv2008.0
+ Revision: 32507
- rebuild with new ocaml

