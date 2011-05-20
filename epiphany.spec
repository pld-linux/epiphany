%define		basever		3.0
Summary:	Epiphany - WebKit-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en WebKit
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	3.0.3
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/3.0/%{name}-%{version}.tar.bz2
# Source0-md5:	3227d5e94f881d8a6009f945ed573e8e
Patch0:		%{name}-pld-homepage.patch
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	NetworkManager-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	avahi-devel >= 0.6.22
BuildRequires:	avahi-gobject-devel >= 0.6.22
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.0.2
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gtk-webkit3-devel >= 1.4.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes >= 0.53
BuildRequires:	libgnome-keyring-devel >= 2.28.0
BuildRequires:	libsoup-gnome-devel >= 2.34.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	libxslt-devel >= 1.1.20
BuildRequires:	nss-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
BuildRequires:	seed-devel >= 2.28.0
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	scrollkeeper
Requires:	ca-certificates
Requires:	dbus >= 1.0.2
Requires:	gnome-icon-theme >= 2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-webkit3 >= 1.4.0
Requires:	hicolor-icon-theme
Provides:	wwwbrowser
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME browser based on WebKit.

%description -l es.UTF-8
Navigador Web de GNOME basado en WebKit.

%description -l pl.UTF-8
Epiphany jest przeglądarką WWW opartą na silniku WebKit.

%package devel
Summary:	Epiphany header files
Summary(es.UTF-8):	Ficheros de cabecera de Epiphany
Summary(pl.UTF-8):	Pliki nagłówkowe Epiphany
Group:		X11/Applications/Networking
# doesn't require base
Requires:	gtk+3-devel >= 3.0.2
Requires:	gtk-webkit3-devel >= 1.4.0
Requires:	libxml2-devel >= 1:2.6.28

%description devel
Epiphany header files for plugin development.

%description devel -l es.UTF-8
Ficheros de cabecera de Epiphany para desarrollar plug-ins.

%description devel -l pl.UTF-8
Pliki nagłówkowe Epiphany do tworzenia wtyczek.

%package apidocs
Summary:	Epiphany API documentation
Summary(pl.UTF-8):	Dokumentacja API Epiphany
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Epiphany API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Epiphany.

%prep
%setup -q
%patch0 -p1

%build
%{__gnome_doc_prepare}
%{__gnome_doc_common}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules \
	--disable-schemas-compile \
	--with-distributor-name="PLD Linux" \
	--with-ca-file=/etc/certs/ca-certificates.crt \
	--enable-network-manager \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/%{basever}/extensions

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/epiphany
%attr(755,root,root) %{_bindir}/ephy-profile-migrator
%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%{_datadir}/%{name}
%{_datadir}/GConf/gsettings/epiphany.convert
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_desktopdir}/bme.desktop
%{_desktopdir}/epiphany.desktop
%{_iconsdir}/*/*/apps/*.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{basever}
%dir %{_libdir}/%{name}/%{basever}/extensions
%{_libdir}/girepository-1.0/Epiphany-*.typelib
%{_libdir}/girepository-1.0/EphyEgg-*.typelib
%{_mandir}/man1/epiphany.1*

%files devel
%defattr(644,root,root,755)
%{_aclocaldir}/epiphany.m4
%{_includedir}/epiphany
%{_pkgconfigdir}/epiphany-*.pc
%{_datadir}/gir-1.0/Epiphany-*.gir
%{_datadir}/gir-1.0/EphyEgg-*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/epiphany
