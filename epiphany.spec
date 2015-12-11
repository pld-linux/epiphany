%define		basever		3.18
Summary:	Epiphany - WebKit-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en WebKit
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	3.18.2
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/3.18/%{name}-%{version}.tar.xz
# Source0-md5:	ede1e5e7e420a2f4c6231d185a94250f
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	avahi-devel >= 0.6.22
BuildRequires:	avahi-gobject-devel >= 0.6.22
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gcr-devel >= 3.6.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 3.6.0
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.14.0
BuildRequires:	gtk-webkit4-devel >= 2.10.0
BuildRequires:	intltool >= 0.50.0
BuildRequires:	iso-codes >= 0.53
BuildRequires:	libnotify-devel >= 0.5.1
BuildRequires:	libsecret-devel >= 0.14
BuildRequires:	libsoup-devel >= 2.48.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libwnck-devel
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	libxslt-devel >= 1.1.20
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
Requires:	ca-certificates
Requires:	dbus >= 1.0.2
Requires:	glib2 >= 1:2.38.0
Requires:	gnome-icon-theme >= 3.4.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.14.0
Requires:	gtk-webkit4 >= 2.10.0
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
%{__gnome_doc_prepare}
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
	--with-distributor-name="PLD Linux"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/%{basever}/web-extensions/*.la

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%glib_compile_schemas

%postun
%update_desktop_database_postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/epiphany
%attr(755,root,root) %{_bindir}/ephy-profile-migrator
%{_datadir}/appdata/epiphany.appdata.xml
%{_datadir}/dbus-1/services/org.gnome.Epiphany.service
%{_datadir}/%{name}
%{_datadir}/GConf/gsettings/epiphany.convert
%{_datadir}/glib-2.0/schemas/org.gnome.Epiphany.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.epiphany.gschema.xml
%{_datadir}/gnome-shell/search-providers/epiphany-search-provider.ini
%{_desktopdir}/epiphany.desktop
%attr(755,root,root) %{_libdir}/epiphany-search-provider
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{basever}
%dir %{_libdir}/%{name}/%{basever}/web-extensions
%attr(755,root,root) %{_libdir}/%{name}/%{basever}/web-extensions/libephywebextension.so
%{_mandir}/man1/epiphany.1*
