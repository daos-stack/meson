#
# spec file for package meson
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global flavor %{nil}
%if "%{flavor}" == "test"
%define name_ext -test
%bcond_without test
%else
%define name_ext %{nil}
%bcond_with test
%endif
%define _name   mesonbuild
%{!?vim_data_dir:%global vim_data_dir %{_datadir}/vim}
%bcond_with setuptools
Name:           meson%{name_ext}
Version:        0.49.0
Release:        128.1
Summary:        Python-based build system
License:        Apache-2.0
Group:          Development/Tools/Building
URL:            http://mesonbuild.com/
Source:         https://github.com/%{_name}/meson/releases/download/%{version}/meson-%{version}.tar.gz
Source1:        https://github.com/%{_name}/meson/releases/download/%{version}/meson-%{version}.tar.gz.asc
Source2:        meson.keyring
# PATCH-FIX-OPENSUSE meson-suse-ify-macros.patch dimstar@opensuse.org -- Make the macros non-RedHat specific: so far there are no separate {C,CXX,F}FLAGS.
Patch0:         meson-suse-ify-macros.patch
# PATCH-FIX-OPENSUSE meson-test-installed-bin.patch dimstar@opensuse.org -- We want the test suite to run against /usr/bin/meson coming from our meson package.
Patch1:         meson-test-installed-bin.patch
# PATCH-FIX-OPENSUSE meson-restore-python3.4.patch -- Restore Python 3.4 support (reverts commit 0538009).
Patch2:         meson-restore-python3.4.patch
# PATCH-FIX-OPENSUSE meson-suse-fix-llvm-3.8.patch -- Fix LLVM 3.8 tests.
Patch3:         meson-suse-fix-llvm-3.8.patch
# PATCH-FIX-OPENSUSE meson-fix-gcc48.patch sor.alexei@meowr.ru -- Fix GCC 4.8 handling for openSUSE Leap 42.x.
Patch4:         meson-fix-gcc48.patch
# PATCH-FEATURE-OPENSUSE meson-distutils.patch tchvatal@suse.com -- build and install using distutils instead of full setuptools
Patch5:         meson-distutils.patch
# PATCH-FIX-UPSTREAM meson-no-lrelease.patch dimstar@opensuse.org -- Don't require lrelease for qt
Patch6:         meson-no-lrelease.patch
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
BuildRequires:  python3-base
BuildArch:      noarch
%if %{with setuptools}
BuildRequires:  python3-setuptools
Requires:       python3-setuptools
%endif
%if !%{with test}
Requires:       ninja
Requires:       python3-base
# meson-gui was last used in openSUSE Leap 42.1.
Provides:       meson-gui = %{version}
Obsoletes:      meson-gui < %{version}
%else
BuildRequires:  bison
BuildRequires:  clang
BuildRequires:  cups-devel
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gcc-fortran
BuildRequires:  gcc-obj-c++
BuildRequires:  gcc-objc
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  gnustep-make
BuildRequires:  googletest-devel
BuildRequires:  itstool
BuildRequires:  libjpeg-devel
BuildRequires:  libpcap-devel
BuildRequires:  libqt5-qtbase-common-devel
BuildRequires:  libqt5-qtbase-private-headers-devel
BuildRequires:  libwmf-devel
BuildRequires:  llvm-devel
BuildRequires:  meson = %{version}
BuildRequires:  ninja
BuildRequires:  pkgconfig
BuildRequires:  python2-devel
BuildRequires:  python3-gobject
BuildRequires:  zlib-devel-static
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(python3) >= 3.4
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(vapigen)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(zlib)
%if 0%{?suse_version} >= 1500
BuildRequires:  java-headless
BuildRequires:  libboost_log-devel
BuildRequires:  libboost_system-devel
BuildRequires:  libboost_test-devel
BuildRequires:  libboost_thread-devel
BuildRequires:  rust
BuildRequires:  rust-std
BuildRequires:  wxWidgets-any-devel
# csharp is not on s390 machines
%ifnarch s390x
BuildRequires:  mono(csharp)
%endif
%else
BuildRequires:  boost-devel
BuildRequires:  mono-core
BuildRequires:  wxWidgets-devel
%endif
%endif

%description
Meson is a build system designed to optimise programmer productivity.
It aims to do this by providing support for software development
tools and practices, such as unit tests, coverage reports, Valgrind,
CCache and the like. Supported languages include C, C++, Fortran,
Java, Rust. Build definitions are written in a non-turing complete
Domain Specific Language.

%package vim
Summary:        Vim support for meson.build files
Group:          Productivity/Text/Editors
Requires:       vim
Supplements:    packageand(vim:%{name})
BuildArch:      noarch

%description vim
Meson is a build system designed to optimise programmer productivity.
It aims to do this by providing support for software development
tools and practices, such as unit tests, coverage reports, Valgrind,
CCache and the like. Supported languages include C, C++, Fortran,
Java, Rust. Build definitions are written in a non-turing complete
Domain Specific Language.

This package provides support for meson.build files in Vim.

%prep
%setup -q -n meson-%{version}
%patch0 -p1
%patch1 -p1
%if 0%{?suse_version} < 1500
%patch2 -p1
%patch3 -p1
%patch4 -p1
%endif
%if !%{with setuptools}
%patch5 -p1
%endif
%patch6 -p1

# Remove static boost tests from "test cases/frameworks/1 boost/".
sed -i "/static/d" test\ cases/frameworks/1\ boost/meson.build

# Disable test of llvm-static libs: openSUSE does not package/ship them
sed -i "s/foreach static : \[true, false\]/foreach static : \[false\]/" test\ cases/frameworks/15\ llvm/meson.build

# We do not have gmock available at this moment - can't run the test suite for it
rm -r "test cases/frameworks/3 gmock" \
      "test cases/objc/2 nsstring"

# AddressSanitizer fails here because of ulimit.
sed -i "/def test_generate_gir_with_address_sanitizer/s/$/\n        raise unittest.SkipTest('ulimit')/" run_unittests.py

# Remove hashbang from non-exec script
sed -i '1{/\/usr\/bin\/env/d;}' ./mesonbuild/rewriter.py

# remove gtest check that actually works because our gtest has .pc files
rm -rf test\ cases/failing/85\ gtest\ dependency\ with\ version

%build
%if !%{with test}
%python3_build
%else
# FIXME: you should use %%meson macros
# Ensure we have no mesonbuild / meson in CWD, thus guaranteeing we use meson in $PATH
rm -r meson.py mesonbuild
%endif

%install
# If this is the test suite, we don't need anything else but the meson package
%if !%{with test}
%python3_install
%fdupes %{buildroot}%{python3_sitelib}

install -Dpm 0644 data/macros.meson \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.meson

install -Dpm 0644 data/syntax-highlighting/vim/ftdetect/meson.vim \
  -t %{buildroot}%{vim_data_dir}/site/ftdetect/
install -Dpm 0644 data/syntax-highlighting/vim/indent/meson.vim \
  -t %{buildroot}%{vim_data_dir}/site/indent/
install -Dpm 0644 data/syntax-highlighting/vim/syntax/meson.vim \
  -t %{buildroot}%{vim_data_dir}/site/syntax/

# entry points are not distutils-able
%if !%{with setuptools}
mkdir -p %{buildroot}%{_bindir}
echo """#!%{_bindir}/python3
import sys

from mesonbuild.mesonmain import main
sys.exit(main())
""" > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

# ensure egg-info is a directory
rm %{buildroot}%{python3_sitelib}/*.egg-info
cp -r meson.egg-info %{buildroot}%{python3_sitelib}/meson-%{version}-py%{python3_version}.egg-info
%endif
%endif

%if %{with test}
%check
export LANG=C.UTF-8
export MESON_EXE=%{_bindir}/meson
python3 run_tests.py --failfast
%endif

%files
%license COPYING
%if !%{with test}
%{_bindir}/meson
%{python3_sitelib}/%{_name}/
%{python3_sitelib}/meson-*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions/
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy
%{_rpmconfigdir}/macros.d/macros.meson
%{_mandir}/man1/meson.1%{?ext_man}

%files vim
%doc data/syntax-highlighting/vim/README
%dir %{vim_data_dir}/
%dir %{vim_data_dir}/site/
%dir %{vim_data_dir}/site/ftdetect/
%dir %{vim_data_dir}/site/indent/
%dir %{vim_data_dir}/site/syntax/
%{vim_data_dir}/site/ftdetect/meson.vim
%{vim_data_dir}/site/indent/meson.vim
%{vim_data_dir}/site/syntax/meson.vim
%endif

%changelog
* Thu Jan 17 2019 tchvatal@suse.com
- Switch to distutils build and properly create egg-info
* Wed Jan 16 2019 dimstar@opensuse.org
- Add meson-no-lrelease.patch: Don't require lrelease for qt.
* Wed Jan  9 2019 tchvatal@suse.com
- Remove succeeding supposed failing gtest test that checks
  gtest version, openSUSE ships the .pc file with the actual
  informations
* Wed Jan  9 2019 tchvatal@suse.com
- Make sure the tests stop on the failure and output the failing
  test at the end for easier digging
* Wed Jan  9 2019 tchvatal@suse.com
- Make the setuptools conditional so I can quickly switch around
  and verify things
* Wed Jan  9 2019 tchvatal@suse.com
- Switch the package to use _multibuild rather than multiple
  spec files
* Tue Jan  8 2019 tchvatal@suse.com
- Use distutils to build/run rather than setuptools to reduce
  buildcycle
- Add patch to be able to build and install using distutils instead
  of full setuptools:
  * meson-distutils.patch
* Tue Dec 11 2018 sor.alexei@meowr.ru
- Update to version 0.49.0:
  * See https://mesonbuild.com/Release-notes-for-0-49-0.html
- Rebase meson-test-installed-bin.patch.
- Rebase meson-suse-fix-llvm-3.8.patch,
  meson-restore-python3.4.patch.
- Add more testsuite dependencies: clang, java-headless,
  mono(csharp), wxWidgets-any-devel.
* Mon Nov 12 2018 sor.alexei@meowr.ru
- Update to version 0.48.2:
  * See https://github.com/mesonbuild/meson/milestone/32?closed=1
* Thu Oct 18 2018 bjorn.lie@gmail.com
- Update to version 0.48.1:
  * See https://github.com/mesonbuild/meson/milestone/31?closed=1
- Drop meson-Fix-handling-generated-desktop-files.patch: Fixed
  upstream.
* Fri Oct  5 2018 bjorn.lie@gmail.com
- Add meson-Fix-handling-generated-desktop-files.patch: Fix
  handling generated .desktop files.
* Mon Oct  1 2018 dimstar@opensuse.org
- Require python3-setuptools.
* Fri Sep 28 2018 sor.alexei@meowr.ru
- Update to version 0.48.0:
  * See http://mesonbuild.com/Release-notes-for-0-48-0.html
- Disable test_generate_gir_with_address_sanitizer with a regex,
  for it fails with ulimits defined in OBS.
- Test against Rust in meson-testsuite on Leap 15.0 or later.
- Rebase meson-suse-ify-macros.patch,
  meson-restore-python3.4.patch, meson-fix-gcc48.patch.
* Sat Aug 25 2018 sor.alexei@meowr.ru
- Update to version 0.47.2:
  * https://github.com/mesonbuild/meson/milestone/29?closed=1
- Rebase meson-restore-python3.4.patch, meson-fix-gcc48.patch.
* Fri Aug  3 2018 sor.alexei@meowr.ru
- Update to version 0.47.1:
  * See https://mesonbuild.com/Release-notes-for-0-47-0.html
- Remove Don-t-raise-StopIteration-in-generators-no-longer-al.patch.
- Add a new dependency for tests:
  libqt5-qtbase-private-headers-devel.
- Set MESON_EXE for tests.
- Adjust meson-test-installed-bin.patch.
- Rebase meson-restore-python3.4.patch, meson-fix-gcc48.patch.
- No longer test with OpenMPI: starting with this release
  "-Wl,--no-undefined -Wl,--as-needed" appears in the gfortran
  arguments, causing an error similiar to lp#1727474.
* Sat Jul 28 2018 bjorn.lie@gmail.com
- Update to version 0.46.1:
  * See https://github.com/mesonbuild/meson/milestone/26?closed=1
- Drop meson-keep-spaces-in-pc-files.patch: Fixed upstream.
* Fri Jul 13 2018 jslaby@suse.com
- Add Don-t-raise-StopIteration-in-generators-no-longer-al.patch
* Sun May 20 2018 dimstar@opensuse.org
- BuildRequire python3-base instead of python3: make building a bit
  cheaper.
* Mon Apr 30 2018 dimstar@opensuse.org
- Add meson-keep-spaces-in-pc-files.patch: Keep spaces in generated
  pkgconfig files (gh#mesonbuild/meson#3479).
- Rebase meson-restore-python3.4.patch.
* Wed Apr 25 2018 sor.alexei@meowr.ru
- Update to version 0.46.0:
  * See http://mesonbuild.com/Release-notes-for-0-46-0.html
- Rebase meson-test-installed-bin.patch,
  meson-restore-python3.4.patch, meson-fix-gcc48.patch.
* Wed Mar 21 2018 sor.alexei@meowr.ru
- Only apply meson-suse-fix-llvm-3.8.patch,
  meson-restore-python3.4.patch, meson-fix-gcc48.patch on Leap 42.x
  or older.
* Wed Mar 21 2018 sor.alexei@meowr.ru
- Fix meson-fix-gcc48.patch.
- Add meson-restore-python3.4.patch: Restore Python 3.4 support for
  SLE 12 and openSUSE Leap 42.x.
- Add meson-suse-fix-llvm-3.8.patch: Fix LLVM 3.8 tests for SLE 12
  and openSUSE Leap 42.x..
* Mon Mar 12 2018 dimstar@opensuse.org
- Add libjpeg-devel BuildRequires to test testsuite.
* Mon Mar  5 2018 dimstar@opensuse.org
- Update to version 0.45.0:
  + Config-Tool based dependencies can be specified in a cross
    file.
  + Visual Studio C# compiler support.
  + Removed two deprecated features:
  - The standalone find_library function has been a no-op for a
    long time. From now on it's an error.
  - There used to be a keywordless version of run_target, which
    is no longer valid.
  + Experimental FPGA support.
  + Generator outputs can preserve directory structure.
  + Hexadecimal string literals.
  + install_data()` defaults to `{datadir}/{projectname}`.
  + install_subdir() supports strip_directory.
  + Integer options.
  + New method meson.project_license().
  + Rust cross-compilation.
  + Rust compiler-private library disambiguation.
  + Project templates.
  + Improve test setup selection.
  + Yielding subproject option to superproject.
- Rebase meson-suse-ify-macros.patch.
* Thu Feb 22 2018 dimstar@opensuse.org
- Update to version 0.44.1:
  + Support running out-of-tree tests against a meson in PATH.
  + Don't add rpaths to system libraries.
  + Fix meson location detection from other meson tools.
  + Various boost, pkg-config and vala related fixes.
- Testsuite changes: Remove mesonbuild directory and meson.py
  again before running the test: ensure we test meson as it was
  installed onto the system.
* Mon Feb  5 2018 dimstar@opensuse.org
- Update to version 0.44.0:
  + New features:
  - Added warning function.
  - Adds support for additional Qt5-Module keyword
    moc_extra_arguments.
  - Prefix-dependent defaults for sysconfdir, localstatedir and
    sharedstatedir.
  - An array type for user options.
  - LLVM dependency supports both dynamic and static linking.
  - Added if_found to subdir.
  - get_unquoted() method for the configuration data object.
  - Added disabler object.
  - Config-Tool based dependencies gained a method to get
    arbitrary options.
  - Embedded Python in Windows MSI packages.
- Rebase meson-suse-ify-macros.patch, meson-fix-gcc48.patch and
  meson-test-installed-bin.patch.
- Testsuite changes:
  + Disable tests for static llvm: we don't ship the static libs.
  + Add cmake(Qt5LinguistTools), libwmf-devel BuildRequires and
    zlib-devel-static: new dependencies for various tests.
* Wed Nov 22 2017 sor.alexei@meowr.ru
- Require python3-xml: mesonbuild/modules/qt5.py imports the xml
  module (boo#1068818).
* Mon Oct 23 2017 dimstar@opensuse.org
- Setup MPI runtime environment before running the test suite.
- Remove tests for static boost libraries from
  test\ cases/frameworks/1\ boost/meson.build.
* Thu Oct 19 2017 badshah400@gmail.com
- Update to version 0.43.0:
  + Generator learned capture: Generators can now be configured to
    capture the standard output.
  + Can index CustomTarget objects: The CustomTarget object can
    now be indexed like an array. The resulting object can be used
    as a source file for other Targets, this will create a
    dependency on the original CustomTarget, but will only insert
    the generated file corresponding to the index value of the
    CustomTarget's output keyword.
  + The cross file can now be used for overriding the result of
    find_program. Then issuing the command find_program('objdump')
    will return the version specified in the cross file.
  + Easier handling of supported compiler arguments.
  + Better support for shared libraries in non-system paths: This
    release adds feature parity to shared libraries that are
    either in non-standard system paths or shipped as part of your
    project. On systems that support rpath, Meson automatically
    adds rpath entries to built targets using manually found
    external libraries.
  + The Wrap dependency system now supports Subversion (svn). This
    support is rudimentary. The repository url has to point to a
    specific (sub)directory containing the meson.build file
    (typically trunk/). However, providing a revision is
    supported.
- Rebase meson-test-installed-bin.patch.
- Run sed to strip the hashbang from a non-executable file; this
  prevents an rpmlint warning.
* Wed Oct 11 2017 sor.alexei@meowr.ru
- Don't use obsolete boost-devel for openSUSE Leap 15.0 and newer
  (boo#1062785).
* Mon Oct  2 2017 jdelvare@suse.com
- Update to version 0.42.1. This is a stable update with various
  bug fixes.
* Fri Sep  8 2017 sor.alexei@meowr.ru
- Rebase meson-fix-gcc48.patch (boo#1057701).
* Tue Aug 15 2017 dimstar@opensuse.org
- Extend meson-test-installed-bin.patch: catch some more cases
  where the test suite referenced meson.py from the source
  directory.
- Add vulkan-devel and libpcap-devel BuildRequires for the test
  suite: new dependencies.
* Tue Aug 15 2017 zaitor@opensuse.org
- Update to version 0.42.0:
  + Distribution tarballs from Mercurial repositories. Creating
    distribution tarballs can now be made out of projects based on
    Mercurial. As before, this remains possible only with the Ninja
    backend.
  + Keyword argument verification. Meson will now check the keyword
    arguments used when calling any function and print a warning if
    any of the keyword arguments is not known. In the future this
    will become a hard error.
  + Add support for Genie to Vala compiler. The Vala compiler has
    an alternative syntax, Genie, that uses the .gs file extension.
    Meson now recognises and uses Genie files.
  + Pkgconfig support for additional cflags. The Pkgconfig module
    object can add arbitrary extra cflags to the Cflags value in
    the .pc file, using the "extra_cflags" keyword.
  + Base options accessible via get_option(). Base options are now
    accessible via the get_option() function.
  + Allow crate type configuration for Rust compiler. Rust targets
    now take an optional rust_crate_type keyword, allowing you to
    set the crate type of the resulting artifact. Valid crate types
    are dylib or cdylib for shared libraries, and rlib or staticlib
    for static libraries. For more, see Rust's linkage reference.
  + Simultaneous use of Address- and Undefined Behavior Sanitizers.
    Both the address- and undefined behavior sanitizers can now be
    used simultaneously by passing -Db_sanitize=address,undefined
    to Meson.
  + Unstable SIMD module. A new experimental module to compile code
    with many different SIMD instruction sets and selecting the
    best one at runtime. This module is unstable, meaning it's API
    is subject to change in later releases. It might also be
    removed altogether.
  + Import libraries for executables on Windows. The new keyword
    implib to executable() allows generation of an import library
    for the executable.
  + Added build_rpath keyword argument. You can specify
    build_rpath: '/foo/bar' in build targets and the given path
    will get added to the target's rpath in the build tree. It is
    removed during the install step.
  + Meson will print a warning when the user tries to add an rpath
    linker flag manually, e.g. via link_args to a target. This is
    not recommended because having multiple rpath causes them to
    stomp on each other. This warning will become a hard error in
    some future release.
  + Vulkan dependency module. Vulkan can now be used as native
    dependency. The dependency module will detect the VULKAN_SDK
    environment variable or otherwise try to receive the vulkan
    library and header via pkgconfig or from the system.
  + Limiting the maximum number of linker processes. With the Ninja
    backend it is now possible to limit the maximum number of
    concurrent linker processes. This is usually only needed for
    projects that have many large link steps that cause the system
    to run out of memory if they are run in parallel. This limit
    can be set with the new backend_max_links option.
  + Disable implicit include directories. By default Meson adds the
    current source and build directories to the header search path.
    On some rare occasions this is not desired. Setting the
    implicit_include_directories keyword argument to false these
    directories are not used.
  + Support for MPI dependency. MPI is now supported as a
    dependency. Because dependencies are language-specific, you
    must specify the requested language with the language keyword,
    i.e., dependency('mpi', language='c') will request the C MPI
    headers and libraries. See the MPI dependency for more
    information.
  + Allow excluding files or directories from install_subdir. The
    install_subdir command accepts the new exclude_files and
    exclude_directories keyword arguments that allow specified
    files or directories to be excluded from the installed
    subdirectory.
  + Make all Meson functionality invokable via the main executable.
    Previously Meson had multiple executables such as
    mesonintrospect and mesontest. They are now invokable via the
    main Meson executable like this: meson configure <arguments> #
    equivalent to mesonconf <options> meson test <arguments> #
    equivalent to mesontest <arguments> The old commands are still
    available but they are deprecated and will be removed in some
    future release.
  + Pcap dependency detector. Meson will automatically obtain
    dependency information for pcap using the pcap-config tool. It
    is used like any other dependency.
  + GNOME module mkenums_simple() addition. Most libraries and
    applications use the same standard templates for glib-mkenums.
    There is now a new mkenums_simple() convenience  method that
    passes those default templates to glib-mkenums and allows some
    tweaks such as optional function decorators or leading
    underscores.
- Rebase meson-fix-gcc48.patch and meson-test-installed-bin.patch.
* Sat Jul 22 2017 mailaender@opensuse.org
- Update to version 0.41.2:
  + Various gtkdoc fixes.
  + Fix how rpath directories are handled.
  + pkgconfig: avoid appending slash at Cflags.
  + Fix a missing path issue causing Python traceback.
  + Qt4 support.
  + Skip handling non-available dependencies.
  + vala: Only add --use-header for unity builds regression.
  + Tag functions in asm properly.
* Tue Jun 27 2017 rodrigo.z.lourenco@tecnico.ulisboa.pt
- Add a vim subpackage to add Meson support to Vim.
* Fri Jun 23 2017 dimstar@opensuse.org
- Split testsuite into an own package, in order to keep the build
  dep chain of meson minimal.
- Drop meson-disable-untested-code.patch: no longer required.
- Add meson-test-installed-bin.patch: use /usr/bin/meson instead of
  meson.py from the source tarball. We want to test the meson
  binary package we produced, not the sources directly.
* Fri Jun 23 2017 dimstar@opensuse.org
- Update to version 0.41.1:
  + wxwidgets: Fix usage of multiple dependency() calls.
  + Make external library no-op when used with incompatible
    target (gh#mesonbuild/meson#1941).
  + Failing test for -D dedupping.
  + Preserve standalone -D arguments always.
  + Handle both pkg-config and pkgconf argument order
    (gh#mesonbuild/meson#1934).
* Fri Jun 23 2017 dimstar@opensuse.org
- Update meson-suse-ify-macros.patch: export LANG for all macros.
* Mon Jun 19 2017 rpm@fthiessen.de
- Update to version 0.41.0:
  * Native support for linking against LLVM using
    the dependency function.
  * Pkgconfig support for custom variables.
  * A target for creating tarballs using 'ninja dist'.
  * Support for passing arguments to Rust compiler.
  * All known issues regarding reproducible builds are fixed.
  * Extended template substitution in configure_file
    for @BASENAME@ and @PLAINNAME@ .
  * Support for capturing stdout of a command in configure_file.
- Removed SDL2 test to reduce dependencies (smaller build footprint)
- Dropped upstreamed patch meson-handle-skipped-tests.patch
- Rebased meson-suse-ify-macros.patch and meson-fix-gcc48.patch
* Tue Jun  6 2017 dimstar@opensuse.org
- Make the build footprint smaller to enter ring1: This means we
  skip a couple tests though. Removed BuildRequires: java-devel,
  libqt5-qtbase-devel, mono-core, mono-devel, wxWidgets-devel,
  pkgconfig(protobuf) and pkgconfig(gtk+-3.0).
* Wed May 17 2017 dimstar@opensuse.org
- Add meson-handle-skipped-tests.patch: Actually do skip tests that
  are marked as MESON_SKIP_TEST (gh#mesonbuild/meson#1804).
* Mon May  8 2017 dimstar@opensuse.org
- Update to version 0.40.1:
  + Outputs of generators can be used in custom targets in the VS
    backend.
  + Visual Studio 2017 support.
  + Automatic initialization of subprojects that are git
    submodules.
  + No download mode for wraps.
  + Overriding options per target.
  + Compiler object get define.
  + Cygwin support.
  + Multiple install directories.
  + Can specify method of obtaining dependencies.
  + Link whole contents of static libraries.
  + Unity builds only for subprojects.
  + Running mesonintrospect from scripts.
* Mon Mar 20 2017 dimstar@opensuse.org
- Add meson-disable-untested-code.patch: meson has code in the test
  suite that assumes different behaviour between glib 2.51.5 (rc)
  and 2.52.0 (final); this must be a wrong assumption to start with
  and the test suite fails with 2.52.0. When this was added by
  upstream 4 months before glib-2.52.0 was released, there must
  have been no way at all to test this. We revert back to a state
  like with the previous glib verison, where this test was simply
  skipped (gh#mesonbuild/meson#1480).
* Thu Mar 16 2017 sor.alexei@meowr.ru
- Update to version 0.39.1 (changes since 0.38.1):
  * Allow specifying extra arguments for tests.
  * Bug fixes and minor polishes.
- Add meson-fix-gcc48.patch: fix GCC 4.8 handling for
  openSUSE Leap 42.x.
* Sat Mar  4 2017 dimstar@opensuse.org
- Update to version 0.38.1:
  + New Uninstall target.
  + Support for arbitrary test setups.
  + Intel C/C++ compiler support.
  + Get values from configuration data objects.
  + Python 3 module support simplified.
  + Default options to subprojects.
  + Set targets to be built (or not) by default.
  + Add option to mesonconf to wipe cached data.
  + Can specify file permissions and owner when installing data.
  + has_header() checks are now faster.
  + Array indexing now supports fallback values.
  + Silent mode for Mesontest.
- Rebase meson-suse-ify-macros.patch.
* Tue Jan 10 2017 dimstar@opensuse.org
- Add meson-suse-ify-macros.patch: Make the meson macros also work
  on openSUSE. We do not (yet?) have separate macros for CFLAGS,
  CXXFLAGS, FFLAGS and LDFLAGS, but only carry optflags. This is no
  issue, since openSUSE so far only added flags that work accross
  compilers/languages. This might change in the future, making the
  patch obsolete.
* Sun Jan  1 2017 sor.alexei@meowr.ru
- Update to version 0.37.1:
  * No changelog available.
* Sun Jan  1 2017 jengelh@inai.de
- Trim boasting words from descriptions. Add to description two
  points from the feature list.
* Mon Dec 19 2016 dev@antergos.com
- Update to version 0.37.0:
  * Mesontest: a new testing tool that allows you to run your
    tests in many different ways.
  * New shared_module function allows shared modules creation.
  * GNOME module now detects required programs and prints useful
    errors if any are missing.
  * GNOME module uses depfile support available in GLib >= 2.52.0.
  * i18n module has a new merge_file() function for creating
    translated files.
  * LLVM IR compilation is now supported.
  * .wrap files for subprojects can now include a separate push
    URL to allow developers to push changes directly from a
    subproject git checkout.
  * Multiple version restrictions while searching for pkg-config
    dependencies is now supported.
  * Support for localstatedir has been added.
  * You can now pass arguments to install scripts added with
    meson.add_install_script().
  * Added new options sbindir and infodir that can be used for
    installation.
- Remove meson-0.36.0-fix-old-pkgconfig-test.patch.
* Sat Dec 10 2016 sor.alexei@meowr.ru
- Add meson-0.36.0-fix-old-pkgconfig-test.patch: tests/common/51:
  Skip validate if pkg-config is too old (commit 2f804e9).
* Tue Nov 22 2016 dimstar@opensuse.org
- Update to version 0.36.0:
  + Add option to run under gdb.
  + Always specify installed data with a File object
    (gh#mesonbuild/meson#858).
  + Made has_function survive optimization flags
    (gh#mesonbuild/meson#1053).
  + Can give many alternative names to find_program to simplify
    searching.
  + Can set compiler arguments in Java.
- Export SUSE_ASNEEDED=0 when running the test suite: linking the
  test libraries/binaries is not done optimally.
* Tue Oct 18 2016 sor.alexei@meowr.ru
- Update to version 0.35.1:
  * No changelog available.
* Fri Oct 14 2016 zaitor@opensuse.org
- Update to version 0.35.0:
  + No changelog available from upstream.
- Changes from version 0.34.0:
  + No changelog available from upstream.
- Drop meson-633.patch and meson-typelib-install.patch : Fixed
  upstream.
* Wed Aug 17 2016 dimstar@opensuse.org
- Update to version 0.33.0:
  + Correctly install .typelib files to libdir.
  + Add option for as-needed link option.
  + Print the CFLAGS/LDFLAGS/etc inherited from the environment.
  + Only append compile flags to the link flags when appropriate.
- Add meson-633.patch: Handle both DT_RPATH as well as DT_RUNPATH
  when fixing rpath settings (gh#mesonbuild/meson#663).
- Add meson-typelib-install.patch: Fix installation path for
  gpobject introspection typelib files.
* Sat Jul 23 2016 sor.alexei@meowr.ru
- Update to version 0.32.0:
  * No changelog available.
- Remove meson-gui package: GUI was removed upstream.
* Mon May  9 2016 jengelh@inai.de
- Avoid unnecessary bashism in %%install script (run with /bin/sh)
* Sat May  7 2016 sor.alexei@meowr.ru
- Update to version 0.31.0.
* Thu Feb 11 2016 sor.alexei@meowr.ru
- Update to 0.29.0.
* Tue Dec 29 2015 sor.alexei@meowr.ru
- Update to 0.28.0.
* Fri Dec  4 2015 sor.alexei@meowr.ru
- Update to 0.27.0.
* Sun Sep 13 2015 sor.alexei@meowr.ru
- Update to 0.26.0.
- Use signed tarball.
* Sun Jul 12 2015 sor.alexei@meowr.ru
- Initial package based on the work of Igor Gnatenko.
