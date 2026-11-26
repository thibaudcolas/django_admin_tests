import unittest

from wasm.deployment import deployment_branch


class DeploymentTests(unittest.TestCase):
    def test_production_and_django_pr_are_separate(self):
        self.assertEqual(deployment_branch("main"), "gh-pages")
        self.assertEqual(deployment_branch("main", "19688"), "preview-19688")
        self.assertEqual(deployment_branch("rtl", "19688"), "preview-19688")
        self.assertEqual(deployment_branch("19688"), "preview-branch-19688")

    def test_branch_aliases_are_stable_and_distinct(self):
        self.assertEqual(deployment_branch("rtl"), "preview-branch-rtl")
        names = ["fix/api", "fix-api", "Fix-API", "a" * 100, "a" * 99 + "b"]
        aliases = [deployment_branch(name) for name in names]
        self.assertEqual(len(set(aliases)), len(names))
        for name, alias in zip(names, aliases):
            self.assertEqual(deployment_branch(name), alias)
            self.assertLessEqual(len(alias), 63)
            self.assertRegex(alias, r"^[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?$")

    def test_rejects_output_branches_and_invalid_prs(self):
        for name in ["", "gh-pages", "preview-19688", "preview-branch-rtl"]:
            with self.assertRaises(ValueError):
                deployment_branch(name)
        for pr in ["0", "-1", "1/head", "12\nbranch=gh-pages"]:
            with self.assertRaises(ValueError):
                deployment_branch("main", pr)
