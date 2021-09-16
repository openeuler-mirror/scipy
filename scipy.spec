%global py_setup_args config_fc --fcompiler=gnu95 --noarch
%global debug_package %{nil}
Name: scipy
Version: 1.2.2
Release: 8
Summary: A Python-based ecosystem of open-source software for mathematics, science, and engineering
License: Qhull and Apache-2.0
URL: https://www.scipy.org
Source0: https://github.com/scipy/scipy/releases/download/v%{version}/scipy-%{version}.tar.gz

BuildRequires: python3-devel python3-numpy >= 1.8.2 python3-numpy-f2py
BuildRequires: gcc-c++ openblas-devel gcc-gfortran chrpath

%description
SciPy (pronounced "Sigh Pie") is open-source software for mathematics, science, and engineering. 
It includes modules for statistics, optimization, integration, linear algebra, Fourier transforms, 
signal and image processing, ODE solvers, and more.

SciPy depends on NumPy, which provides convenient and fast N-dimensional array manipulation. 
SciPy is built to work with NumPy arrays, and provides many user-friendly and efficient numerical routines 
such as routines for numerical integration and optimization. 
Together, they run on all popular operating systems, are quick to install, and are free of charge. 
NumPy and SciPy are easy to use, but powerful enough to be depended upon by some of the world's leading scientists and engineers. 
If you need to manipulate numbers on a computer and display or publish the results, give SciPy a try!

%package -n python3-scipy
Summary: python3 package for scipy
Requires: python3 python3-numpy

%description -n python3-scipy
python3 package for scipy

%prep
%autosetup -n %{name}-%{version} -p1

cat > site.cfg << EOF
[amd]
library_dirs = %{_libdir}
include_dirs = /usr/include/suitesparse
amd_libs = amd
 
[umfpack]
library_dirs = %{_libdir}
include_dirs = /usr/include/suitesparse
umfpack_libs = umfpack

[openblas]
library_dirs = %{_libdir}
openblas_libs = openblasp
EOF

rm -rf %{py3dir}
cp -a . %{py3dir}


%build
export CFLAGS="$RPM_OPT_FLAGS -lm"
export LDFLAGS="$RPM_LD_FLAGS -Wall -shared"
pushd %{py3dir}
env FFLAGS="$RPM_OPT_FLAGS -fPIC -w -fallow-argument-mismatch -O2"\
    OPENBLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} \
    %py3_build
popd

%install
export CFLAGS="$RPM_OPT_FLAGS -lm"
export LDFLAGS="$RPM_LD_FLAGS -Wall -shared"

pushd %{py3dir}
env FFLAGS="$RPM_OPT_FLAGS -fPIC" \
    OPENBLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} \
    %py3_install
popd

find %{buildroot} -type f -name '*.so' -exec strip '{}' ';'

cd  $RPM_BUILD_ROOT/usr
file `find -type f`| grep -w ELF | awk -F":" '{print $1}' | for i in `xargs`
do
  chrpath -d $i
done
cd -
mkdir -p  $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_bindir}/%{name}" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf
echo "%{_libdir}/%{name}" >> $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -n python3-scipy
%license LICENSE.txt
%{python3_sitearch}/scipy
%{python3_sitearch}/*.egg-info
%config(noreplace) /etc/ld.so.conf.d/*

%changelog
* Thu Sep 16 2021 chenchen <chen_aka_jan@163.com> - 1.2.2-8
- del rpath for some binaries and bin

* Sat Sep 4 2021 zhangtao <zhangtao221@huawei.com> - 1.2.2-7
- Strip Dynamic library

* Mon Aug 02 2021 chenyanpanHW <chenyanpan@huawei.com> - 1.2.2-6
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Sun Aug 01 2021 sunguoshuai <sunguoshuai@huawei.com> - 1.2.2-5
- Fix build error with gcc 10

* Mon May 31 2021 huanghaitao <huanghaitao8@huawei.com> - 1.2.2-4
- Completing build dependencies to fix git commands missing error

* Tue Oct 27 2020 huanghaitao <huanghaitao8@openeuler.org> - 1.2.2-3
- Disable python2 module

* Mon Mar 23 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.2.2-2
- Add macros of python2

* Mon Nov 4 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.2.2-1
- Package init
