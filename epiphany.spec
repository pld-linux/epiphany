# TODO: use gtk4-update-icon-cache
#
# Conditional build:
%bcond_with	granite		# elementaryOS integration

Summary:	Epiphany - WebKit-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en WebKit
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	46.0
Release:	1
License:	GPL v3+
Group:		X11/Applications/Networking
Source0:	https://download.gnome.org/sources/epiphany/46/%{name}-%{version}.tar.xz
# Source0-md5:	c284bbbad1c08e218c6aae0068906b6f
URL:		https://wiki.gnome.org/Apps/Web
BuildRequires:	appstream-glib
BuildRequires:	cairo-devel >= 1.2
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gcc >= 6:4.7
BuildRequires:	gcr4-devel >= 3.9.0
BuildRequires:	gdk-pixbuf2-devel >= 2.36.5
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	glib2-devel >= 1:2.74.0
BuildRequires:	gmp-devel
%{?with_granite:BuildRequires:	granite7-devel >= 7.2.0}
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk4-devel >= 4.12.0
BuildRequires:	gtk-webkit6-devel >= 2.43.4
BuildRequires:	iso-codes >= 0.53
BuildRequires:	json-glib-devel >= 1.6
BuildRequires:	libadwaita-devel >= 1.4
BuildRequires:	libarchive-devel
BuildRequires:	libnotify-devel >= 0.5.1
BuildRequires:	libportal-gtk4-devel >= 0.6
BuildRequires:	libsecret-devel >= 0.19.0
BuildRequires:	libsoup3-devel >= 2.99.4
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	meson >= 0.59.0
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
Requires(post,postun):	glib2 >= 1:2.74.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	bubblewrap
Requires:	ca-certificates
Requires:	dbus >= 1.0.2
Requires:	gcr4 >= 3.9.0
Requires:	gdk-pixbuf2 >= 2.36.5
Requires:	glib2 >= 1:2.74.0
Requires:	gsettings-desktop-schemas
Requires:	gtk4 >= 4.12.0
Requires:	gtk-webkit6 >= 2.43.4
Requires:	hicolor-icon-theme
Requires:	iso-codes >= 0.53
Requires:	json-glib >= 1.6
Requires:	libadwaita >= 1.4
Requires:	libnotify >= 0.5.1
Requires:	libportal-gtk4 >= 0.6
Requires:	libsecret >= 0.19.0
Requires:	libsoup3 >= 2.99.4
Requires:	libxml2 >= 1:2.6.28
Requires:	nettle >= 3.4
Requires:	sqlite3 >= 3.22
Requires:	xdg-dbus-proxy
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
%meson build \
	%{?with_granite:-Dgranite=enabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

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
%attr(755,root,root) %{_libdir}/epiphany/web-process-extensions/libephywebextension.so
%attr(755,root,root) %{_libdir}/epiphany/web-process-extensions/libephywebprocessextension.so
%attr(755,root,root) %{_libexecdir}/epiphany-search-provider
%attr(755,root,root) %{_libexecdir}/epiphany-webapp-provider
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/epiphany
%endif
%attr(755,root,root) %{_libexecdir}/epiphany/ephy-profile-migrator
%{_datadir}/dbus-1/services/org.gnome.Epiphany.SearchProvider.service
%{_datadir}/dbus-1/services/org.gnome.Epiphany.WebAppProvider.service
%{_datadir}/epiphany
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_datadir}/gnome-shell/search-providers/org.gnome.Epiphany.SearchProvider.ini
%{_datadir}/metainfo/org.gnome.Epiphany.appdata.xml
%{_desktopdir}/org.gnome.Epiphany.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Epiphany.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Epiphany-symbolic.svg
%{_mandir}/man1/epiphany.1*
