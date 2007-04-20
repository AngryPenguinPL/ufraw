%define	name		ufraw
%define	version		0.11
%define	release		%mkrel 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Graphical tool to convert raw images of digital cameras
Group:		Graphics
URL:		http://ufraw.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/ufraw/%{name}-%{version}.tar.bz2
License:	GPL
BuildRequires:	libgimp-devel >= 2.0 gtk+2-devel libjpeg-devel
BuildRequires:	libtiff-devel zlib-devel liblcms-devel ImageMagick
# we use libexiv instead of libexif
#BuildRequires:	libexif-devel
BuildRequires:	libexiv-devel
BuildRequires:  desktop-file-utils
Buildroot:	%_tmppath/%name-%version-%release-root

%description

UFRaw is a utility to read and manipulate raw images from digital cameras.
It can be used by itself or as a Gimp plug-in.
It reads raw images using Dave Coffin's raw conversion utility DCRaw.
And it supports basic color management using Little CMS, allowing
the user to apply color profiles.

Ufraw was originally based on the gimp plug-in by Dave Coffin
http://www.cybercom.net/~dcoffin/
and on Pawel T. Jochym's (jochym at ifj edu pl) plug-in.

Raw images are the data directly read from the CCD of the camera,
without in-camera processing, without lossy JPEG compression, and in
36 or 48 bits color depth (TIFF has 24 bits). Problem of the raw
images is that they are in proprietary, camera-specific formats as
they are exactly what the CCD has captured, and the CCDs on differnt
cameras are very different. It also contains info about the camera
settings.

%package gimp
Summary: 	Reads the raw image formats of digital cameras into GIMP
Group: 		Graphics
Requires: 	gimp
Conflicts:	dcraw-gimp2.0 rawphoto
 
%description gimp

A GIMP plug-in which reads and processes raw images from most digital
cameras. The conversion is done by the dcraw software and so all
cameras supported by dcraw are also supported by this plug-in.

In contrary to the original GIMP plug-in of dcraw this one is much
more comfortable, especially because of the life preview image but
also due to more options.

%prep
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%setup -q 

%build
%configure2_5x --with-exiv2  --enable-mime
%make

%install

rm -fr %buildroot

%makeinstall_std schemasdir=%{_sysconfdir}/gconf/schemas

#don't package mime file, shared-mime-info is ok now
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime

%find_lang ufraw

# Install menu stuff
install -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{name}" \
icon="%{name}.png" \
section="Multimedia/Graphics" \
title="UFRaw" \
longtitle="Graphical tool to convert RAW images from digital cameras" \
xdg=true \
needs="x11"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Graphics" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


install -d %buildroot%{_datadir}/icons/{large,mini}

convert icons/ufraw.png -resize 32x32 %buildroot%{_iconsdir}/%{name}.png
convert icons/ufraw.png -resize 16x16 %buildroot%{_miconsdir}/%{name}.png
cp icons/ufraw.png %buildroot%{_liconsdir}/%{name}.png

%clean
rm -fr %buildroot

%define schemas ufraw

# Update menus
%post
%post_install_gconf_schemas %schemas
%update_desktop_database
%update_menus

%preun
%preun_uninstall_gconf_schemas %schemas

%postun
%clean_menus
%clean_desktop_database

%files -f %{name}.lang
%defattr(-,root,root)
%docdir %{_docdir}/%{name}-%{version}
%doc README
%_sysconfdir/gconf/schemas/ufraw.schemas
%_bindir/*
%_menudir/*
%_datadir/applications/ufraw.desktop
%_datadir/pixmaps/*.png
%_iconsdir/*.png
%_liconsdir/*.png
%_miconsdir/*.png
%_mandir/man1/*

%files gimp
%defattr(-,root,root)
%{_libdir}/gimp/2.0/plug-ins/*


