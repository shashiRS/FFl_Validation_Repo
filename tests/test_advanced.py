import fundamentals.example as cm_exp


def test_confusion_matrix_example(tmp_path, open_explorer=False):
    cm_exp.main(tmp_path)
    assert (tmp_path / "out" / "report" / "html" / "index.html").exists()
