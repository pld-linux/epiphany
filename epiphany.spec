%define		basever		2.30
Summary:	Epiphany - WebKit-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en WebKit
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	2.30.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/2.30/%{name}-%{version}.tar.bz2
# Source0-md5:	29b084acfa016540d91d3601ec3dff5c
Patch0:		%{name}-pld-homepage.patch
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	GConf2-devel >= 2.28.0
BuildRequires:	NetworkManager-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	avahi-gobject-devel >= 0.6.22
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gtk-webkit-devel >= 1.1.22
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes >= 0.53
BuildRequires:	libgnome-keyring-devel >= 2.28.0
BuildRequires:	libicu-devel
BuildRequires:	libnotify-devel >= 0.4
BuildRequires:	libsoup-gnome-devel >= 2.30.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	libxslt-devel >= 1.1.20
BuildRequires:	nss-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.364
BuildRequires:	scrollkeeper
BuildRequires:	sed >= 4.0
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	ca-certificates
Requires:	dbus >= 1.0.2
Requires:	gnome-icon-theme >= 2.26.0
Provides:	wwwbrowser
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME browser based on WebKit.

%description -l es.UTF-8
Navigador Web de GNOME basado en WebKit.

%description -l pl.UTF-8
Epiphany jest przeglądarką WWW bazującą na WebKit.

%package devel
Summary:	Epiphany header files
Summary(es.UTF-8):	Ficheros de cabecera de Epiphany
Summary(pl.UTF-8):	Pliki nagłówkowe Epiphany
Group:		X11/Applications/Networking
# doesn't require base
Requires:	gtk+2-devel >= 2:2.20.0
Requires:	gtk-webkit-devel >= 1.1.22
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

sed -i -e 's/^en@shaw//' po/LINGUAS
rm -f po/en@shaw.po

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
	--with-distributor-name="PLD Linux" \
	--with-ca-file=/etc/certs/ca-certificates.crt \
	--enable-network-manager \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/%{basever}/extensions

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_iconsdir}/LowContrastLargePrint

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install epiphany-lockdown.schemas
%gconf_schema_install epiphany.schemas
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall epiphany-lockdown.schemas
%gconf_schema_uninstall epiphany.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README

%attr(755,root,root) %{_bindir}/epiphany
%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%{_datadir}/%{name}
%{_desktopdir}/bme.desktop
%{_desktopdir}/epiphany.desktop
%{_iconsdir}/*/*/apps/*.*
%{_sysconfdir}/gconf/schemas/epiphany-lockdown.schemas
%{_sysconfdir}/gconf/schemas/epiphany.schemas
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{basever}
%dir %{_libdir}/%{name}/%{basever}/extensions
%{_libdir}/girepository-1.0/Epiphany-*.typelib
%{_mandir}/man1/epiphany.1*

%files devel
%defattr(644,root,root,755)
%{_aclocaldir}/epiphany.m4
%{_includedir}/epiphany
%{_pkgconfigdir}/epiphany-*.pc
%{_datadir}/gir-1.0/Epiphany-*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/epiphany
