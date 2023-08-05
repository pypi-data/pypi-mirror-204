/*
Copyright (c) Microsoft Corporation 2014
Copyright Rene Rivera 2015
Distributed under the Boost Software License, Version 1.0.
(See accompanying file LICENSE_1_0.txt or copy at
http://www.boost.org/LICENSE_1_0.txt)
*/

#ifndef MSGPACK_PREDEF_PLAT_WINDOWS_STORE_H
#define MSGPACK_PREDEF_PLAT_WINDOWS_STORE_H

#include <msgpack/predef/version_number.h>
#include <msgpack/predef/make.h>
#include <msgpack/predef/os/windows.h>

/*`
[heading `MSGPACK_PLAT_WINDOWS_STORE`]

[table
    [[__predef_symbol__] [__predef_version__]]

    [[`WINAPI_FAMILY == WINAPI_FAMILY_APP`] [__predef_detection__]]
    ]
 */

#define MSGPACK_PLAT_WINDOWS_STORE MSGPACK_VERSION_NUMBER_NOT_AVAILABLE

#if MSGPACK_OS_WINDOWS && defined(WINAPI_FAMILY) && WINAPI_FAMILY == WINAPI_FAMILY_APP
#   undef MSGPACK_PLAT_WINDOWS_STORE
#   define MSGPACK_PLAT_WINDOWS_STORE MSGPACK_VERSION_NUMBER_AVAILABLE
#endif
 
#if MSGPACK_PLAT_WINDOWS_STORE
#   define MSGPACK_PLAT_WINDOWS_STORE_AVAILABLE
#   include <msgpack/predef/detail/platform_detected.h>
#endif

#define MSGPACK_PLAT_WINDOWS_STORE_NAME "Windows Store"

#endif

#include <msgpack/predef/detail/test.h>
MSGPACK_PREDEF_DECLARE_TEST(MSGPACK_PLAT_WINDOWS_STORE,MSGPACK_PLAT_WINDOWS_STORE_NAME)
