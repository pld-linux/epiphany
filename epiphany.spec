%define		basever		2.18
Summary:	Epiphany - gecko-based GNOME web browser
Summary(es.UTF-8):	Epiphany - navigador Web de GNOME basado en gecko
Summary(pl.UTF-8):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	2.18.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/epiphany/2.18/%{name}-%{version}.tar.bz2
# Source0-md5:	d9a82160bafa4e80091681b19a70ba79
Patch0:		%{name}-first-tab.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-pld-homepage.patch
Patch3:		%{name}-configure.patch
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	GConf2-devel >= 2.18.0.1
BuildRequires:	ORBit2-devel >= 1:2.14.7
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	gnome-common >= 2.18.0
BuildRequires:	gnome-desktop-devel >= 2.18.0
BuildRequires:	gnome-doc-utils >= 0.10.1
BuildRequires:	gnome-vfs2-devel >= 2.18.0.1
BuildRequires:	gtk+2-devel >= 2:2.10.10
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	intltool >= 0.35.5
BuildRequires:	iso-codes >= 0.53
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeprintui-devel >= 2.18.0
BuildRequires:	libgnomeui-devel >= 2.18.1
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.28
BuildRequires:	libxslt-devel >= 1.1.20
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-devel >= 2.18.0
BuildRequires:	python-pygtk-devel >= 2:2.10.4
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xulrunner
BuildRequires:	xulrunner-devel >= 1.8.0.4
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	dbus >= 1.0.2
Requires:	gnome-icon-theme >= 2.18.0
Requires:	libgnomeui >= 2.18.1
%requires_eq	xulrunner
Obsoletes:	python-epiphany
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so
# we have strict deps for it
%define		_noautoreq	libxpcom.so

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
Requires:	gtk+2-devel >= 2:2.10.10
Requires:	libxslt-devel >= 1.1.20

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
%patch2 -p1
%patch3 -p1

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
	--enable-gtk-doc \
	--enable-python \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/%{basever}/extensions

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/%{basever}/plugins/*.la

%find_lang %{name} --with-gnome

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

%preun
%gconf_schema_uninstall epiphany-fonts.schemas
%gconf_schema_uninstall epiphany-lockdown.schemas
%gconf_schema_uninstall epiphany-pango.schemas
%gconf_schema_uninstall epiphany.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_sysconfdir}/gconf/schemas/epiphany-fonts.schemas
%{_sysconfdir}/gconf/schemas/epiphany-lockdown.schemas
%{_sysconfdir}/gconf/schemas/epiphany-pango.schemas
%{_sysconfdir}/gconf/schemas/epiphany.schemas
%{_omf_dest_dir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{basever}
%dir %{_libdir}/%{name}/%{basever}/extensions
%dir %{_libdir}/%{name}/%{basever}/plugins
%attr(755,root,root) %{_libdir}/epiphany/%{basever}/plugins/*.so*
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
