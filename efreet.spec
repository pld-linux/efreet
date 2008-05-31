#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		ecore_ver	0.9.9

Summary:	freedesktop.org standards implementation for the EFL
Summary(pl.UTF-8):	Implementacja standardów freedesktop.org dla EFL
Name:		efreet
Version:	0.0.3.002
Release:	1
License:	BSD
Group:		X11/Libraries
Source0:	http://enlightenment.freedesktop.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	e39b686b04cfa3ef634efe8f95858daf
URL:		http://enlightenment.org/p.php?p=about/libs/efreet
BuildRequires:	autoconf
BuildRequires:	automake >= 1.4
# ecore-file; ecore-desktop for tests
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Requires:	ecore-file >= %{ecore_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Efreet is an implementation of the following specifications from
freedesktop.org:
 - Base Directory - Locations for system and user specific desktop
   configuration files,
 - Desktop Entries - The metadata associated with the applications
   installed on a system,
 - Application Menus - The arrangement of available applications into
   a hierarchical menu,
 - Icon Themes - A means of associating icons with various objects on
   the desktop in a themable fashion.

By following these specifications, Enlightenment 0.17 uses the same
format for describing application launchers, menus and icon themes as
the GNOME, KDE and XFCE Desktop Environments. A system must only
provide a single set of this data for use with any of these desktops.

%description -l pl.UTF-8
Efreet to implementacja następujących specyfikacji z freedesktop.org:
 - Base Directory - położenie plików konfiguracyjnych środowiska dla
   systemu i użytkownika,
 - Desktop Entries - metadane związane z aplikacjami zainstalowanymi w
   systemie,
 - Application Menus - uporządkowanie dostępnych aplikacji w menu
   hierarchiczne,
 - Icon Themes - sposób wiązania ikon z różnymi obiektami w środowisku
   w sposób pozwalający na ustawianie motywów.

%package devel
Summary:	Efreet header files
Summary(pl.UTF-8):	Pliki nagłówkowe Efreet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# ecore-file
BuildRequires:	ecore-devel >= %{ecore_ver}

%description devel
Header files for Efreet.

%description devel -l pl.UTF-8
Pliki nagłówkowe Efreet.

%package static
Summary:	Static Efreet library
Summary(pl.UTF-8):	Statyczna biblioteka Efreet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Efreet library.

%description static -l pl.UTF-8
Statyczna biblioteka Efreet.

%prep
%setup -q

sed -i -e 's/-g -O0//' src/lib/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# just tests
rm $RPM_BUILD_ROOT%{_bindir}/efreet_{alloc,menu_alloc,test,spec_test,cache_test}
rm $RPM_BUILD_ROOT%{_bindir}/{ecore_alloc,compare_results}
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/test

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README TODO
%attr(755,root,root) %{_libdir}/libefreet.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/efreet-config
%attr(755,root,root) %{_libdir}/libefreet.so
%{_libdir}/libefreet.la
%{_includedir}/efreet
%{_pkgconfigdir}/efreet.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libefreet.a
%endif
