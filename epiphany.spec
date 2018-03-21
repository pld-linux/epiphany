%define		basever		3.28
Summary:	Epiphany - WebKit-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en WebKit
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	3.28.0.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/3.28/%{name}-%{version}.tar.xz
# Source0-md5:	3e127d843d3f255f426ab34804f29163
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	appstream-glib-devel
BuildRequires:	avahi-devel >= 0.6.22
BuildRequires:	avahi-gobject-devel >= 0.6.22
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gcr-ui-devel >= 3.6.0
BuildRequires:	gdk-pixbuf2-devel >= 2.36.5
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.46.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 3.6.0
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	gtk-webkit4-devel >= 2.19.5
BuildRequires:	iso-codes >= 0.53
BuildRequires:	json-glib-devel >= 1.2.0
BuildRequires:	libicu-devel
BuildRequires:	libnotify-devel >= 0.5.1
BuildRequires:	libsecret-devel >= 0.14
BuildRequires:	libsoup-devel >= 2.48.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libwnck-devel
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	libxslt-devel >= 1.1.20
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	nss-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	ca-certificates
Requires:	dbus >= 1.0.2
Requires:	gdk-pixbuf2 >= 2.36.5
Requires:	glib2 >= 1:2.46.0
Requires:	gnome-icon-theme >= 3.4.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.22.0
Requires:	gtk-webkit4 >= 2.16.0
Requires:	hicolor-icon-theme
Requires:	json-glib >= 1.2.0
Requires:	libsoup >= 2.48.0
Provides:	wwwbrowser
Obsoletes:	epiphany-apidocs < 3.8.0-2
Obsoletes:	epiphany-devel < 3.8.0-2
Obsoletes:	epiphany-extensions < 3.8.0
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME browser based on WebKit.

%description -l es.UTF-8
Navigador Web de GNOME basado en WebKit.

%description -l pl.UTF-8
Epiphany jest przeglądarką WWW opartą na silniku WebKit.

%prep
%setup -q

%build
%meson build

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/{,web-extensions/}*.la

%find_lang %{name} --with-gnome --with-omf

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/epiphany
%dir %{_libdir}/epiphany
%attr(755,root,root) %{_libdir}/epiphany/ephy-profile-migrator
%attr(755,root,root) %{_libdir}/epiphany/libephymain.so
%attr(755,root,root) %{_libdir}/epiphany/libephymisc.so
%dir %{_libdir}/epiphany/web-extensions
%attr(755,root,root) %{_libdir}/epiphany/web-extensions/libephywebextension.so
%{_datadir}/appdata/org.gnome.Epiphany.appdata.xml
%{_datadir}/dbus-1/services/org.gnome.EpiphanySearchProvider.service
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_datadir}/gnome-shell/search-providers/epiphany-search-provider.ini
%{_desktopdir}/org.gnome.Epiphany.desktop
%{_iconsdir}/hicolor/*/*/org.gnome.Epiphany*.png
%{_iconsdir}/hicolor/symbolic/*/org.gnome.Epiphany*.svg
%attr(755,root,root) %{_libdir}/epiphany-search-provider
%{_mandir}/man1/epiphany.1*
