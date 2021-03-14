Summary:	Epiphany - WebKit-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en WebKit
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	3.38.3
Release:	1
License:	GPL v3+
Group:		X11/Applications/Networking
Source0:	https://download.gnome.org/sources/epiphany/3.38/%{name}-%{version}.tar.xz
# Source0-md5:	e2e53c42f0ce20acf45ff651b403a321
URL:		https://wiki.gnome.org/Apps/Web
BuildRequires:	appstream-glib
BuildRequires:	cairo-devel >= 1.2
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gcr-ui-devel >= 3.6.0
BuildRequires:	gdk-pixbuf2-devel >= 2.36.5
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.61.2
BuildRequires:	gmp-devel
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.24.0
BuildRequires:	gtk-webkit4-devel >= 2.29.3
BuildRequires:	iso-codes >= 0.53
BuildRequires:	json-glib-devel >= 1.2.4
BuildRequires:	libdazzle-devel >= 3.37.1
BuildRequires:	libhandy1-devel >= 0.90.0
BuildRequires:	libnotify-devel >= 0.5.1
BuildRequires:	libportal-devel >= 0.0.2
BuildRequires:	libsecret-devel >= 0.19.0
BuildRequires:	libsoup-devel >= 2.48.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	meson >= 0.46.0
BuildRequires:	nettle-devel >= 3.4
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.22
BuildRequires:	tar >= 1:1.22
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
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.24.0
Requires:	gtk-webkit4 >= 2.29.3
Requires:	hicolor-icon-theme
Requires:	iso-codes >= 0.53
Requires:	json-glib >= 1.2.4
Requires:	libdazzle >= 3.37.1
Requires:	libhandy1 >= 0.90.0
Requires:	libnotify >= 0.5.1
Requires:	libportal >= 0.0.2
Requires:	libsecret >= 0.19.0
Requires:	libsoup >= 2.48.0
Requires:	libxml2 >= 1:2.6.28
Requires:	nettle >= 3.4
Requires:	sqlite3 >= 3.22
Provides:	wwwbrowser
Obsoletes:	epiphany-apidocs < 3.8.0-2
Obsoletes:	epiphany-devel < 3.8.0-2
Obsoletes:	epiphany-extensions < 3.8.0
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
