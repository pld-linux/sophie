Summary:	Sophie is a daemon which uses 'libsavi' library from Sophos antivirus
Summary(pl):	Sophie jest demonem u�ywaj�cym biblioteki 'libsavi' z Sophosa
Name:		sophie
Version:	1.40rc1
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.vanja.com/tools/sophie/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.vanja.com/tools/sophie/
#BuildRequires:	-
#PreReq:		-
#Requires:	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libsavi.so.2

%description
Sophie is a daemon which uses 'libsavi' library from Sophos anti virus
vendor ( http://www.sophos.com/ ).

On startup, Sophie initializes SAPI (Sophos Anti-Virus Interface),
loads virus patterns into memory, opens local UNIX domain socket, and
waits for someone to connect and instructs it which path to scan.

Since it is loaded in RAM, scanning is very fast. Of course, speed of
scanning also depends on SAVI settings and size of the file.

%description -l pl
Sophie jest demonem kt�ry u�ywa biblioteki 'libsavi' udost�pnionej
przez producenta oprogramowania antywirusowego Sophos (
http://www.sophos.com/ ).

Podczas uruchomienia, Sophie inicjuje SAPI (Sophos Anti-Virus
Interface), wczytuje wzorce wirus�w do pami�ci, otwiera lokalne
gniazdo unixowe, i czeka na po��czenie i polecenie sprawdzenia danej
�cie�ki.

Jako, �e Sophie ca�y czas jest za�adowana w pami�ci RAM, skanowanie
jest bardzo szybkie. Oczywi�cie pr�dko�� tego skanowania zale�y od
ustawie� SAVI i rozmiaru sprawdzanego pliku.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-user=amavis \
	--with-group=nobody
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
if [ -n "`getgid sweep`" ]; then
	if [ "`getgid sweep`" != "97" ]; then
		echo "Error: group sweep doesn't have gid=97. Correct this before installing sophie." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 97 -r -f sweep 1>&2 || :
fi
if [ -n "`id -u sweep 2>/dev/null`" ]; then
	if [ "`id -u sweep`" != "24" ]; then
		echo "Error: user sweep doesn't have uid=24. Correct this before installing sophie." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 24 -g sweep -r -d /usr/local/sav -s /bin/false -c "Anti Virus Checker" sweep 1>&2
fi

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
	/usr/sbin/userdel sweep
	/usr/sbin/groupdel sweep
fi

%files
%defattr(644,root,root,755)
%doc README* Changes Credits
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/*
