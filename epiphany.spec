Summary:	Epiphany - WebKit-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en WebKit
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	3.34.2
Release:	1
License:	GPL v3+
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/3.34/%{name}-%{version}.tar.xz
# Source0-md5:	ae404e3a70ff904f5a23466727f8a90a
URL:		https://wiki.gnome.org/Apps/Web
BuildRequires:	appstream-glib-devel
BuildRequires:	avahi-devel >= 0.6.22
BuildRequires:	avahi-gobject-devel >= 0.6.22
BuildRequires:	cairo-devel >= 1.2
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gcr-ui-devel >= 3.6.0
BuildRequires:	gdk-pixbuf2-devel >= 2.36.5
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.61.2
BuildRequires:	gnome-desktop-devel >= 3.6.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.24.0
BuildRequires:	gtk-webkit4-devel >= 2.26.0
BuildRequires:	iso-codes >= 0.53
BuildRequires:	json-glib-devel >= 1.2.4
BuildRequires:	libdazzle-devel >= 3.32
BuildRequires:	libhandy-devel >= 0.0.10
BuildRequires:	libicu-devel
BuildRequires:	libnotify-devel >= 0.5.1
BuildRequires:	libsecret-devel >= 0.14
BuildRequires:	libsoup-devel >= 2.48.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libwnck-devel
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	libxslt-devel >= 1.1.20
BuildRequires:	meson >= 0.46.0
BuildRequires:	nettle-devel >= 3.4
BuildRequires:	ninja >= 1.5
BuildRequires:	nss-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.61.2
Requires(post,postun):	gtk-update-icon-cache
Requires:	ca-certificates
Requires:	dbus >= 1.0.2
Requires:	gcr-ui >= 3.6.0
Requires:	gdk-pixbuf2 >= 2.36.5
Requires:	glib2 >= 1:2.61.2
Requires:	gnome-icon-theme >= 3.4.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.24.0
Requires:	gtk-webkit4 >= 2.26.0
Requires:	hicolor-icon-theme
Requires:	iso-codes >= 0.53
Requires:	json-glib >= 1.2.4
Requires:	libdazzle >= 3.32
Requires:	libhandy >= 0.0.10
Requires:	libnotify >= 0.5.1
Requires:	libsecret >= 0.14
Requires:	libsoup >= 2.48.0
Requires:	libxml2 >= 1:2.6.28
Requires:	nettle >= 3.4
Provides:	wwwbrowser
Obsoletes:	epiphany-apidocs < 3.8.0-2
Obsoletes:	epiphany-devel < 3.8.0-2
Obsoletes:	epiphany-extensions < 3.8.0
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Web (codename: Epiphany) is a GNOME web browser based on the
WebKit rendering engine.

%description -l es.UTF-8
Navigador Web de GNOME basado en WebKit.

%description -l pl.UTF-8
GNOME Web (nazwa kodowa: Epiphany) jest przeglądarką WWW dla GNOME
opartą na silniku renderującym WebKit.

%prep
%setup -q

%build
%meson build

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%glib_compile_schemas
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md TODO
%attr(755,root,root) %{_bindir}/epiphany
%dir %{_libdir}/epiphany
%attr(755,root,root) %{_libdir}/epiphany/libephymain.so
%attr(755,root,root) %{_libdir}/epiphany/libephymisc.so
%attr(755,root,root) %{_libdir}/epiphany/libephysync.so
%dir %{_libdir}/epiphany/web-process-extensions
%attr(755,root,root) %{_libdir}/epiphany/web-process-extensions/libephywebprocessextension.so
%attr(755,root,root) %{_libexecdir}/epiphany-search-provider
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/epiphany
%endif
%attr(755,root,root) %{_libexecdir}/epiphany/ephy-profile-migrator
%{_datadir}/dbus-1/services/org.gnome.Epiphany.SearchProvider.service
%{_datadir}/epiphany
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_datadir}/gnome-shell/search-providers/org.gnome.Epiphany.SearchProvider.ini
%{_datadir}/metainfo/org.gnome.Epiphany.appdata.xml
%{_desktopdir}/org.gnome.Epiphany.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Epiphany.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Epiphany-symbolic.svg
%{_mandir}/man1/epiphany.1*
