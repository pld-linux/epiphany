
%define		minmozver	1.5b

Summary:	Epiphany - gecko-based GNOME web browser
Summary(pl):	Epiphany - przegl±darka WWW dla GNOME
Name:		epiphany
Version:	1.0
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/1.0/%{name}-%{version}.tar.bz2
# Source0-md5:	d7f02d1c9d4f0bc8086ff329ab9b4743
#Source0:	http://downloads.uk1.mozdev.org/rsync/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-MOZILLA_FIVE_HOME.patch
URL:		http://epiphany.mozdev.org/
BuildRequires:	GConf2-devel
BuildRequires:	ORBit2-devel >= 2.7.5-1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common >= 2.3.0
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gtk+2-devel >= 2.0.6
BuildRequires:	intltool
BuildRequires:	libbonobo-devel >= 2.3.5
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel >= 2.3.3.1-2
BuildRequires:	libxml2-devel
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	nautilus-devel >= 2.3.8
BuildRequires:	scrollkeeper
BuildRequires:	rpm-build >= 4.1-10
Requires(post):	GConf2
Requires(post):	scrollkeeper
Requires:	mozilla-embedded = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%description
GNOME browser based on Gecko (Mozilla rendering engine).

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
	--with-mozilla-snapshot=1.5b

# CFLAGS is a hack for gcc 3.3
%{__make} \
	CFLAGS="%{rpmcflags} -fno-strict-aliasing"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# epiphany-2.0.mo, but gnome/help/epiphany
%find_lang %{name}-2.0 --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install
/usr/bin/scrollkeeper-update

%postun -p /usr/bin/scrollkeeper-update

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
%{_libdir}/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/epiphany-1.0
%{_pkgconfigdir}/*.pc
