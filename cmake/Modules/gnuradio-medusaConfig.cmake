find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_MEDUSA gnuradio-medusa)

FIND_PATH(
    GR_MEDUSA_INCLUDE_DIRS
    NAMES gnuradio/medusa/api.h
    HINTS $ENV{MEDUSA_DIR}/include
        ${PC_MEDUSA_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_MEDUSA_LIBRARIES
    NAMES gnuradio-medusa
    HINTS $ENV{MEDUSA_DIR}/lib
        ${PC_MEDUSA_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-medusaTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_MEDUSA DEFAULT_MSG GR_MEDUSA_LIBRARIES GR_MEDUSA_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_MEDUSA_LIBRARIES GR_MEDUSA_INCLUDE_DIRS)
