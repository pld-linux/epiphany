# Conditinal build:
%bcond_with	mozilla_firefox	# build with mozilla-firefox-devel
#
Summary:	Epiphany - gecko-based GNOME web browser
Summary(es):	Epiphany - navigador Web de GNOME basado en gecko
Summary(pl):	Epiphany - przeglądarka WWW dla GNOME
Name:		epiphany
Version:	1.9.6
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/epiphany/1.9/%{name}-%{version}.tar.bz2
# Source0-md5:	097278ad79deaa017b8c026b5c8a383f
Patch0:		%{name}-first-tab.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-mozilla_includes.patch
Patch3:		%{name}-pld-homepage.patch
Patch4:		%{name}-configure.patch
Patch5:		%{name}-m4.patch
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	ORBit2-devel >= 1:2.12.1
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.8
BuildRequires:	dbus-glib-devel >= 0.34
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-desktop-devel >= 2.10.0-2
BuildRequires:	gnome-doc-utils >= 0.3.2-1
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.8.3
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	intltool >= 0.33
BuildRequires:	iso-codes >= 0.35
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeprintui-devel >= 2.11.0-3
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	startup-notification-devel >= 0.5
BuildRequires:	libtool
BuildRequires:	libxslt-devel >= 1.1.15
%if %{with mozilla_firefox}
BuildRequires:	mozilla-firefox-devel >= 1.0.5
%else
BuildRequires:	mozilla-devel >= 5:1.7.9
%endif
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-devel >= 2.6.0
BuildRequires:	python-pygtk-devel >= 2.6.0
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	dbus >= 0.34
Requires:	gnome-icon-theme >= 2.10.0
Requires:	gtk+2 >= 2:2.8.3
%if %{with mozilla_firefox}
%requires_eq	mozilla-firefox
%else
Requires:	mozilla-embedded = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
%endif
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
Requires:	gtk+2-devel >= 2:2.8.3
Requires:	libxslt-devel >= 1.1.15

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
%patch4 -p1
%patch5 -p1

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
# CFLAGS is a hack for gcc 3.3
%{__make} \
	CFLAGS="%{rpmcflags} -fno-strict-aliasing"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/1.9/extensions

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no
rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/1.9/plugins/*.la

# epiphany-2.0.mo, but gnome/help/epiphany
%find_lang %{name}-2.0 --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install epiphany-fonts.schemas
%gconf_schema_install epiphany-lockdown.schemas
%gconf_schema_install epiphany.schemas
%scrollkeeper_update_post
%update_desktop_database_post

%preun
%gconf_schema_uninstall epiphany-fonts.schemas
%gconf_schema_uninstall epiphany-lockdown.schemas
%gconf_schema_uninstall epiphany.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun

%files -f %{name}-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{name}
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/epiphany-fonts.schemas
%{_sysconfdir}/gconf/schemas/epiphany-lockdown.schemas
%{_sysconfdir}/gconf/schemas/epiphany.schemas
%{_omf_dest_dir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/1.9
%dir %{_libdir}/%{name}/1.9/extensions
%dir %{_libdir}/%{name}/1.9/plugins
%attr(755,root,root) %{_libdir}/epiphany/1.9/plugins/*.so*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_aclocaldir}/*
%{_includedir}/epiphany
%{_pkgconfigdir}/*.pc
%{_datadir}/pygtk/*/defs/epiphany.defs
%{_gtkdocdir}/*
