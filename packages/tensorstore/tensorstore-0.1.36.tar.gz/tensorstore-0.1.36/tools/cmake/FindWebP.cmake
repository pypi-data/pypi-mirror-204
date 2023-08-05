# https://github.com/WebKit/webkit/blob/main/Source/cmake/FindWebP.cmake
# Copyright (C) 2020 Sony Interactive Entertainment Inc.
# Copyright (C) 2012 Raphael Kubo da Costa <rakuco@webkit.org>
# Copyright (C) 2013 Igalia S.L.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1.  Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 2.  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND ITS CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR ITS
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#[=======================================================================[.rst:
FindWebP
--------------

Find WebP headers and libraries.

Imported Targets
^^^^^^^^^^^^^^^^

``WebP::webp``
  The WebP library, if found.

``WebP::demux``
  The WebP demux library, if found.

Result Variables
^^^^^^^^^^^^^^^^

This will define the following variables in your project:

``WebP_FOUND``
  true if (the requested version of) WebP is available.
``WebP_VERSION``
  the version of WebP.
``WebP_LIBRARIES``
  the libraries to link against to use WebP.
``WebP_INCLUDE_DIRS``
  where to find the WebP headers.
``WebP_COMPILE_OPTIONS``
  this should be passed to target_compile_options(), if the
  target is not used for linking

#]=======================================================================]

find_package(PkgConfig QUIET)
pkg_check_modules(PC_WEBP QUIET libwebp)
set(WebP_COMPILE_OPTIONS ${PC_WEBP_CFLAGS_OTHER})
set(WebP_VERSION ${PC_WEBP_CFLAGS_VERSION})

find_path(WebP_INCLUDE_DIR
    NAMES webp/decode.h
    HINTS ${PC_WEBP_INCLUDEDIR} ${PC_WEBP_INCLUDE_DIRS}
)

find_library(WebP_LIBRARY
    NAMES ${WebP_NAMES} webp
    HINTS ${PC_WEBP_LIBDIR} ${PC_WEBP_LIBRARY_DIRS}
)

# There's nothing in the WebP headers that could be used to detect the exact
# WebP version being used so don't attempt to do so. A version can only be found
# through pkg-config
if ("${WebP_FIND_VERSION}" VERSION_GREATER "${WebP_VERSION}")
    if (WebP_VERSION)
        message(FATAL_ERROR "Required version (" ${WebP_FIND_VERSION} ") is higher than found version (" ${WebP_VERSION} ")")
    else ()
        message(WARNING "Cannot determine WebP version without pkg-config")
    endif ()
endif ()

# Find components
if (WebP_INCLUDE_DIR AND WebP_LIBRARY)
    set(_WebP_REQUIRED_LIBS_FOUND ON)
    set(WebP_LIBS_FOUND "WebP (required): ${WebP_LIBRARY}")
else ()
    set(_WebP_REQUIRED_LIBS_FOUND OFF)
    set(WebP_LIBS_NOT_FOUND "WebP (required)")
endif ()

if ("demux" IN_LIST WebP_FIND_COMPONENTS)
    find_library(WebP_DEMUX_LIBRARY
        NAMES ${WebP_DEMUX_NAMES} webpdemux
        HINTS ${PC_WEBP_LIBDIR} ${PC_WEBP_LIBRARY_DIRS}
    )

    if (WebP_DEMUX_LIBRARY)
        if (WebP_FIND_REQUIRED_demux)
            list(APPEND WebP_LIBS_FOUND "demux (required): ${WebP_DEMUX_LIBRARY}")
        else ()
           list(APPEND WebP_LIBS_FOUND "demux (optional): ${WebP_DEMUX_LIBRARY}")
        endif ()
    else ()
        if (WebP_FIND_REQUIRED_demux)
           set(_WebP_REQUIRED_LIBS_FOUND OFF)
           list(APPEND WebP_LIBS_NOT_FOUND "demux (required)")
        else ()
           list(APPEND WebP_LIBS_NOT_FOUND "demux (optional)")
        endif ()
    endif ()
endif ()

if (NOT WebP_FIND_QUIETLY)
    if (WebP_LIBS_FOUND)
        message(STATUS "Found the following WebP libraries:")
        foreach (found ${WebP_LIBS_FOUND})
            message(STATUS " ${found}")
        endforeach ()
    endif ()
    if (WebP_LIBS_NOT_FOUND)
        message(STATUS "The following WebP libraries were not found:")
        foreach (found ${WebP_LIBS_NOT_FOUND})
            message(STATUS " ${found}")
        endforeach ()
    endif ()
endif ()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(WebP
    FOUND_VAR WebP_FOUND
    REQUIRED_VARS WebP_INCLUDE_DIR WebP_LIBRARY _WebP_REQUIRED_LIBS_FOUND
    VERSION_VAR WebP_VERSION
)

if (WebP_LIBRARY AND NOT TARGET WebP::webp)
    add_library(WebP::webp UNKNOWN IMPORTED GLOBAL)
    set_target_properties(WebP::webp PROPERTIES
        IMPORTED_LOCATION "${WebP_LIBRARY}"
        INTERFACE_COMPILE_OPTIONS "${WebP_COMPILE_OPTIONS}"
        INTERFACE_INCLUDE_DIRECTORIES "${WebP_INCLUDE_DIR}"
    )
endif ()

if (WebP_DEMUX_LIBRARY AND NOT TARGET WebP::demux)
    add_library(WebP::demux UNKNOWN IMPORTED GLOBAL)
    set_target_properties(WebP::demux PROPERTIES
        IMPORTED_LOCATION "${WebP_DEMUX_LIBRARY}"
        INTERFACE_COMPILE_OPTIONS "${WebP_COMPILE_OPTIONS}"
        INTERFACE_INCLUDE_DIRECTORIES "${WebP_INCLUDE_DIR}"
    )
endif ()

mark_as_advanced(
    WebP_INCLUDE_DIR
    WebP_LIBRARY
    WebP_DEMUX_LIBRARY
)

if (WebP_FOUND)
    set(WebP_LIBRARIES ${WebP_LIBRARY} ${WebP_DEMUX_LIBRARY})
    set(WebP_INCLUDE_DIRS ${WebP_INCLUDE_DIR})
endif ()
