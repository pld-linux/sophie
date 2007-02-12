Summary:	Sophie is a daemon which uses 'libsavi' library from Sophos antivirus
Summary(pl.UTF-8):	Sophie jest demonem używającym biblioteki 'libsavi' z Sophosa
Name:		sophie
Version:	1.44
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.vanja.com/tools/sophie/%{name}-%{version}.tar.bz2
# Source0-md5:	4b8cdcd5f550a811cfceae87d2cfb0d0
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.vanja.com/tools/sophie/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(sweep)
Provides:	user(sweep)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#%define		_noautoreqdep	libsavi.so.3

%description
Sophie is a daemon which uses 'libsavi' library from Sophos anti virus
vendor <http://www.sophos.com/>.

On startup, Sophie initializes SAPI (Sophos Anti-Virus Interface),
loads virus patterns into memory, opens local UNIX domain socket, and
waits for someone to connect and instructs it which path to scan.

Since it is loaded in RAM, scanning is very fast. Of course, speed of
scanning also depends on SAVI settings and size of the file.

%description -l pl.UTF-8
Sophie jest demonem który używa biblioteki 'libsavi' udostępnionej
przez producenta oprogramowania antywirusowego Sophos (
http://www.sophos.com/ ).

Podczas uruchomienia, Sophie inicjuje SAPI (Sophos Anti-Virus
Interface), wczytuje wzorce wirusów do pamięci, otwiera lokalne
gniazdo uniksowe, i czeka na połączenie i polecenie sprawdzenia danej
ścieżki.

Jako, że Sophie cały czas jest załadowana w pamięci RAM, skanowanie
jest bardzo szybkie. Oczywiście prędkość tego skanowania zależy od
ustawień SAVI i rozmiaru sprawdzanego pliku.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-user=amavis \
	--with-group=nobody \
	--enable-net
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{rc.d/init.d,sysconfig}}

install sophie $RPM_BUILD_ROOT%{_sbindir}/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 97 sweep
%useradd -u 24 -g sweep -d /usr/share/empty -s /bin/false -c "Anti Virus Checker" sweep

%post
/sbin/chkconfig --add sophie
if [ -f /var/lock/subsys/sophie ]; then
	/etc/rc.d/init.d/sophie restart >&2
else
	echo "Run \"/etc/rc.d/init.d/sophie start\" to start Sophie daemon."
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/sophie ]; then
		/etc/rc.d/init.d/sophie stop >&2
	fi
	/sbin/chkconfig --del sophie
fi

%postun
if [ "$1" = "0" ]; then
	%userremove sweep
	%groupremove sweep
fi

%files
%defattr(644,root,root,755)
%doc README* Changes Credits
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/*
