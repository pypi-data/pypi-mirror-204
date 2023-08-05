import importlib
import src.jadecobra.tester
import src.jadecobra.versioning
import src.jadecobra.toolkit


class TestZBuildDeploy(src.jadecobra.tester.TestCase):

    version = src.jadecobra.versioning.Version()

    def assert_published_version_is_source_version(self):
        src.jadecobra.toolkit.get_latest_published_version()
        import jadecobra
        importlib.reload(jadecobra)
        self.assertEqual(
            jadecobra.__version__,
            src.jadecobra.__version__
        )
        self.assertEqual(
            jadecobra.__version__,
            self.version.current_pyproject_version
        )

    def test_z_published_version_is_test_version(self):
        # if error publishing
        # update version
        # publish
        # self.assertFalse(True)
        result = src.jadecobra.toolkit.publish(True)
        if result and 'ERROR' in result.stdout.decode():
            self.assertFalse(True)
            src.jadecobra.publish(True)
            self.assert_published_version_is_source_version()
        else:
            self.assertEqual(
                result,
                {}
            )
        # self.assertFalse(True)
