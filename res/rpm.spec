Name:       domacdesk
Version:    1.5.3
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     domacdesk <info@rustdesk.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/domacdesk/
mkdir -p %{buildroot}/usr/share/domacdesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/domacdesk %{buildroot}/usr/bin/domacdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/domacdesk/libsciter-gtk.so
install $HBB/res/domacdesk.service %{buildroot}/usr/share/domacdesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/domacdesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/domacdesk.svg
install $HBB/res/domacdesk.desktop %{buildroot}/usr/share/domacdesk/files/
install $HBB/res/domacdesk-link.desktop %{buildroot}/usr/share/domacdesk/files/

%files
/usr/bin/domacdesk
/usr/share/domacdesk/libsciter-gtk.so
/usr/share/domacdesk/files/domacdesk.service
/usr/share/icons/hicolor/256x256/apps/domacdesk.png
/usr/share/icons/hicolor/scalable/apps/domacdesk.svg
/usr/share/domacdesk/files/domacdesk.desktop
/usr/share/domacdesk/files/domacdesk-link.desktop
/usr/share/domacdesk/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop domacdesk || true
  ;;
esac

%post
cp /usr/share/domacdesk/files/domacdesk.service /etc/systemd/system/domacdesk.service
cp /usr/share/domacdesk/files/domacdesk.desktop /usr/share/applications/
cp /usr/share/domacdesk/files/domacdesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable domacdesk
systemctl start domacdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop domacdesk || true
    systemctl disable domacdesk || true
    rm /etc/systemd/system/domacdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/domacdesk.desktop || true
    rm /usr/share/applications/domacdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
