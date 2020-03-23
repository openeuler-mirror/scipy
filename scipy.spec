%global py_setup_args config_fc --fcompiler=gnu95 --noarch
%bcond_without python2

Name: scipy
Version: 1.2.2
Release: 2
Summary: A Python-based ecosystem of open-source software for mathematics, science, and engineering
License: BSD, MIT, Boost and Public Domain
URL: https://www.scipy.org
Source0: https://github.com/scipy/scipy/releases/download/v%{version}/scipy-%{version}.tar.gz

BuildRequires: python3-devel python3-numpy >= 1.8.2 python3-numpy-f2py
#BuildRequires: python3-pytest
%if %{with python2}
BuildRequires: python2-devel python2-numpy >= 1.8.2 python2-numpy-f2py
#BuildRequires: python2-pytest
%endif 
BuildRequires: gcc-c++ openblas-devel gcc-gfortran
#BuildRequires: fftw-devel blas-devel lapack-devel 



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

%if %{with python2}
%package -n python2-scipy
Summary: python2 package for scipy
Requires: python2 python2-numpy

%description -n python2-scipy
python2 package for scipy
%endif


%prep
%autosetup -n %{name}-%{version} -p1 -Sgit

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
env FFLAGS="$RPM_OPT_FLAGS -fPIC"\
    OPENBLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} \
    %py3_build
popd

%if %{with python2} 
env FFLAGS="$RPM_OPT_FLAGS -fPIC"\
    OPENBLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} \
    %py2_build
%endif


%install
export CFLAGS="$RPM_OPT_FLAGS -lm"
export LDFLAGS="$RPM_LD_FLAGS -Wall -shared"

pushd %{py3dir}
env FFLAGS="$RPM_OPT_FLAGS -fPIC" \
    OPENBLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} \
    %py3_install
popd

%if %{with python2}
env FFLAGS="$RPM_OPT_FLAGS -fPIC" \
    OPENBLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} LAPACK=%{_libdir} \
    %py2_install
%endif


#%check
#pushd %{buildroot}/%{python3_sitearch}
#py.test-%{python3_version} --timeout=300 -k "not test_denormals" scipy || :
#popd

#%if %{with python2}
#pushd %{buildroot}/%{python2_sitearch}
#py.test-%{python2_version} --timeout=300 -k "not test_denormals" scipy || :
#popd
#%endif


%files -n python3-scipy
%license LICENSE.txt
%{python3_sitearch}/scipy
%{python3_sitearch}/*.egg-info


%if %{with python2}
%files -n python2-scipy
%license LICENSE.txt
%{python2_sitearch}/scipy
%{python2_sitearch}/*.egg-info
%endif

%changelog
* Mon Mar 23 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.2.2-2
- Add macros of python2

* Mon Nov 4 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.2.2-1
- Package init
