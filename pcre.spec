Name:       pcre
%define keepstatic 1

Summary:    Perl-compatible regular expression library
Version:    8.45+git3
Release:    1
License:    BSD
URL:        http://www.pcre.org/
Source0:    %{name}-8.45.tar.gz

Patch1:     pcre-8.41-stack_frame_size_detection.patch
Patch2:     pcre-8.45-bsc1199232-unicode-property-matching.patch

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libstdc++-devel

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary:    Static libraries files for %{name}
Requires:   %{name} = %{version}-%{release}

%description static
Static development files for %{name}.

%package doc
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release}

%description doc
Man pages and documentation for %{name}.


%prep
%autosetup -p1 -n %{name}-8.45

%build
libtoolize --copy --force && autoreconf -vfi
# One contributor's name is non-UTF-8
for F in ChangeLog; do
iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
touch --reference "$F" "${F}.utf8"
mv "${F}.utf8" "$F"
done

%configure  \
%ifnarch aarch64
    --enable-jit \
%endif
    --enable-utf \
    --enable-unicode-properties \
    --enable-pcre8 \
    --enable-pcre16

%make_build

%install
%make_install

mv %{buildroot}%{_docdir}/pcre{,-%{version}}

%check
# Some setlocale calls fail with C.UTF-8
export LC_ALL=C
# RunTest test 2 needs lots of stack, if it ever segfaults
# try increasing this
ulimit -s $((16*1024))
%make_build check
export LC_ALL=

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENCE
%{_libdir}/*.so.*
%{_bindir}/pcregrep
%{_bindir}/pcretest

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_bindir}/pcre-config

%files static
%{_libdir}/*.a

%files doc
%{_mandir}/*/*.gz
%doc %{_docdir}/%{name}-%{version}
