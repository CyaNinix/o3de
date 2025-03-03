"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import os
import pytest

import ly_test_tools.environment.file_system as file_system
from ly_test_tools.o3de.editor_test import EditorSingleTest, EditorSharedTest, EditorParallelTest, EditorTestSuite


@pytest.mark.SUITE_main
@pytest.mark.parametrize("launcher_platform", ['windows_editor'])
@pytest.mark.parametrize("project", ["AutomatedTesting"])
class TestAutomationNoAutoTestMode(EditorTestSuite):

    # Disable -autotest_mode and -BatchMode. Tests cannot run in -BatchMode due to UI interactions, and these tests
    # interact with modal dialogs
    global_extra_cmdline_args = []

    # Helper for test level cleanup
    def cleanup_test_level(self, workspace):
        file_system.delete([os.path.join(workspace.paths.engine_root(), "AutomatedTesting", "Levels", "tmp_level")],
                           True, True)

    class test_AssetPicker_UI_UX(EditorSharedTest):
        from .EditorScripts import AssetPicker_UI_UX as test_module

    class test_BasicEditorWorkflows_ExistingLevel_EntityComponentCRUD(EditorSharedTest):
        from .EditorScripts import BasicEditorWorkflows_ExistingLevel_EntityComponentCRUD as test_module

    @pytest.mark.skip(reason="https://github.com/o3de/o3de/issues/9971")
    class test_EditorWorkflow_ParentEntityTransform_Affects_ChildEntityTransform(EditorSharedTest):
        from .EditorScripts import EditorWorkflow_ParentEntityTransform_Affects_ChildEntityTransform as test_module

    @pytest.mark.skip(reason="https://github.com/o3de/o3de/issues/9971")
    class test_EditorWorkflow_ChildEntityTransform_Persists_After_ParentEntityTransform(EditorSharedTest):
        from .EditorScripts import EditorWorkflow_ChildEntityTransform_Persists_After_ParentEntityTransform as test_module

    class test_BasicEditorWorkflows_LevelEntityComponentCRUD(EditorSingleTest):

        # Custom setup and teardown to remove level created during test
        def setup(self, request, workspace, editor, editor_test_results, launcher_platform):
            TestAutomationNoAutoTestMode.cleanup_test_level(self, workspace)

        def teardown(self, request, workspace, editor, editor_test_results, launcher_platform):
            TestAutomationNoAutoTestMode.cleanup_test_level(self, workspace)

        from .EditorScripts import BasicEditorWorkflows_LevelEntityComponentCRUD as test_module

    @pytest.mark.REQUIRES_gpu
    class test_BasicEditorWorkflows_GPU_LevelEntityComponentCRUD(EditorSingleTest):
        # Disable null renderer
        use_null_renderer = False

        # Custom teardown to remove level created during test
        def setup(self, request, workspace, editor, editor_test_results, launcher_platform):
            TestAutomationNoAutoTestMode.cleanup_test_level(self, workspace)

        def teardown(self, request, workspace, editor, editor_test_results, launcher_platform):
            TestAutomationNoAutoTestMode.cleanup_test_level(self, workspace)

        from .EditorScripts import BasicEditorWorkflows_LevelEntityComponentCRUD as test_module

    class test_InputBindings_Add_Remove_Input_Events(EditorSharedTest):
        from .EditorScripts import InputBindings_Add_Remove_Input_Events as test_module


@pytest.mark.SUITE_main
@pytest.mark.parametrize("launcher_platform", ['windows_editor'])
@pytest.mark.parametrize("project", ["AutomatedTesting"])
class TestAutomationAutoTestMode(EditorTestSuite):

    # Enable only -autotest_mode for these tests. Tests cannot run in -BatchMode due to UI interactions
    global_extra_cmdline_args = ["-autotest_mode"]

    class test_AssetBrowser_SearchFiltering(EditorSharedTest):
        from .EditorScripts import AssetBrowser_SearchFiltering as test_module

    class test_AssetBrowser_TreeNavigation(EditorSharedTest):
        from .EditorScripts import AssetBrowser_TreeNavigation as test_module

    @pytest.mark.xfail(reason="Unknown failure. Investigation blocked by https://github.com/o3de/o3de/issues/8108")
    class test_ComponentCRUD_Add_Delete_Components(EditorSharedTest):
        from .EditorScripts import ComponentCRUD_Add_Delete_Components as test_module

    @pytest.mark.REQUIRES_gpu
    class test_Docking_BasicDockedTools(EditorSharedTest):
        from .EditorScripts import Docking_BasicDockedTools as test_module

    class test_EntityOutliner_EntityOrdering(EditorSharedTest):
        from .EditorScripts import EntityOutliner_EntityOrdering as test_module

    class test_Menus_EditMenuOptions_Work(EditorSharedTest):
        from .EditorScripts import Menus_EditMenuOptions as test_module

    class test_Menus_FileMenuOptions_Work(EditorSharedTest):
        from .EditorScripts import Menus_FileMenuOptions as test_module

    class test_Menus_ViewMenuOptions_Work(EditorSharedTest):
        from .EditorScripts import Menus_ViewMenuOptions as test_module
