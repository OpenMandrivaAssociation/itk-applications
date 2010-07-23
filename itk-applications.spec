%define		name		itk-applications
%define		version		3.20.0
%define		release		%mkrel 1

%define		itkver		3.20

Summary:	Medicine Insight Segmentation and Registration
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSDish
Group:		Sciences/Other
URL:		http://www.itk.org
Source0:	http://belnet.dl.sourceforge.net/sourceforge/itk/InsightApplications-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	itk-devel
BuildRequires:	vtk-devel
BuildRequires:	fltk-devel
BuildRequires:	qt4-devel
BuildRequires:	fftw3-devel
BuildRequires:	cableswig
BuildRequires:	python-itk
BuildRequires:	python-vtk-devel
BuildRequires:	tcl-itk
BuildRequires:	tcl-vtk-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

# FIXME the last portion of the patch is ugly, i.e. s/libitkfoo/libitkfooD/
Patch0:		InsightApplications-3.16.0-build.patch

%description
The following applications illustrate the use of ITK in real-world medical
imaging applications. Note these application are found in the
InsightApplications module. They differ from the Insight/Examples examples in
that they use other systems such as VTK, FLTK and Qt to create turn-key
applications. 

%files
%defattr(0644,root,root,0755)
%{_bindir}/*
%{_libdir}/*

#------------------------------------------------------------------------
%package	devel
Group:		Development/Other
Summary:	itk applications development files

%description	devel
itk applications development files

%files		devel
%defattr(0644,root,root,0755)
%{_includedir}*

#------------------------------------------------------------------------
%prep
%setup -q -n InsightApplications-%{version}

# remove some applications
# LandmarkInitializedMutualInformationRegistration and SNAP requires valid display
# DeformableModelSimplexMesh and CellularSegmentation requires patented algorithms
mv CMakeLists.txt CMakeLists.sav
egrep -v 'LandmarkInitializedMutualInformationRegistration|SNAP|DeformableModelSimplexMesh|CellularSegmentation' CMakeLists.sav > CMakeLists.txt

# remove CVS dirs
find -name CVS -type d | xargs rm -rf

%patch0 -p1

#------------------------------------------------------------------------
%build
(
%cmake	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DBUILD_DOXYGEN:BOOL=ON \
	-DBUILD_TESTING:BOOL=ON \
	-DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
	-DCMAKE_C_FLAGS:STRING="%{optflags}" \
	-DCMAKE_SKIP_RPATH:BOOL=ON \
	-DCMAKE_EXE_LINKER_FLAGS:STRING="-L%{_libdir}/InsightToolkit -L%{_libdir}/vtk/python/" \
	-DCMAKE_MODULE_LINKER_FLAGS:STRING="-L%{_libdir}/InsightToolkit -L%{_libdir}/vtk/python/" \
	-DCMAKE_SHARED_LINKER_FLAGS:STRING="-L%{_libdir}/InsightToolkit -L%{_libdir}/vtk/python/" \
	-DUSE_FLTK:BOOL=ON \
	-DUSE_VTK:BOOL=ON \
	-DITK_DIR:PATH=%{_libdir}/itk-%{itkver}
%make
)

#------------------------------------------------------------------------
%install
%makeinstall_std -C build
%ifarch x86_64 ppc64
  mv -f %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
%endif

#------------------------------------------------------------------------
%clean
rm -rf %{buildroot}
