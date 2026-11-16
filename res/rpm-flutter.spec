Name:       domacdesk
Version:    1.5.3
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     domacdesk <info@rustdesk.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/domacdesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/domacdesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/domacdesk.service -t "%{buildroot}/usr/share/domacdesk/files"
install -Dm 644 $HBB/res/domacdesk.desktop -t "%{buildroot}/usr/share/domacdesk/files"
install -Dm 644 $HBB/res/domacdesk-link.desktop -t "%{buildroot}/usr/share/domacdesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/domacdesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/domacdesk.svg"

%files
/usr/share/domacdesk/*
/usr/share/domacdesk/files/domacdesk.service
/usr/share/icons/hicolor/256x256/apps/domacdesk.png
/usr/share/icons/hicolor/scalable/apps/domacdesk.svg
/usr/share/domacdesk/files/domacdesk.desktop
/usr/share/domacdesk/files/domacdesk-link.desktop

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
ln -sf /usr/share/DisneyMjr/domacdesk /usr/bin/domacdesk
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
    rm /usr/bin/domacdesk || true
    rmdir /usr/lib/domacdesk || true
    rmdir /usr/local/domacdesk || true
    rmdir /usr/share/domacdesk || true
    rm /usr/share/applications/domacdesk.desktop || true
    rm /usr/share/applications/domacdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/domacdesk || true
    rmdir /usr/local/domacdesk || true
  ;;
esac
