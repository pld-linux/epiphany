
%define		minmozver	1.4

Summary:	Epiphany - gecko-based GNOME web browser
Summary(pl):	Epiphany - przegl±darka WWW dla GNOME
Name:		epiphany
Version:	0.8.0
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	b75c4d7eae8c08eb7d817138e5867b73
Patch0:		%{name}-MOZILLA_FIVE_HOME.patch
URL:		http://epiphany.mozdev.org/
BuildRequires:	GConf2-devel
BuildRequires:	ORBit2-devel >= 2.7.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libbonobo-devel >= 2.3.5
BuildRequires:	gnome-common >= 2.3.0
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gtk+2-devel >= 2.0.6
BuildRequires:	intltool
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libxml2-devel
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	nautilus-devel >= 2.0.0
BuildRequires:	scrollkeeper
BuildRequires:	rpm-build >= 4.1-10
Requires(post):	GConf2
Requires(post):	scrollkeeper
Requires:	mozilla-embedded = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%description
Gnome browser based on Gecko (Mozilla rendering engine).

%description -l pl
Epiphany jest przegl±dark± WWW bazuj±c± na Gecko (mechanizmie
interpretacji stron Mozilli).

%package devel
Summary:	Epiphany header files
Summary(pl):	Pliki nag³ówkowe Epiphany
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}

%description devel
Epiphany header files for plugin development.

%description devel -l pl
Pliki nag³ówkowe Epiphany do tworzenia wtyczek.


%prep
%setup -q
%patch0 -p1

%build
rm -f acconfig.h
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoheader}
%{__automake}
%{__autoconf}

# rebuild for new ORBit2
cd idl
orbit-idl-2 -I/usr/share/idl -I/usr/share/idl/bonobo-2.0 \
	-I/usr/share/idl/bonobo-activation-2.0 EphyAutomation.idl
mv -f *.h *.c ../src
cd ..

%configure \
	--disable-schemas-install \
	--enable-nautilus-view=yes \
	--with-mozilla-snapshot=1.4

# CFLAGS is a hack for gcc 3.3
%{__make} CFLAGS="%{rpmcflags} -fno-strict-aliasing"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# epiphany-2.0.mo, but gnome/help/epiphany
%find_lang %{name}-2.0 --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install
/usr/bin/scrollkeeper-update

%files -f %{name}-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_datadir}/%{name}
%{_desktopdir}/*
%{_datadir}/application-registry/*
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/*
%{_omf_dest_dir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/epiphany-1.0
