%define		minmozver	5:1.7
Summary:	Epiphany - gecko-based GNOME web browser
Summary(es):	Epiphany - navigador Web de GNOME basado en gecko
Summary(pl):	Epiphany - przegl±darka WWW dla GNOME
Name:		epiphany
Version:	1.6.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/epiphany/1.6/%{name}-%{version}.tar.bz2
# Source0-md5:	945545f33714736154725ed2a3b8c8b8
Patch0:		%{name}-first-tab.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-mozilla_includes.patch
Patch3:		%{name}-mozilla.patch
URL:		http://www.gnome.org/projects/epiphany/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	ORBit2-devel >= 1:2.12.1
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-desktop >= 2.10.0-2
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.6.4
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	intltool >= 0.33
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.19
BuildRequires:	mozilla-devel >= %{minmozver}
BuildRequires:	nautilus-devel >= 2.10.0-3
BuildRequires:	pango-devel >= 1:1.8.1
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.196
BuildRequires:	scrollkeeper
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	gnome-icon-theme >= 2.10.0
Requires:	gtk+2 >= 2:2.6.4
Requires:	mozilla-embedded = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%description
GNOME browser based on Gecko (Mozilla rendering engine).

%description -l es
Navigador Web de GNOME basado en Gecko (el engine plasmante de Mozilla).

%description -l pl
Epiphany jest przegl±dark± WWW bazuj±c± na Gecko (mechanizmie
interpretacji stron Mozilli).

%package devel
Summary:	Epiphany header files
Summary(es):	Ficheros de cabecera de Epiphany
Summary(pl):	Pliki nag³ówkowe Epiphany
Group:		X11/Applications/Networking
# doesn't require base
Requires:	gtk+2-devel >= 2:2.6.4
Requires:	libxml2-devel >= 2.6.19

%description devel
Epiphany header files for plugin development.

%description devel -l es
Ficheros de cabecera de Epiphany para desarrollar plug-ins.

%description devel -l pl
Pliki nag³ówkowe Epiphany do tworzenia wtyczek.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm -f acconfig.h
cp /usr/share/automake/mkinstalldirs .
glib-gettextize --copy --force
intltoolize --copy --force
gnome-doc-common --copy
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}

%configure \
	--disable-schemas-install \
	--enable-nautilus-view=yes \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
# CFLAGS is a hack for gcc 3.3
%{__make} \
	CFLAGS="%{rpmcflags} -fno-strict-aliasing"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}-1.6/extensions

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no
rm -r $RPM_BUILD_ROOT%{_datadir}/application-registry/*

# epiphany-2.0.mo, but gnome/help/epiphany
%find_lang %{name}-2.0 --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
%gconf_schema_install /etc/gconf/schemas/epiphany-lockdown.schemas
%gconf_schema_install /etc/gconf/schemas/epiphany.schemas
/usr/bin/scrollkeeper-update -q
/usr/bin/update-desktop-database

%preun
if [ $1 = 0 ]; then
	%gconf_schema_uninstall /etc/gconf/schemas/epiphany-lockdown.schemas
	%gconf_schema_uninstall /etc/gconf/schemas/epiphany.schemas
fi

%postun
if [ $1 = 0 ]; then
	umask 022
	/usr/bin/scrollkeeper-update -q
	/usr/bin/update-desktop-database
fi

%files -f %{name}-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_datadir}/%{name}
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/*
%{_omf_dest_dir}/*
%dir %{_libdir}/%{name}-1.6
%dir %{_libdir}/%{name}-1.6/extensions
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/epiphany-1.6
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/*
