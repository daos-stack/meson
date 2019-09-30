NAME    := meson
SRC_EXT := gz
SOURCE   = https://github.com/$(NAME)build/$(NAME)/releases/download/$(VERSION)/$(NAME)-$(VERSION).tar.$(SRC_EXT)
PATCHES  = $(NAME)-$(VERSION).tar.$(SRC_EXT).asc meson.keyring                  \
	   meson-suse-ify-macros.patch meson-test-installed-bin.patch           \
	   meson-restore-python3.4.patch meson-suse-fix-llvm-3.8.patch          \
	   meson-fix-gcc48.patch meson-distutils.patch meson-no-lrelease.patch

include packaging/Makefile_packaging.mk