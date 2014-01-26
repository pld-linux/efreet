# NOTE: for versions >= 1.8 see efl.spec
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		ecore_ver	1.7.10
%define		eet_ver		1.7.10
%define		eina_ver	1.7.10

Summary:	freedesktop.org standards implementation for the EFL
Summary(pl.UTF-8):	Implementacja standardów freedesktop.org dla EFL
Name:		efreet
Version:	1.7.10
Release:	1
License:	BSD
Group:		X11/Libraries
Source0:	http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	4aa5d4a677abd2d5a013ccfe61be8824
URL:		http://trac.enlightenment.org/e/wiki/Efreet
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	ecore-file-devel >= %{ecore_ver}
BuildRequires:	eet-devel >= %{eet_ver}
BuildRequires:	eina-devel >= %{eina_ver}
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.22
Requires:	ecore >= %{ecore_ver}
Requires:	ecore-file >= %{ecore_ver}
Requires:	eet >= %{eet_ver}
Requires:	eina >= %{eina_ver}
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
Requires:	ecore-devel >= %{ecore_ver}
Requires:	ecore-file-devel >= %{ecore_ver}
Requires:	eet-devel >= %{eet_ver}
Requires:	eina-devel >= %{eina_ver}

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

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# just tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/efreet_{alloc,menu_alloc,test,spec_test,cache_test}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/test

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/efreet_icon_cache_dump
%attr(755,root,root) %{_libdir}/libefreet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libefreet.so.1
%attr(755,root,root) %{_libdir}/libefreet_mime.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libefreet_mime.so.1
%attr(755,root,root) %{_libdir}/libefreet_trash.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libefreet_trash.so.1
%dir %{_libdir}/efreet
%attr(755,root,root) %{_libdir}/efreet/efreet_desktop_cache_create
%attr(755,root,root) %{_libdir}/efreet/efreet_icon_cache_create

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libefreet.so
%attr(755,root,root) %{_libdir}/libefreet_mime.so
%attr(755,root,root) %{_libdir}/libefreet_trash.so
%{_libdir}/libefreet.la
%{_libdir}/libefreet_mime.la
%{_libdir}/libefreet_trash.la
%{_includedir}/efreet-1
%{_pkgconfigdir}/efreet.pc
%{_pkgconfigdir}/efreet-mime.pc
%{_pkgconfigdir}/efreet-trash.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libefreet.a
%{_libdir}/libefreet_mime.a
%{_libdir}/libefreet_trash.a
%endif
