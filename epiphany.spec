
%define		minmozver	5:1.6
%define		snap            20031203

Summary:	Epiphany - gecko-based GNOME web browser
Summary(pl):	Epiphany - przegl±darka WWW dla GNOME
Name:		epiphany
Version:	1.1.9
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/1.1/%{name}-%{version}.tar.bz2
# Source0-md5:	acd82b331790ffb25752e7e7184eab41
#Source0:	%{name}-%{version}.%{snap}.tar.bz2
#Source0:	http://downloads.uk1.mozdev.org/rsync/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-MOZILLA_FIVE_HOME.patch
#Patch1:		%{name}-tabsmenu.patch
Patch2:		%{name}-first-tab.patch
Patch3:		%{name}-schemas.patch
Patch4:		%{name}-locale-names.patch
URL:		http://epiphany.mozdev.org/
BuildRequires:	GConf2-devel
BuildRequires:	ORBit2-devel >= 1:2.9.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common >= 2.4.0
BuildRequires:	gnome-vfs2-devel >= 2.5.6
BuildRequires:	gtk+2-devel >= 1:2.3.2
BuildRequires:	intltool >= 0.29
BuildRequires:	libbonoboui-devel >= 2.5.1
BuildRequires:	libglade2-devel >= 1:2.3.1
BuildRequires:	libgnomeui-devel >= 2.5.3
BuildRequires:	libxml2-devel >=  2.6.6
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	nautilus-devel >= 2.5.6
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper
Requires(post):	GConf2
Requires(post):	scrollkeeper
Requires:	mozilla-embedded = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
# epiphany uses new widgets not present in older version
Requires:	gtk+2 >= 1:2.3.2
Requires:	gnome-icon-theme >= 1.1.6-2
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
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel >= 2.3.2
Requires:	libxml2-devel >= 2.6.6

%description devel
Epiphany header files for plugin development.

%description devel -l pl
Pliki nag³ówkowe Epiphany do tworzenia wtyczek.

%prep
%setup -q
%patch0 -p1
#%%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

mv po/{no,nb}.po

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
#cd idl
#orbit-idl-2 -I/usr/share/idl -I/usr/share/idl/bonobo-2.0 \
#	-I/usr/share/idl/bonobo-activation-2.0 EphyAutomation.idl
#mv -f *.h *.c ../src
#cd ..

%configure \
	--disable-schemas-install \
	--enable-nautilus-view=yes \
	--with-mozilla-snapshot=1.6 \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

# CFLAGS is a hack for gcc 3.3
%{__make} \
	CFLAGS="%{rpmcflags} -fno-strict-aliasing"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

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
%{_includedir}/epiphany-1.1
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/*
