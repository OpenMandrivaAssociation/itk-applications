
%define name	itk-applications
%define version	2.0.0
%define release	%mkrel 3

Summary:	Medicine Insight Segmentation and Registration
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSDish
Group:		Sciences/Other
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.itk.org
Source0:	http://belnet.dl.sourceforge.net/sourceforge/itk/InsightApplications-%{version}.tar.bz2
BuildRequires:	cmake gcc-c++ itk-devel vtk-devel fltk-devel qt3-devel fftw3-devel
BuildRequires:	cableswig python-itk tcl-itk python-vtk tcl-vtk

%description
The following applications illustrate the use of ITK in real-world medical
imaging applications. Note these application are found in the
InsightApplications module. They differ from the Insight/Examples examples in
that they use other systems such as VTK, FLTK and Qt to create turn-key
applications. 

%package -n python-ConnectVTKITK
Group:          Development/Python
Summary:        VTK ITK python connection
Requires:	python-vtk python-itk

%description -n python-ConnectVTKITK
VTK ITK python connection

%files -n python-ConnectVTKITK
%defattr(-,root,root,0755)
%{_libdir}/InsightToolkit/python/*
%{_libdir}/InsightToolkit/*Python.so

# %package -n tcl-ConnectVTKITK
# Group:          Development/Other
# Summary:        VTK ITK tcl connection
# Requires:       tcl-vtk tcl-itk
# 
# %description -n tcl-ConnectVTKITK
# VTK ITK tcl connection
# 
# %files -n tcl-ConnectVTKITK
# %{_libdir}/InsightToolkit/tcl/*
# %{_libdir}/InsightToolkit/*Tcl.so



%prep

%setup -q -n InsightApplications-%{version}

# remove some applications
# LandmarkInitializedMutualInformationRegistration and SNAP requires valid display
# DeformableModelSimplexMesh and CellularSegmentation requires patented algorithms
mv CMakeLists.txt CMakeLists.sav
egrep -v 'LandmarkInitializedMutualInformationRegistration|SNAP|DeformableModelSimplexMesh|CellularSegmentation' CMakeLists.sav > CMakeLists.txt




# remove CVS dirs
find -name CVS -type d | xargs rm -rf

%build


cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DBUILD_SHARED_LIBS:BOOL=ON \
      -DBUILD_DOXYGEN:BOOL=ON \
      -DBUILD_TESTING:BOOL=ON \
      -DCMAKE_CXX_FLAGS:STRING="$RPM_OPT_FLAGS" \
      -DCMAKE_C_FLAGS:STRING="$RPM_OPT_FLAGS" \
      -DCMAKE_SKIP_RPATH:BOOL=ON \
      -DCMAKE_EXE_LINKER_FLAGS:STRING="-L/usr/lib/InsightToolkit -L/usr/lib/vtk/python/" \
      -DCMAKE_MODULE_LINKER_FLAGS:STRING="-L/usr/lib/InsightToolkit -L/usr/lib/vtk/python/" \
      -DCMAKE_SHARED_LINKER_FLAGS:STRING="-L/usr/lib/InsightToolkit -L/usr/lib/vtk/python/" \
      -DUSE_FLTK:BOOL=ON \
      -DUSE_VTK:BOOL=ON \
.
      
%make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# 
# make install does quite nothing
# everything needs to be done here :-(
#

# Create base dirs

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/InsightToolkit/python
# mkdir -p $RPM_BUILD_ROOT/%{_libdir}/InsightToolkit/tcl
# mkdir -p $RPM_BUILD_ROOT/%{_libdir}/vtk/python
# mkdir -p $RPM_BUILD_ROOT/%{_libdir}/vtk/tcl
# mkdir -p $RPM_BUILD_ROOT/%{_includedir}

#
# ConnectVTKITK
#

cd ConnectVTKITK/
cp *.py* $RPM_BUILD_ROOT/%{_libdir}/InsightToolkit/python
# cp pkgIndex.tcl $RPM_BUILD_ROOT/%{_libdir}/InsightToolkit/tcl
cp *Python.so $RPM_BUILD_ROOT/%{_libdir}/InsightToolkit


%clean
rm -rf $RPM_BUILD_ROOT


