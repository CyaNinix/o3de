#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

# Cmake version 3.20 is the minimum version needed for all of Open 3D Engine's supported platforms
cmake_minimum_required(VERSION 3.20)

include(cmake/LySet.cmake)
include(cmake/Version.cmake)
include(cmake/OutputDirectory.cmake)

if(NOT PROJECT_NAME)
    include(cmake/CompilerSettings.cmake)
    project(O3DE
        LANGUAGES C CXX
        VERSION ${LY_VERSION_STRING}
    )
endif()

################################################################################
# Initialize
################################################################################
include(cmake/GeneralSettings.cmake)
include(cmake/FileUtil.cmake)
include(cmake/PAL.cmake)
include(cmake/PALTools.cmake)
include(cmake/RuntimeDependencies.cmake)
include(cmake/Configurations.cmake) # Requires to be after PAL so we get platform variable definitions
include(cmake/Dependencies.cmake)
include(cmake/Deployment.cmake)
include(cmake/3rdParty.cmake)
include(cmake/LYPython.cmake)
include(cmake/Install.cmake)
include(cmake/LYWrappers.cmake)
include(cmake/Gems.cmake)
include(cmake/UnitTest.cmake)
include(cmake/LYTestWrappers.cmake)
include(cmake/Monolithic.cmake)
include(cmake/SettingsRegistry.cmake)
include(cmake/TestImpactFramework/LYTestImpactFramework.cmake)
include(cmake/CMakeFiles.cmake)
include(cmake/O3DEJson.cmake)
include(cmake/Subdirectories.cmake)

# Gather the list of o3de_manifest external Subdirectories
# into the LY_EXTERNAL_SUBDIRS_O3DE_MANIFEST_PROPERTY
add_o3de_manifest_json_external_subdirectories()

# Add the projects first so the Launcher can find them
include(cmake/Projects.cmake)


if(NOT INSTALLED_ENGINE)
    # Add external subdirectories listed in the engine.json.
    # LY_EXTERNAL_SUBDIRS is a cache variable so the user can add extra
    # external subdirectories.
    add_engine_json_external_subdirectories()

    # Add the rest of the targets
    add_subdirectory(Assets)
    add_subdirectory(Code)
    add_subdirectory(python)
    add_subdirectory(Registry)
    add_subdirectory(scripts)
    add_subdirectory(Templates)
    add_subdirectory(Tools)

    # Invoke add_subdirectory on all external subdirectories
    # that is in use by the union of projects specified by path in LY_PROJECTS
    add_subdirectory_on_external_subdirs()

else()
    ly_find_o3de_packages()
    add_subdirectory_on_external_subdirs()
endif()

################################################################################
# Post-processing
################################################################################
# The following steps have to be done after all targets are registered:

# 1. Add any dependencies registered via ly_enable_gems
ly_enable_gems_delayed()

# 2. Defer generation of the StaticModules.inl file which is needed to create the AZ::Module derived class in monolithic
#    builds until after all the targets are known and all the gems are enabled
ly_delayed_generate_static_modules_inl()

# 3. generate a settings registry .setreg file for all ly_add_project_dependencies() and ly_add_target_dependencies() calls
#    to provide applications with the filenames of gem modules to load
#    This must be done before ly_delayed_target_link_libraries() as that inserts BUILD_DEPENDENCIES as MANUALLY_ADDED_DEPENDENCIES
#    if the build dependency is a MODULE_LIBRARY. That would cause a false load dependency to be generated
ly_delayed_generate_settings_registry()

# 4. link targets where the dependency was yet not declared, we need to have the declaration so we do different
#    linking logic depending on the type of target
ly_delayed_target_link_libraries()

# 5. generate a registry file for unit testing for platforms that support unit testing
if(PAL_TRAIT_BUILD_TESTS_SUPPORTED)
    ly_delayed_generate_unit_test_module_registry()
endif()

# 5. inject runtime dependencies to the targets. We need to do this after (1) since we are going to walk through
#    the dependencies
ly_delayed_generate_runtime_dependencies()

# 6. Perform test impact framework post steps once all of the targets have been enumerated
ly_test_impact_post_step()

# 7. Generate the O3DE find file and setup install locations for scripts, tools, assets etc., required by the engine
if(LY_INSTALL_ENABLED)
    # 8. Generate the O3DE find file and setup install locations for scripts, tools, assets etc., required by the engine
    ly_setup_o3de_install()
    # 9. CPack information (to be included after install)
    include(cmake/Packaging.cmake)
endif()
