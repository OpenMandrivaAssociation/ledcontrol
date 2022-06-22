Summary:	Tool to control LEDs over D-Bus
Name:		ledcontrol
Version:	0.0.1
Release:	2
Group:		System
Source0:	https://github.com/OpenMandrivaSoftware/ledcontrol/archive/%{version}/%{name}-%{version}.tar.gz
License:	GPLv3
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5DBus)
BuildRequires:	cmake
BuildRequires:	ninja
# Only for CMake's checks
BuildRequires:	qmake5

%description
A tool that allows users to control LEDs over D-Bus. It is primarily
meant for use in Plasma Mobile.

%prep
%autosetup -p1
%cmake -G Ninja

%build
%ninja_build -C build
%ninja_build -C build dbus

%install
%ninja_install -C build
mkdir -p %{buildroot}/lib/systemd/system
cat >%{buildroot}/lib/systemd/system/ledcontrol.service <<'EOF'
[Unit]
Description=LED control interface
Wants=dbus.socket
After=dbus.socket

[Service]
BusName=ch.lindev.LEDControl
CapabilityBoundingSet=
IPAddressDeny=any
LockPersonality=yes
NoNewPrivileges=yes
ProtectClock=yes
ProtectControlGroups=yes
ProtectHome=yes
ProtectHostname=yes
ExecStart=%{_bindir}/ledcontrol

[Install]
WantedBy=multi-user.target
Alias=dbus-ch.lindev.LEDControl.service
EOF

%files
%{_bindir}/ledcontrol
%{_sysconfdir}/dbus-1/system.d/ch.lindev.LEDControl.conf
%{_datadir}/dbus-1/interfaces/ch.lindev.LEDControl.xml
/lib/systemd/system/ledcontrol.service
