%define		basever	2.15
Summary:	Epiphany - gecko-based GNOME web browser
Summary(es):	Epiphany - navigador Web de GNOME basado en gecko
Summary(pl):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	2.15.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/epiphany/%{basever}/%{name}-%{version}.tar.bz2
# Source0-md5:	eb9826f106b29168a8154dbf4aaaf718
Patch0:		%{name}-first-tab.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-pld-homepage.patch
Patch3:		%{name}-configure.patch
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	ORBit2-devel >= 1:2.14.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.8
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-desktop-devel >= 2.15.2
BuildRequires:	gnome-doc-utils >= 0.6.0
BuildRequires:	gnome-vfs2-devel >= 2.15.1
BuildRequires:	gtk+2-devel >= 2:2.9.2
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	intltool >= 0.35
BuildRequires:	iso-codes >= 0.35
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeprintui-devel >= 2.12.0
BuildRequires:	libgnomeui-devel >= 2.15.1
BuildRequires:	startup-notification-devel >= 0.5
BuildRequires:	libtool
BuildRequires:	libxslt-devel >= 1.1.17
BuildRequires:	mozilla-firefox-devel >= 1.0.5
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-devel >= 2.15.1
BuildRequires:	python-pygtk-devel >= 2.9.0
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	dbus >= 0.60
Requires:	gnome-icon-theme >= 2.15.2
Requires:	gtk+2 >= 2:2.9.2
Requires:	libgnomeui >= 2.15.1
%requires_eq	mozilla-firefox
Obsoletes:	python-epiphany
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%description
GNOME browser based on Gecko (Mozilla rendering engine).

%description -l es
Navigador Web de GNOME basado en Gecko (el engine plasmante de Mozilla).

%description -l pl
Epiphany jest przeglądarką WWW bazującą na Gecko (mechanizmie
interpretacji stron Mozilli).

%package devel
Summary:	Epiphany header files
Summary(es):	Ficheros de cabecera de Epiphany
Summary(pl):	Pliki nagłówkowe Epiphany
Group:		X11/Applications/Networking
# doesn't require base
Requires:	gtk+2-devel >= 2:2.9.2
Requires:	libxslt-devel >= 1.1.17

%description devel
Epiphany header files for plugin development.

%description devel -l es
Ficheros de cabecera de Epiphany para desarrollar plug-ins.

%description devel -l pl
Pliki nagłówkowe Epiphany do tworzenia wtyczek.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
gnome-doc-prepare --copy --force
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

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/tk
rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/%{basever}/plugins/*.la

# epiphany-2.0.mo, but gnome/help/epiphany
%find_lang %{name}-2.0 --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install epiphany-fonts.schemas
%gconf_schema_install epiphany-lockdown.schemas
%gconf_schema_install epiphany-pango.schemas
%gconf_schema_install epiphany.schemas
%scrollkeeper_update_post
%update_desktop_database_post
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%preun
%gconf_schema_uninstall epiphany-fonts.schemas
%gconf_schema_uninstall epiphany-lockdown.schemas
%gconf_schema_uninstall epiphany-pango.schemas
%gconf_schema_uninstall epiphany.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%files -f %{name}-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{name}
%{_desktopdir}/*
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
%{_gtkdocdir}/*
