
%define		minmozver	1.4a
%define		snap		20030315

Summary:	Epiphany - gecko-based GNOME web browser
Summary(pl):	Epiphany - przegl±darka WWW dla GNOME
Name:		epiphany
Version:	0.5.0
Release:	2
License:	GPL
Group:		X11/Applications/Networking
#Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source0:	http://downloads.mozdev.org/epiphany/%{name}-%{version}.tar.gz
Patch0:		%{name}-ac.patch
URL:		http://epiphany.mozdev.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	GConf2-devel
BuildRequires:	ORBit2-devel
BuildRequires:	bonobo-activation-devel >= 2.1.0
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
Requires:	mozilla-embedded = %(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded)
Requires(post):	GConf2
Requires(post):	mozilla
Requires(post):	scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%description
Gnome browser based on Gecko (Mozilla rendering engine).

%description -l pl
Epiphany jest przegl±dark± WWW bazuj±c± na Gecko (mechanizmie
interpretacji stron Mozilli).

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

%configure \
	--disable-schemas-install \
	--enable-nautilus-view=yes

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}-2.0

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
%{_datadir}/applications/*
%{_datadir}/gnome/help/*
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/*
%{_omf_dest_dir}/*
