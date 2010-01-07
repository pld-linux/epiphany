#
#Conditional build:
%bcond_with	webkit		# Build with experimental webkit support instead of xulrunner
#
%define		basever		2.26
Summary:	Epiphany - gecko-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en gecko
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	2.26.3
Release:	7
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/GNOME/sources/epiphany/2.26/%{name}-%{version}.tar.bz2
# Source0-md5:	16f44012bc376077e1443e049d725847
Patch0:		%{name}-pld-homepage.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-ti-agent.patch
Patch3:		%{name}-agent.patch
Patch4:		%{name}-lt.patch
Patch5:		%{name}-libxul.patch
Patch7:		%{name}-build_date.patch
Patch8:		%{name}-xulrunner-plugins-dir.patch
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	GConf2-devel >= 2.26.0
BuildRequires:	NetworkManager-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	avahi-gobject-devel >= 0.6
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	enchant-devel >= 1.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gnome-desktop-devel >= 2.26.0
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gtk+2-devel >= 2:2.16.0
BuildRequires:	gtk-doc >= 1.8
%if %{with webkit}
BuildRequires:	gtk-webkit-devel
BuildRequires:	libssh2-devel
%endif
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes >= 0.53
BuildRequires:	libcanberra-gtk-devel >= 0.3
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnomeui-devel >= 2.24.0
BuildRequires:	libnotify-devel >= 0.4
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	libxslt-devel >= 1.1.20
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-devel >= 2.20.0
BuildRequires:	python-pygtk-devel >= 2:2.12.0
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.364
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.8
%if %{without webkit}
BuildRequires:	xulrunner
BuildRequires:	xulrunner-devel >= 1.9.0.1-1
%endif
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	dbus >= 1.0.2
Requires:	gnome-icon-theme >= 2.26.0
Requires:	libgnomeui >= 2.24.0
Provides:	wwwbrowser
%if %{without webkit}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
%requires_eq	xulrunner
%endif
Obsoletes:	python-epiphany
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without webkit}
# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so
# we have strict deps for it
%define		_noautoreq	libxpcom.so
%endif

%description
GNOME browser based on Gecko (Mozilla rendering engine).

%description -l es.UTF-8
Navigador Web de GNOME basado en Gecko (el engine plasmante de
Mozilla).

%description -l pl.UTF-8
Epiphany jest przeglądarką WWW bazującą na Gecko (mechanizmie
interpretacji stron Mozilli).

%package devel
Summary:	Epiphany header files
Summary(es.UTF-8):	Ficheros de cabecera de Epiphany
Summary(pl.UTF-8):	Pliki nagłówkowe Epiphany
Group:		X11/Applications/Networking
# doesn't require base
Requires:	gtk+2-devel >= 2:2.16.0
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
%patch1 -p1
%if "%{pld_release}" == "ti"
%patch2 -p1
%else
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch7 -p1
%patch8 -p1

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
	--disable-schemas-install \
	--enable-dbus \
	%{!?with_webkit:--enable-gtk-doc} \
	--enable-network-manager \
	--enable-python \
%if %{with webkit}
	--with-engine=webkit \
%else
	--with-gecko=libxul-embedding \
%endif
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/%{basever}/extensions

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/%{basever}/plugins

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/%{basever}/plugins/*.la
rm -rf $RPM_BUILD_ROOT%{_iconsdir}/LowContrastLargePrint

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install epiphany-fonts.schemas
%gconf_schema_install epiphany-lockdown.schemas
%gconf_schema_install epiphany-pango.schemas
%gconf_schema_install epiphany.schemas
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor
%if %{without webkit}
%update_browser_plugins
%endif

%preun
%gconf_schema_uninstall epiphany-fonts.schemas
%gconf_schema_uninstall epiphany-lockdown.schemas
%gconf_schema_uninstall epiphany-pango.schemas
%gconf_schema_uninstall epiphany.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor
%if %{without webkit}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi
%endif

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README

%if %{without webkit}
# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist
%endif

%attr(755,root,root) %{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/*/*/apps/*.*
%{_sysconfdir}/gconf/schemas/epiphany-fonts.schemas
%{_sysconfdir}/gconf/schemas/epiphany-lockdown.schemas
%{_sysconfdir}/gconf/schemas/epiphany-pango.schemas
%{_sysconfdir}/gconf/schemas/epiphany.schemas
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{basever}
%dir %{_libdir}/%{name}/%{basever}/extensions
%if %{without webkit}
%dir %{_libdir}/%{name}/%{basever}/plugins
%attr(755,root,root) %{_libdir}/epiphany/%{basever}/plugins/*.so*
%endif
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_aclocaldir}/*
%{_includedir}/epiphany
%{_pkgconfigdir}/*.pc
%{_datadir}/pygtk/*/defs/epiphany.defs

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
