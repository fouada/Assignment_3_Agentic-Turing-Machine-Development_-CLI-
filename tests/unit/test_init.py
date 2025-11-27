"""
Unit tests for src/__init__.py

Tests cover:
- Module imports
- Version info
- Path constants
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestModuleImports:
    """Test module-level imports and constants"""

    def test_version_defined(self):
        """Test that __version__ is defined"""
        import src
        assert hasattr(src, "__version__")
        assert isinstance(src.__version__, str)
        assert len(src.__version__) > 0

    def test_author_defined(self):
        """Test that __author__ is defined"""
        import src
        assert hasattr(src, "__author__")
        assert isinstance(src.__author__, str)
        assert len(src.__author__) > 0

    def test_project_root_defined(self):
        """Test that PROJECT_ROOT is defined and exists"""
        import src
        assert hasattr(src, "PROJECT_ROOT")
        assert isinstance(src.PROJECT_ROOT, Path)

    def test_skills_dir_defined(self):
        """Test that SKILLS_DIR is defined"""
        import src
        assert hasattr(src, "SKILLS_DIR")
        assert isinstance(src.SKILLS_DIR, Path)
        assert src.SKILLS_DIR.name == "skills"

    def test_data_dir_defined(self):
        """Test that DATA_DIR is defined"""
        import src
        assert hasattr(src, "DATA_DIR")
        assert isinstance(src.DATA_DIR, Path)
        assert src.DATA_DIR.name == "data"

    def test_results_dir_defined(self):
        """Test that RESULTS_DIR is defined"""
        import src
        assert hasattr(src, "RESULTS_DIR")
        assert isinstance(src.RESULTS_DIR, Path)
        assert src.RESULTS_DIR.name == "results"

    def test_config_dir_defined(self):
        """Test that CONFIG_DIR is defined"""
        import src
        assert hasattr(src, "CONFIG_DIR")
        assert isinstance(src.CONFIG_DIR, Path)
        assert src.CONFIG_DIR.name == "config"


class TestPathRelationships:
    """Test relationships between path constants"""

    def test_all_dirs_under_project_root(self):
        """Test that all directory constants are under PROJECT_ROOT"""
        import src
        
        # All these paths should be children of PROJECT_ROOT
        assert src.SKILLS_DIR.parent == src.PROJECT_ROOT or \
               str(src.PROJECT_ROOT) in str(src.SKILLS_DIR)
        assert src.DATA_DIR.parent == src.PROJECT_ROOT or \
               str(src.PROJECT_ROOT) in str(src.DATA_DIR)
        assert src.RESULTS_DIR.parent == src.PROJECT_ROOT or \
               str(src.PROJECT_ROOT) in str(src.RESULTS_DIR)
        assert src.CONFIG_DIR.parent == src.PROJECT_ROOT or \
               str(src.PROJECT_ROOT) in str(src.CONFIG_DIR)

    def test_paths_are_absolute_or_relative(self):
        """Test that paths can be resolved"""
        import src
        
        # Paths should be resolvable (either absolute or relative)
        assert src.PROJECT_ROOT is not None
        assert src.SKILLS_DIR is not None
        assert src.DATA_DIR is not None
        assert src.RESULTS_DIR is not None
        assert src.CONFIG_DIR is not None


class TestModuleDocstring:
    """Test module documentation"""

    def test_module_has_docstring(self):
        """Test that module has a docstring"""
        import src
        assert src.__doc__ is not None
        assert len(src.__doc__) > 0

    def test_docstring_contains_key_info(self):
        """Test that docstring contains project information"""
        import src
        docstring = src.__doc__.lower()
        assert "agentic" in docstring or "turing" in docstring or "machine" in docstring


class TestModuleImportability:
    """Test that the module can be imported without errors"""

    def test_import_src_module(self):
        """Test basic import of src module"""
        try:
            import src
            assert src is not None
        except ImportError:
            pytest.fail("Failed to import src module")

    def test_reimport_src_module(self):
        """Test that module can be imported multiple times"""
        import src as src1
        import src as src2
        
        # Should be the same module
        assert src1.__version__ == src2.__version__
        assert src1.PROJECT_ROOT == src2.PROJECT_ROOT


class TestVersionFormat:
    """Test version string format"""

    def test_version_format(self):
        """Test that version follows semantic versioning"""
        import src
        version = src.__version__
        
        # Should have at least major.minor format
        parts = version.split(".")
        assert len(parts) >= 2, f"Version {version} doesn't follow semantic versioning"
        
        # First two parts should be numeric
        assert parts[0].isdigit(), f"Major version '{parts[0]}' is not numeric"
        assert parts[1].isdigit(), f"Minor version '{parts[1]}' is not numeric"

