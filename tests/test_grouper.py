from indexer.grouper import density_group


def test_sparse_folders_merge_to_parent():
    # Only 2 files in a/b/ — below threshold of 5, should group to "a/b"
    files = ["a/b/foo.py", "a/b/bar.py"]
    groups = density_group(files, merge_threshold=5)
    assert all(g == "a/b" for g in groups.values())


def test_dense_folder_gets_own_page():
    # 6 files in a/b/ — at threshold, should stay together as "a/b"
    files = [f"a/b/file{i}.py" for i in range(6)]
    groups = density_group(files, merge_threshold=5)
    assert len(set(groups.values())) == 1
    assert all(g == "a/b" for g in groups.values())


def test_different_folders_get_separate_groups():
    files = ["auth/middleware.py", "auth/tokens.py", "api/routes.py", "api/views.py"]
    groups = density_group(files, merge_threshold=1)
    assert groups["auth/middleware.py"] != groups["api/routes.py"]


def test_deep_sparse_merges_upward():
    # a/b/c/ has only 1 file — sparse, should merge with a/b/other.py into same group
    files = ["a/b/c/lone.py", "a/b/other.py"]
    groups = density_group(files, merge_threshold=3)
    assert groups["a/b/c/lone.py"] == groups["a/b/other.py"]


def test_root_level_files():
    files = ["main.py", "config.py"]
    groups = density_group(files, merge_threshold=5)
    # root files should have a consistent group label
    assert groups["main.py"] == groups["config.py"]


def test_returns_all_files():
    files = ["a/b/foo.py", "a/c/bar.py", "main.py"]
    groups = density_group(files, merge_threshold=5)
    assert set(groups.keys()) == set(files)
